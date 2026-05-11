-------------------------------------📈Panel de Análisis de Cliente💯-------------------------------------

1. 📝 Descripción del proyecto

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


2. 🗂️ Dataset utilizado

Para este proyecto se utilizó el Sample_Analytics que tiene 3 tablas:
Accounts: Contiene información sobre cuentas de clientes
Customers: Contiene detalles sobre los clientes
Transactions: Contiene transacciones de clientes
, para mayor información consultar https://www.mongodb.com/es/docs/atlas/sample-data/sample-analytics/

3. 🏗️ Arquitectura

3.1 Stack Tecnológico 💻
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

3.2 Flujo de Datos 🚀
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
index.html + Chart.js + style.css
     |
     |KPIs y tablas
     ↓
 Dashboard(Navegador)

3.3 Estructura del proyecto 🏗️

NGDS_Prueba/
|--app
|   └--main.py # 11 endpoints
|--frontend
|      └app.js      #Consumo de endpoints
|      └index.html  #Estructura del dashboard
|      └styles      #Estética
|--resources
|      └forestwp.avif
|
|--.env #Variables de entorno
|--.env.example 
|
|--.gitignore
|--README.txt
|--requirements.txt #Configuración del entorno



4. ⚙️ Instalación y ejecución

   1. Crear una carpeta, abrir la terminal en su ubicación y ejecutar git clone https://github.com/DanielTry-ISA/NGDS_Prueba.git
   2. Dentro de esa misma dirección crear un entorno ejecutando python -m venv <NombreDelEntorno> e.g. python -m venv venv
   3. Activar el entorno con el comando <NombreDelEntorno>\Scripts\activate e.g. venv\Scripts\activate 
   4. Cuando el entorno esté activo, ejecutar pip install -r requirements.txt
   5. Ejecutar el backend con el comando uvicorn app.main:app --reload
   6. Abrir otra terminal en la dirección ./frontend y ejecutar el frontend con el comando python -m http.server <<Puerto a utilizar(recomendación 5500)>>
      e.g. python -m http.server 5500
   7. Abrir http://localhost:<<Puerto a utilizar(recomendación 5500)>> e.g. http://localhost:5500


5. 📡 Endpoints
Se crearon 11 endpoints, a continuación se muestra la descripción de cada uno y su formato de salida JSON

   • /numeroclientes: Trae el número total de clientes. Ejemplo de salida: {"total_clientes":500}
   • /totalcuentas: Trae el número total de cuentas. [{"total_cuentas":1746}]
   • /clientesacteinact: Trae el número de clientes activos e inactivos [{"cantidad":499,"estado":"Inactivos"},{"cantidad":1,"estado":"Activos"}]
   • /volumen: Monto total histórico de dinero en movimiento {"volumen_total":35704876501.23871,"cantidad_transacciones":88119,"volumen_total_miles":35704876501.24}
   • /totaltransacciones: Total histórico de transacciones {"total_transacciones":88119}
   • /cuentasporusuario: Cantidad de clientes con un determinado número de cuentas {"_id":1,"cantidad_cuentas":62},{"_id":2,"cantidad_cuentas":520}
   • /topclientes: Top 10 clientes con un mayor volumen transaccional {"username":"zgraham","volumen_total":490114715.70542735,"transacciones":343,"cliente":"Scott Fisher"}
   • /volumenes: Volumen operado cada mes {"volumen":4417.291782586593,"cantidad":1,"mes":"1962-03"},{"volumen":30907.20390520289,"cantidad":1,"mes":"1962-05"}
   • /proporcionproductos: Cantidad de cuentas con un determinado producto {"cantidad_cuentas":1746,"producto":"InvestmentStock"}
   • /anomalías Anomalias {"transacciones_muy_grandes":881,"cuentas_limites_muy_altos":1701,"clientes_con_platinum":101}
   • /transacciones/anio/{year} endpoint dinámico que devuelve el número total de transacciones en un año específico {"year":2015,"total_transacciones":9682}




6. 📊 Pipelines principales

1. Top clientes por volumen transaccional

Endpoint: /topclientes

Este pipeline identifica los clientes con mayor volumen transaccional. Operaciones principales:
- `$lookup`: une la colección `customers` con `transactions` mediante `account_id`
- `$unwind`: desanida el array de transacciones para operar sobre cada una individualmente
- `$group`: agrupa por cliente calculando volumen total y número de transacciones
- `$sort` + `$limit`: retorna los 10 clientes con mayor volumen descendente

------------------------------------------------------------------------------------------------------

2. Volumen transaccional por mes

Endpoint: /volumenes

Este pipeline construye una serie de tiempo con el volumen y cantidad de transacciones
agrupadas mensualmente. Operaciones principales:
- `$unwind`: expande el array de transacciones embebidas
- `$match`: filtra documentos que contengan el campo `total` para evitar errores en la agregación
- `$group`: agrupa por mes usando `$dateToString` con formato `%Y-%m`
- `$sort`: ordena cronológicamente para visualización en gráfica de línea

------------------------------------------------------------------------------------------------------

### 3. Proporción de productos financieros

Endpoint: /proporcionproductos

Este pipeline calcula la distribución de productos financieros entre todas las cuentas,
útil para identificar cuáles son los más adoptados. Operaciones principales:
- `$unwind`: desanida el array `products` de cada cuenta
- `$group`: agrupa por tipo de producto contando cuántas cuentas lo tienen
- `$sort`: ordena por popularidad descendente para visualización en gráfica de torta

------------------------------------------------------------------------------------------------------

### 4. ⭐ Detección de transacciones anómalas (Percentil 99)

Endpoint: /anomalias

Este pipeline es el núcleo analítico del dashboard. Calcula el umbral estadístico del
percentil 99 sobre todas las transacciones y cuantifica cuántas superan ese umbral,
permitiendo detectar comportamientos atípicos sin un valor de corte arbitrario.
Operaciones principales:
- `$unwind` + `$set`: expande las transacciones y convierte `total` a `Double`
  para operaciones numéricas precisas
- `$group` con `$percentile`: calcula el P99 usando el método `approximate` de MongoDB,
  eficiente para grandes volúmenes. Simultáneamente acumula todos los valores en `$push`
- `$project` con `$filter`: en una sola pasada, expone el umbral P99 y cuenta cuántas
  transacciones lo superan usando `$filter` + `$size` sobre el array acumulado,
  evitando una segunda lectura a la colección


7. 📈 Justificación de librería de visualización

Se eligió Chart.js sobre las demás opciones por las siguientes razones:

- COMPATIBILIDAD CON VANILLA JS: al no usar ningún framework frontend (React, Vue, etc.),
  Chart.js se integra directamente sin configuración adicional ni dependencias extra.
- BAJA CURVA DE APRENDIZAJE: su API declarativa permite crear gráficas funcionales
  con pocas líneas de código, priorizando el tiempo de desarrollo en los pipelines y endpoints.
- SUFICIENCIA: para un dashboard analítico con KPIs, barras y líneas
  de tendencia, Chart.js cubre todos los requisitos sin la complejidad de D3.js ni la
  necesidad de licencia comercial de Highcharts.



## 📐 Escalabilidad


Si el volumen de datos creciera significativamente, se aplicarían las siguientes estrategias:

- Sharding por `account_id` para distribuir la carga entre nodos.
- Caché con Redis para los pipelines más costosos como rankings y detección de anomalías.
- Paginación en endpoints que devuelven listas para evitar transferencias masivas.