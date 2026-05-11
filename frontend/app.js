


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
        `$${data.volumen_total_miles.toLocaleString()}`;
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
                label: "Cantidad cuentas",
                data: valores
            }]
        }
    });
}
async function cargarTopClientesChart() {

    const data = await obtenerDatos(
        "topclientes"
    );

    const labels = data.map(x => x.username);

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

cargarClientesKPI();
cargarCuentasKPI();
cargarEstadoClientes();
cargarVolumenKPI();

cargarCuentasChart();
cargarTopClientesChart();
cargarVolumenMensualChart();
cargarProductosChart();

cargarTabla();