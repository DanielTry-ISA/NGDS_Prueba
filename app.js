async function cargarGrafico() {

    // consumir endpoint FastAPI
    const response = await fetch(
        "http://127.0.0.1:8000/metricasagregadas"
    );

    const data = await response.json();

    // labels eje X
    const labels = data.map(item => item._id);

    // valores eje Y
    const valores = data.map(item => item.cantidad_cuentas);

    // obtener canvas
    const ctx = document
        .getElementById("productosChart")
        .getContext("2d");

    // crear gráfica
    new Chart(ctx, {

        type: "bar",

        data: {

            labels: labels,

            datasets: [{
                label: "Cantidad de cuentas",

                data: valores,

                backgroundColor: "rgba(54, 162, 235, 0.7)",

                borderColor: "rgba(54, 162, 235, 1)",

                borderWidth: 1
            }]
        },

        options: {

            responsive: true,

            scales: {

                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

cargarGrafico();