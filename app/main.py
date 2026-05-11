import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException

#Variables de entorno
USR = None
PWD = None
CLUS = None



# Carga de variables de entorno
def load_env():

    global USR,PWD,CLUS
    load_dotenv()
    USR = os.getenv("MONGO_USR")
    PWD = os.getenv("MONGO_PWD")
    CLUS = os.getenv("CLUSTER")

load_env()

#Aplicación
app = FastAPI()


#Conexión con MongoDB
client = MongoClient(f'mongodb+srv://developer:{PWD}@datacluster.hfoiucp.mongodb.net/?appName={CLUS}')


#Seleccion de base de datos y tablas
db = client['sample_analytics']
accounts_collection = db['accounts']
customers_collection = db['customers']
transactions_collection = db['transactions']

#Endpoint de bienvenida
@app.get('/')
def root():
    return{"messsage":"Sea usted bienvenido!!!"}




#Primer indicador: numero de clientes
@app.get('/numeroclientes')
def numero_clientes():
    try:
        pl_total_clientes = [{"$count": "total_clientes"}]
        result = list(customers_collection.aggregate(pl_total_clientes))
        return result
    except Exception as e:
        print("Error:", str(e))   
        raise HTTPException(status_code=500, detail=str(e))

    

#Segundo indicador: numero de cuentas
@app.get('/totalcuentas')
def numero_cuentas():
    try:
        pl_total_cuentas = [{"$count": "total_cuentas"}]
        result = list(accounts_collection.aggregate(pl_total_cuentas))
        return result
    except Exception as e:
        print("Error:", str(e))   
        raise HTTPException(status_code=500, detail=str(e))

    

#Tercer indicador: #clientes activos y # clientes inactivos
@app.get('/clientesacteinact')
def activos_inactivos():
    try:
        pl_activos_inactivos = [{'$group': {"_id": '$active',
                                       "cantidad": {'$sum':1}
                                       }},
                                       {"$project":{"_id":0,
                                                    "estado": {'$cond':['$_id', "Activos", "Inactivos"]},
                                                    "cantidad" : 1
                                                    }
                                           
                                       }]
        result = list(customers_collection.aggregate(pl_activos_inactivos))
        return result
    except Exception as e:
        print("Error:", str(e))   
        raise HTTPException(status_code=500, detail=str(e))

    




#Cuarto Indicador cantidad de dinero total movido en todas las transacciones
@app.get('/volumen')
def total_dinero():
    try:
        pipeline_volumen_total = [
            {
                "$unwind": "$transactions"   # más simple
            },
            {
                "$match": {
                    "transactions.total": {"$exists": True, "$ne": None}   # filtramos valores malos
                }
            },
            {
                "$group": {
                    "_id": None,
                    "volumen_total": {
                        "$sum": {
                            "$toDouble": "$transactions.total"
                        }
                    },
                    "cantidad_transacciones": {"$sum": 1}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "volumen_total": 1,
                    "cantidad_transacciones": 1,
                    "volumen_total_miles": {
                        "$round": ["$volumen_total", 2]
                    }
                }
            }
        ]

        result = list(transactions_collection.aggregate(pipeline_volumen_total))
        
        if result:
            return result[0]
        else:
            return {
                "volumen_total": 0,
                "cantidad_transacciones": 0,
                "volumen_total_miles": 0
            }
            
    except Exception as e:
        print("Error en pipeline:", str(e))   # ← Esto te ayudará a ver el error en consola
        raise HTTPException(status_code=500, detail=str(e))

#Numero total de transacciones
@app.get('/totaltransacciones')
def total_transacciones():
    try:
        pipeline_total_transacciones = [
    {
        "$group": {
            "_id": None,
            "total_transacciones": {
                "$sum": { "$size": { "$ifNull": ["$transactions", []] } }
            }
        }
    },
    {
        "$project": {
            "_id": 0,
            "total_transacciones": 1
        }
    }
]
        result = list(transactions_collection.aggregate(pipeline_total_transacciones))
        return result[0] if result else {"total_transacciones": 0}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


##GRAFICAS

#Numero de usuarios con 1, 2, 3, 4 y 5 cuentas
@app.get('/cuentasporusuario')
def aggregate_data():
    try:
        cuentas_numproductos = [{
        "$project": {
            "num_productos" : {"$size": "$products"}
        }},
        {"$group":
         {
          "_id": "$num_productos",
          "cantidad_cuentas": {"$sum":1}   
         }
         },
         {
             "$sort": {"_id":1}
         }
    ]
        resultados = list(accounts_collection.aggregate(cuentas_numproductos))
        return resultados
    
    except Exception as e:
        print("Error:", str(e))   
        raise HTTPException(status_code=500, detail=str(e))



