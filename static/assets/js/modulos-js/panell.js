console.log("Panel cargado correctamente.");

let chartReservas = null;
let graficoIngresos = null;


document.addEventListener("DOMContentLoaded", () => {

    const reservasMes = window.reservasMes || [];
    const reservasDia = window.reservasDia || [];

    const ingresosMes = window.ingresosMes || [];
    const ingresosDia = window.ingresosDia || [];


    // ==========================
    // CONTADORES KPI
    // ==========================

    document.querySelectorAll('.counter').forEach(c => {

        let target = Number(c.dataset.target);

        if (isNaN(target)) {
            return;
        }

        let count = 0;


        function actualizarContador() {

            let incremento = Math.ceil(target / 50);

            count += incremento;


            if (count < target) {

                c.innerText = count;

                setTimeout(actualizarContador, 20);

            } else {

                c.innerText = target;

            }

        }


        actualizarContador();

    });



    // ==========================
    // GRAFICO RESERVAS
    // ==========================


    const contenedorReservas = document.querySelector("#chart-reservas");

    const filtroReservas = document.querySelector("#filtroReservas");


    if (contenedorReservas) {


        const categoriasMes = [
            "Ene", "Feb", "Mar", "Abr",
            "May", "Jun", "Jul", "Ago",
            "Sep", "Oct", "Nov", "Dic"
        ];


        const datosMes = reservasMes.map(item =>
            Number(item.total_reservas)
        );


        const categoriasDia = reservasDia.map(item =>
            item.dia
        );


        const datosDia = reservasDia.map(item =>
            Number(item.total_reservas)
        );


        function cargarGraficoReservas(tipo = "mes") {


            if (chartReservas) {

                chartReservas.destroy();

            }


            let categorias;
            let datos;


            if (tipo === "mes") {

                categorias = categoriasMes;
                datos = datosMes;

            } else {

                categorias = categoriasDia;
                datos = datosDia;

            }


            chartReservas = new ApexCharts(

                contenedorReservas,

                {

                    series: [{
                        name: "Reservas",
                        data: datos
                    }],


                    chart: {

                        type: tipo === "mes" ? "bar" : "line",

                        height: 320,

                        toolbar: {
                            show: false
                        }

                    },


                    colors: ["#0d6efd"],


                    plotOptions: {

                        bar: {

                            borderRadius: 8,

                            columnWidth: "45%"

                        }

                    },


                    stroke: {

                        curve: "smooth",

                        width: 4

                    },


                    markers: {

                        size: tipo === "mes" ? 0 : 6

                    },


                    dataLabels: {

                        enabled: true,

                        formatter: function (valor) {

                            return Math.round(valor);

                        }

                    },


                    xaxis: {

                        categories: categorias

                    },


                    // ==========================================
                    // EJE Y - SOLO VALORES ENTEROS
                    // ==========================================

                    yaxis: {

                        min: 0,

                        forceNiceScale: false,

                        decimalsInFloat: 0,

                        labels: {

                            formatter: function (valor) {

                                return Math.round(valor);

                            }

                        }

                    },


                    tooltip: {

                        y: {

                            formatter: function (valor) {

                                return Math.round(valor) + " reservas";

                            }

                        }

                    }


                }

            );


            chartReservas.render();

        }


        cargarGraficoReservas("mes");


        if (filtroReservas) {

            filtroReservas.addEventListener("change", function () {

                cargarGraficoReservas(this.value);

            });

        }


    }


    // ==========================
    // GRAFICO INGRESOS
    // ==========================

    const contenedorIngresos = document.querySelector("#chart-ingresos");

    if (contenedorIngresos) {

        function cargarGraficoIngresos(tipo = "mes") {

            let datos = tipo === "mes" ? ingresosMes : ingresosDia;

            let categorias = [];
            let valores = [];

            datos.forEach(item => {

                categorias.push(
                    tipo === "mes"
                        ? item.mes
                        : `${item.dia} - ${item.fecha.substring(8, 10)}/${item.fecha.substring(5, 7)}`
                );

                valores.push(
                    Number(item.total_ingresos)
                );

            });

            if (graficoIngresos) {
                graficoIngresos.destroy();
            }

            graficoIngresos = new ApexCharts(
                contenedorIngresos,
                {

                    chart: {
                        type: "bar",
                        height: 350
                    },

                    series: [{
                        name: "Ingresos",
                        data: valores
                    }],

                    xaxis: {
                        categories: categorias
                    },

                    dataLabels: {
                        enabled: true,
                        formatter: function (valor) {
                            return "$" + Number(valor).toFixed(2);
                        }
                    },

                    yaxis: {
                        labels: {
                            formatter: function (valor) {
                                return "$" + Number(valor).toFixed(2);
                            }
                        }
                    },

                    tooltip: {
                        y: {
                            formatter: function (valor) {
                                return "$" + Number(valor).toFixed(2);
                            }
                        }
                    }

                }
            );

            graficoIngresos.render();
        }

        cargarGraficoIngresos("mes");

        const filtroIngresos = document.querySelector("#filtroIngresos");

        if (filtroIngresos) {

            filtroIngresos.addEventListener(
                "change",
                function () {

                    cargarGraficoIngresos(this.value);

                }
            );

        }

    }




    // ==========================
    // GRAFICO servicios populares
    // ==========================
    const contenedorServicios =
        document.querySelector("#chart-servicios");

    let graficoServicios = null;

    if (contenedorServicios) {

        function cargarGraficoServicios() {

            let categorias = [];
            let valores = [];

            serviciosPopulares.forEach(item => {

                categorias.push(item.nombre_servicio);

                valores.push(
                    Number(item.cantidad_reservas)
                );

            });

            if (graficoServicios) {
                graficoServicios.destroy();
            }

            graficoServicios = new ApexCharts(
                contenedorServicios,
                {

                    chart: {
                        type: "donut",
                        height: 350
                    },

                    series: valores,

                    labels: categorias,

                    dataLabels: {
                        enabled: true
                    },

                    legend: {
                        position: "bottom"
                    },

                    tooltip: {
                        y: {
                            formatter: function (valor) {
                                return valor + " reservas";
                            }
                        }
                    }

                }
            );

            graficoServicios.render();
        }

        cargarGraficoServicios();
    }





    const contenedorInventario = document.querySelector("#chart-inventario");
    const productosStock = window.productosStock || [];

    if (contenedorInventario) {
        contenedorInventario.innerHTML = "";

        productosStock.forEach(item => {
            const stockItem = document.createElement("div");

            stockItem.className = "stock-item d-flex justify-content-between align-items-center";

            stockItem.innerHTML = `
            <span>${item.nombre_producto}</span>
            <span>${Number(item.stock)}</span>
        `;

            contenedorInventario.appendChild(stockItem);
        });
    }
});


