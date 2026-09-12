document.addEventListener("DOMContentLoaded", function () {

    const tabla = $('#tableBitacora').DataTable({
        language: {
            url: '//cdn.datatables.net/plug-ins/1.13.7/i18n/es-ES.json'
        },
        order: [[2, "desc"]]
    });

    // ==========================
    // FILTRAR
    // ==========================

    document.getElementById("btnFiltrar")
        .addEventListener("click", function () {

            const fecha = document.getElementById("filtro_fecha").value;
            const anio = document.getElementById("filtro_anio").value;

            $.fn.dataTable.ext.search.push(function (settings, data) {

                let fechaTabla = data[2];

                if (fecha) {

                    let fechaFormateada = fecha.split("-").reverse().join("/");

                    if (fechaTabla !== fechaFormateada) {
                        return false;
                    }
                }

                if (anio) {

                    if (!fechaTabla.includes(anio)) {
                        return false;
                    }
                }

                return true;
            });

            tabla.draw();

            $.fn.dataTable.ext.search.pop();

        });

    // ==========================
    // LIMPIAR
    // ==========================

    document.getElementById("btnLimpiar")
        .addEventListener("click", function () {

            document.getElementById("filtro_fecha").value = "";
            document.getElementById("filtro_anio").value = "";

            tabla.search("").columns().search("").draw();

        });

});