


async function obtenerDatos(endpoint) {

    const response = await fetch(
        `http://127.0.0.1:8000/${endpoint}`
    );

    return await response.json();
}


async function cargarClientesKPI() {

    const data = await obtenerDatos("numeroclientes");

    document.getElementById("clientesKPI")
        .innerText = data[0].total_clientes;
}
async function cargarCuentasKPI() {

    const data = await obtenerDatos("totalcuentas");

    document.getElementById("cuentasKPI")
        .innerText = data[0].total_cuentas;
}
async function cargarEstadoClientes() {

    const data = await obtenerDatos(
        "clientesacteinact"
    );

    const activos = data.find(
        x => x.estado === "Activos"
    );

    const inactivos = data.find(
        x => x.estado === "Inactivos"
    );

    document.getElementById("activosKPI")
        .innerText = activos.cantidad;

    document.getElementById("inactivosKPI")
        .innerText = inactivos.cantidad;
}
async function cargarVolumenKPI() {

    const data = await obtenerDatos("volumen");

    document.getElementById("volumenKPI")
        .innerText =
        `$${data.volumen_total_miles.toLocaleString() + ' USD'}`;
}
async function cargarCuentasChart() {

    const data = await obtenerDatos(
        "cuentasporusuario"
    );

    const labels = data.map(x => x._id);

    const valores = data.map(
        x => x.cantidad_cuentas
    );

    const ctx = document
        .getElementById("cuentasChart");

    new Chart(ctx, {

        type: "bar",

        data: {

            labels: labels,

            datasets: [{
                label: "Cantidad de cuentas",
                data: valores,
                backgroundColor: "#4e73df"
            }]
        },

        options: {

            responsive: true,

            plugins: {

                title: {
                    display: true,
                    text: "Perfil de clientes según la cantidad de cuentas",
                    font: {
                        size: 20
                    }
                }
            },

            scales: {

                x: {

                    title: {
                        display: true,
                        text: "Número de productos por cuenta",
                        font: {
                            size: 14
                        }
                    }
                },

                y: {

                    beginAtZero: true,

                    title: {
                        display: true,
                        text: "Cantidad de clientes",
                        font: {
                            size: 14
                        }
                    }
                }
            }
        }
    });
}
async function cargarTopClientesChart() {

    const data = await obtenerDatos(
        "topclientes"
    );

    const labels = data.map(x => x.cliente);

    const volumen = data.map(
        x => x.volumen_total
    );

    const transacciones = data.map(
        x => x.transacciones
    );

    const ctx = document
        .getElementById("topClientesChart");

    new Chart(ctx, {

        type: "bar",

        data: {

            labels: labels,

            datasets: [

                {
                    label: "Volumen",
                    data: volumen
                },

                {
                    label: "Transacciones",
                    data: transacciones
                }
            ]
        },

        options: {
            plugins: {
                title: {
                    display: true,
                    text: "Top 10 clientes con mayor volumen transaccional",
                    font: {
                        size:20
                    }
                }
            },
           scales: {

                x: {

                    title: {
                        display: true,
                        text: "Cliente",
                        font: {
                            size: 14
                        }
                    }
                },

                y: {

                    beginAtZero: true,

                    title: {
                        display: true,
                        text: "Volumen transaccional(USD)",
                        font: {
                            size: 14
                        }
                    }
                }
            }
        }
        
    });
}
async function cargarVolumenMensualChart() {

    const data = await obtenerDatos(
        "volumenes"
    );

    const labels = data.map(x => x.mes);

    const valores = data.map(x => x.volumen);

    const ctx = document
        .getElementById("volumenMensualChart");

    new Chart(ctx, {

        type: "line",

        data: {

            labels: labels,

            datasets: [{
                label: "Volumen mensual",
                data: valores
            }]
        },

        options: {
            plugins: {
                title: {
                    display: true,
                    text: "Volumen histórico por mes",
                    font: {
                        size:20
                    }
                }
            },
            scales: {

                x: {

                    title: {
                        display: true,
                        text: "Mes (03/1962-01/2017)",
                        font: {
                            size: 14
                        }
                    }
                },

                y: {

                    beginAtZero: true,

                    title: {
                        display: true,
                        text: "Volumen transaccional(USD)",
                        font: {
                            size: 14
                        }
                    }
                }
            }
        }
    });
}
async function cargarProductosChart() {

    const data = await obtenerDatos(
        "proporcionproductos"
    );

    const labels = data.map(x => x.producto);

    const valores = data.map(
        x => x.cantidad_cuentas
    );

    const ctx = document
        .getElementById("productosChart");

    new Chart(ctx, {
    type: "pie",
    data: {
        labels: labels,
        datasets: [{
            data: valores
        }]
    },
    options: {
        plugins: {
            title: {
                    display: true,
                    text: "Composición del Uso de Productos Financieros",
                    font: {
                        size:20
                    }
                },
            tooltip: {
                callbacks: {
                    label: (context) => {

                        const data = context.chart.data.datasets[0].data;

                        const total = data.reduce((a, b) => a + b, 0);

                        const value = context.raw;

                        const percentage = ((value / total) * 100).toFixed(2);

                        return `${context.label}: ${value} (${percentage}%)`;
                    }
                }
            }
        }
    }
});
}
async function cargarTabla() {

    const data = await obtenerDatos(
        "topclientes"
    );

    const tbody = document.querySelector(
        "#summaryTable tbody"
    );

    data.forEach(cliente => {

        const row = `
            <tr>
                <td>${cliente.username}</td>
                <td>$${cliente.volumen_total.toFixed(0)}</td>
                <td>${cliente.transacciones}</td>
            </tr>
        `;

        tbody.innerHTML += row;
    });
}
async function cargarTablaAnomalias() {

    const data = await obtenerDatos("anomalias");

    const tbody = document.querySelector("#anomaliesTable tbody");

    const rows = [

        {
            tipo: "Transacciones muy grandes",
            descripcion: "Transacciones con montos extremadamente altos",
            cantidad: data.transacciones_muy_grandes
        },

        {
            tipo: "Cuentas con límites altos",
            descripcion: "Cuentas con límite máximo de crédito (10000)",
            cantidad: data.cuentas_limites_muy_altos
        },

        {
            tipo: "Clientes Platinum",
            descripcion: "Clientes con algún beneficio de categoría platinum",
            cantidad: data.clientes_con_platinum
        }
    ];

    rows.forEach(r => {

        const row = `
            <tr>
                <td>${r.tipo}</td>
                <td>${r.descripcion}</td>
                <td>${r.cantidad}</td>
            </tr>
        `;

        tbody.innerHTML += row;
    });
}
async function cargarTransaccionesPorAnio() {
    const year = document.getElementById("yearSelect").value;

    if (!year) {
        document.getElementById("transaccionesAnioKPI").innerText = "";
        return;
    }

    const data = await obtenerDatos(`transacciones/anio/${year}`);

    document.getElementById("transaccionesAnioKPI").innerText =
        data.total_transacciones.toLocaleString();
}

cargarClientesKPI();
cargarCuentasKPI();
cargarEstadoClientes();
cargarVolumenKPI();

cargarCuentasChart();
cargarTopClientesChart();
cargarVolumenMensualChart();
cargarProductosChart();
cargarTablaAnomalias();

cargarTabla();
cargarTransaccionesPorAnio()