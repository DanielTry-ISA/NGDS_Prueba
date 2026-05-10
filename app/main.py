import numpy as np
from dotenv import load_dotenv
from fastapi import FastAPI
import os
from pymongo import MongoClient

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

@app.get('/metricasagregadas')
def aggregate_data():
    return {'texto':'funciona'}
# print(f"el usuario es: {USR} y el cluster es: {CLUS} y la uri es{return_uri}")

@app.get('/anomalias')
def anomaly_summary():
    return {'texto':'también funciona :v'}