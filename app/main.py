import numpy as np
from dotenv import load_dotenv
from fastapi import FastAPI
import os
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

app = FastAPI()



client = MongoClient(f'mongodb+srv://developer:{PWD}@datacluster.hfoiucp.mongodb.net/?appName={CLUS}')

db = client['sample_analytics']

accounts_collection = db['accounts']
customers_collection = db['customers']
transactions_collection = db['transactions']

@app.get('/')
def root():
    return{"messsage":"API Funcionando"}

# mongoUri = f'mongodb+srv://developer:{PWD}@datacluster.hfoiucp.mongodb.net/?appName={CLUS}'

#Endpoint
@app.get('/resumen')
def get_data():
    #Verificar si es necesario usar .limit
    # transactions = list(transactions_collection.find({}, {"_id":0}).limit(100))
    accounts = list(accounts_collection.find({},{"_id":0}))
    customers = list(customers_collection.find({},{"_id":0}))
    transactions = list(transactions_collection.find({},{"_id":0}))
    return {'accounts': accounts,
            'customers': customers,
            'transactions': transactions
    }



@app.get('/customers/summary')
def summary():
    return "El endpoint funciona"


@app.get('/metricasagregadas')
def aggregate_data():
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
# print(f"el usuario es: {USR} y el cluster es: {CLUS} y la uri es{return_uri}")

#Primer indicador: numero de clientes
@app.get('/numeroclientes')
def numero_clientes():
    pl_total_clientes = [{"$count": "total_clientes"}]
    result = list(customers_collection.aggregate(pl_total_clientes))
    return result

#Segundo indicador: numero de cuentas
@app.get('/totalcuentas')
def numero_cuentas():
    pl_total_cuentas = [{"$count": "total_cuentas"}]
    result = list(accounts_collection.aggregate(pl_total_cuentas))
    return result

#Tercer indicador: #clientes activos y # clientes inactivos
@app.get('/clientesacteinact')
def activos_inactivos():
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





@app.get('/vol')
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





@app.get('/anomalias')
def anomaly_summary():
    return {'texto':'también funciona :v'}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)