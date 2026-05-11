-------------------------------------📈Panel de Análisis de Cliente💯-------------------------------------

##📝 Descripción del proyecto

Dashboard analítico construido sobre el dataset **sample_analytics** de MongoDB Atlas,
desarrollado como prueba técnica para evaluar exploración de datos, diseño de pipelines
de agregación y construcción de APIs REST con visualización de datos.

A partir de tres colecciones (`customers`, `accounts`, `transactions`), se identificaron
relaciones clave y se propuso un caso de uso financiero: analizar el comportamiento
transaccional de clientes, detectar anomalías y extraer métricas agregadas de valor
para un usuario de negocio.

La solución expone **11 endpoints REST** construidos con **FastAPI**, cada uno respaldado
por aggregation pipelines de MongoDB. Los datos son consumidos por un frontend en
**JavaScript vanilla** y visualizados mediante **Chart.js**.


## 🗂️ Dataset utilizado

Para este proyecto se utilizó el Sample_Analytics que tiene 3 tablas:
Accounts: Contiene información sobre cuentas de clientes
Customers: Contiene detalles sobre los clientes
Transactions: Contiene transacciones de clientes
, para mayor información consultar https://www.mongodb.com/es/docs/atlas/sample-data/sample-analytics/

## 🏗️ Arquitectura

### Stack Tecnológico 💻
+----------------+--------------------------+-----------------------------------------------------------+
| CAPA           | TECNOLOGÍA               | JUSTIFICACIÓN                                             |
+----------------+--------------------------+-----------------------------------------------------------+
| Base de datos  | MongoDB Atlas            | Dataset nativo en formato documento                       |
+----------------+--------------------------+-----------------------------------------------------------+
| Backend        | Python + FastAPI         | Rápido de desarrollar, oportunidad de aprendizaje         |
+----------------+--------------------------+-----------------------------------------------------------+
| Frontend       | HTML + CSS + JS Vanilla  | Frontend robusto y ligero                                 |
+----------------+--------------------------+-----------------------------------------------------------+
| Visualización  | Chart.js                 | Fácil integración                                         |
+----------------+--------------------------+-----------------------------------------------------------+

### Flujo de Datos 🚀
MongoDB Atlas
     | 
     | Aggregation Pipelines
     ↓
main.py(FastAPI)
     |
     | 11 endpoints GET /endpoint
     ↓
   app.js
     |
     | fetch() por cada endpoint
     ↓
index.html + Chart.js
     |
     |KPIs y tablas
     ↓
 Dashboard(Navegador)

### Estructura del proyecto 🏗️

NGDS_Prueba/
|--app
|   └--main.py # 11 endpoints
|
|
|
|
|
|
|
|
|





## ⚙️ Instalación y ejecución

1. Crear una carpeta, abrir cmd en su ubicación y ejecutar git clone https://github.com/DanielTry-ISA/NGDS_Prueba.git
2. Dentro de esa misma dirección crear un entorno ejecutando python -m venv <NombreDelEntorno>
3. Activar el entorno con el comando <NombreDelEntorno>\Scripts\activate
4. Cuando el entorno esté activo, ejecutar pip install -r requirements.txt
5. Ejecutar el backend con el comando uvicorn app.main:app --reload
6. Abrir otra terminal en la dirección ./frontend y ejecutar el frontend con el comando python -m http.server <<Puerto a utilizar(recomendación 5500)>>
7. Abrir http://localhost:<<Puerto a utilizar(recomendación 5500)>>


## 🔐 Variables de entorno
## 📡 Endpoints
## 📊 Pipelines principales
## 📈 Justificación de librería de visualización
## 🗃️ Recomendaciones de índices
## 📐 Escalabilidad
