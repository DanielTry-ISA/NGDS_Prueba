import numpy as np
from dotenv import load_dotenv
from fastapi import FastAPI
import os

#Variables de entorno
usr = None
pwd = None
clus = None


def load_env():

    global usr,pwd,clus
    load_dotenv()
    usr = os.getenv("MONGO_USR")
    pwd = os.getenv("MONGO_PWD")
    clus = os.getenv("CLUSTER")

load_env()

print(f"el usuario es: {usr} y el cluster es: {clus}")