#Top 10 clientes con mayor volumen transaccional
@app.get('/topclientes')
def top_clientes():
    try:
        pipeline_top_clientes = [
    {"$lookup": {
        "from": "transactions",
        "localField": "accounts",
        "foreignField": "account_id",
        "as": "cust_tx"
    }},
    {"$unwind": "$cust_tx"},
    {"$unwind": "$cust_tx.transactions"},
    {"$group": {
        "_id": "$_id",
        "name": {"$first": "$name"},
        "username": {"$first": "$username"},
        "volumen_total": {"$sum": {"$toDouble": "$cust_tx.transactions.total"}},
        "transacciones": {"$sum": 1}
    }},
    {"$sort": {"volumen_total": -1}},
    {"$limit": 10},
    {"$project": {
        "_id": 0,
        "cliente": "$name",
        "username": 1,
        "volumen_total": 1,
        "transacciones": 1
    }}
]
        result = list(customers_collection.aggregate(pipeline_top_clientes))
        return result
    except Exception as e:
        print("Error:", str(e))   
        raise HTTPException(status_code=500, detail=str(e))
    


#Volumen de dinero en movimiento por mes
@app.get('/volumenes')
def volumen_por_mes():
    try:
        pipeline_volumen_mes = [
            {"$unwind": "$transactions"},
            {"$match": {"transactions.total": {"$exists": True}}},
            {"$group": {
                "_id": {
                    "$dateToString": {"format": "%Y-%m", "date": "$transactions.date"}
                },
                "volumen": {"$sum": {"$toDouble": "$transactions.total"}},
                "cantidad": {"$sum": 1}
            }},
            {"$sort": {"_id": 1}},
            {"$project": {
                "_id": 0,
                "mes": "$_id",
                "volumen": 1,
                "cantidad": 1
            }}
        ]
        
        
        result = list(transactions_collection.aggregate(pipeline_volumen_mes))
        
        return result
        
    except Exception as e:
        print("Error:", str(e))   
        raise HTTPException(status_code=500, detail=str(e))



    
#Proporción de productos utilizados por los clientes
@app.get('/proporcionproductos')
def proporcion_productos():
    pl_prop_productos = [
    {
        "$unwind": "$products"          
    },
    {
        "$group": {
            "_id": "$products",
            "cantidad_cuentas": {"$sum": 1}
        }
    },
    {
        "$project": {
            "_id": 0,
            "producto": "$_id",
            "cantidad_cuentas": 1
        }
    },
    {
        "$sort": {"cantidad_cuentas": -1}  
    }
]
    try:
        result = list(accounts_collection.aggregate(pl_prop_productos))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    



# Tabla
#Tabla de anomalias
# número de transacciones muy grandes
# cuentas con un límite de 10000
# Clientes con algun beneficio platinum
@app.get('/anomalias')
def anomaly_summary():
    try:
        pipeline_tx_grandes = [

    {
        "$unwind": "$transactions"
    },

    
    {
        "$set": {
            "totalValue": {
                "$toDouble": "$transactions.total"
            }
        }
    },


    {
        "$group": {
            "_id": None,
            "p99": {
                "$percentile": {
                    "input": "$totalValue",
                    "p": [0.99],
                    "method": "approximate"
                }
            },
            "totals": {
                "$push": "$totalValue"
            }
        }
    },


    {
        "$project": {
            "_id": 0,
            "percentile99": {
                "$arrayElemAt": ["$p99", 0]
            },
            "veryLargeTransactions": {
                "$size": {
                    "$filter": {
                        "input": "$totals",
                        "as": "t",
                        "cond": {
                            "$gt": [
                                "$$t",
                                {"$arrayElemAt": ["$p99", 0]}
                            ]
                        }
                    }
                }
            }
        }
    }
]


        result_trans = list(transactions_collection.aggregate(pipeline_tx_grandes))

        pipeline_limites_altos = [

    {
        "$match": {
            "limit": {
                "$gt": 9999
            }
        }
    },

    {
        "$count": "cuentas_limites_muy_altos"
    }
]
        result_lim_alto = list(accounts_collection.aggregate(pipeline_limites_altos))

        pipeline_tier_platino = [
    {
        "$project": {
            "platinum_tiers": {
                "$filter": {
                    "input": {
                        "$objectToArray": "$tier_and_details"
                    },
                    "as": "tier",
                    "cond": {
                        "$eq": [
                            "$$tier.v.tier",
                            "Platinum"
                        ]
                    }
                }
            }
        }
    },
    {
        "$match": {
            "platinum_tiers.0": {
                "$exists": True
            }
        }
    },
    {
        "$count": "total_customers_with_platinum"
    }
]
        result_plat = list(customers_collection.aggregate(pipeline_tier_platino))
        
        # return {result_trans[0], result_lim_alto}
        # return result_plat
        return {
            "transacciones_muy_grandes": result_trans[0].get("veryLargeTransactions", 0) if result_trans else 0,
            "cuentas_limites_muy_altos": result_lim_alto[0].get("cuentas_limites_muy_altos", 0) if result_lim_alto else 0,
            "clientes_con_platinum": result_plat[0].get("total_customers_with_platinum", 0) if result_plat else 0
        }
                
                
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#filtro de número de teansacciones por año
@app.get("/transacciones/anio/{year}")
async def transacciones_por_anio(year: int):
    pipeline = [
        
        { "$unwind": "$transactions" },

        
        {
            "$match": {
                "$expr": {
                    "$eq": [{ "$year": "$transactions.date" }, year]
                }
            }
        },

        
        {
            "$count": "total_transacciones"
        }
    ]

    result = list(transactions_collection.aggregate(pipeline))

    if result:
        return { "year": year, "total_transacciones": result[0]["total_transacciones"] }
    return { "year": year, "total_transacciones": 0 }
    

#Cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)