console.log("Abrió reporte.js");

document.addEventListener("DOMContentLoaded", () => {

    // ===================== GRAFICO DIAS =====================

    new Chart(document.getElementById("graficoDias"), {
        type: "bar",
        data: {
            labels: reservasDia.map(x => x.dia),
            datasets: [{
                label: "Reservas",
                data: reservasDia.map(x => Number(x.total_reservas))
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1,
                        precision: 0
                    }
                }
            }
        }
    });

    // ===================== GRAFICO MES =====================
    new Chart(document.getElementById("graficoTendencia"), {
        type: "line",
        data: {
            labels: reservasMes.map(x => "Mes " + x.mes),
            datasets: [{
                label: "Reservas",
                data: reservasMes.map(x => Number(x.total_reservas))
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1,
                        precision: 0
                    }
                }
            }
        }
    });

    // ===================== GRAFICO HORAS =====================
    new Chart(document.getElementById("graficoHorarios"), {
        type: "bar",
        data: {
            labels: reservasHora.map(x => x.hora),
            datasets: [{
                label: "Reservas",
                data: reservasHora.map(x => Number(x.total_reservas))
            }]
        },
        options: {
            indexAxis: "y",
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1,
                        precision: 0
                    }
                }
            }
        }
    });

    // ===================== GRAFICO ESTADO =====================
    new Chart(document.getElementById("graficoEstado"), {

        type: "doughnut",

        data: {

            labels: ["Activas", "Canceladas"],

            datasets: [{
                data: [
                    estadisticas.reservas_activas,
                    estadisticas.reservas_inactivas
                ]
            }]

        },

        options: {
            responsive: true,
            maintainAspectRatio: false
        }

    });



    document
        .getElementById("formPDFEspecialista")
        .addEventListener("submit", function (e) {

            const especialista =
                document.getElementById("especialista_reporte").value;

            if (!especialista) {

                e.preventDefault();

                Swal.fire({
                    icon: "warning",
                    title: "Seleccione un especialista",
                    text: "Debe seleccionar un especialista para generar su reporte."
                });

                return;
            }

            document.getElementById("pdf_especialista_cedula").value =
                especialista;

        });


    document
        .getElementById("formPDFCliente")
        .addEventListener("submit", function (e) {

            const cliente =
                document.getElementById("cliente_reporte").value;

            if (!cliente) {

                e.preventDefault();

                Swal.fire({
                    icon: "warning",
                    title: "Seleccione un cliente",
                    text: "Debe seleccionar un cliente para generar su reporte."
                });

                return;
            }

            document.getElementById("pdf_cliente_cedula").value =
                cliente;

        });



});