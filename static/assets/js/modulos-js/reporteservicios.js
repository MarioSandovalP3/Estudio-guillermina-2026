document.addEventListener('DOMContentLoaded', function() {
    const filtroInicio = document.getElementById('filtroInicio');
    const filtroFin = document.getElementById('filtroFin');
    const filtroCedula = document.getElementById('filtroCedula');
    const status = document.getElementById('status');
    const btnLimpiar = document.getElementById('btnLimpiar');
    const filas = document.querySelectorAll('#tablaservicios tr');

    // Función de filtrado visual de la tabla
    function filtrarTabla() {
        const inicio = filtroInicio.value ? new Date(filtroInicio.value) : null;
        const fin = filtroFin.value ? new Date(filtroFin.value) : null;
        const cedulaVal = filtroCedula.value.trim().toLowerCase();
        const statusVal = status.value;

        filas.forEach(fila => {
            // Fecha (dd/mm/yyyy) -> Date
            const fechaTexto = fila.children[5].textContent.trim();
            const parts = fechaTexto.split('/');
            const fecha = new Date(parts[2], parts[1]-1, parts[0]);

            const filaCedula = fila.children[0].textContent.trim().toLowerCase();
            const filaStatus = fila.children[7].textContent.trim().toLowerCase();

            let visible = true;
            if (inicio && fecha < inicio) visible = false;
            if (fin && fecha > fin) visible = false;
            if (cedulaVal && !filaCedula.includes(cedulaVal)) visible = false;
            if (statusVal !== 'all') {
                if (statusVal === 'active' && filaStatus !== 'activo') visible = false;
                if (statusVal === 'anulado' && filaStatus !== 'cancelado') visible = false;
            }

            fila.style.display = visible ? '' : 'none';
        });
    }

    // Limpiar filtros
    btnLimpiar.addEventListener('click', function(e) {
        e.preventDefault();
        filtroInicio.value = '';
        filtroFin.value = '';
        filtroCedula.value = '';
        status.value = 'all';
        filas.forEach(fila => fila.style.display = '');
    });

    filtroInicio.addEventListener('change', filtrarTabla);
    filtroFin.addEventListener('change', filtrarTabla);
    filtroCedula.addEventListener('input', filtrarTabla);
    status.addEventListener('change', filtrarTabla);

    // Formularios PDF/Excel
    const formPDFHeader = document.getElementById('formPDFHeader');
    const formExcelHeader = document.getElementById('formExcelHeader');
    const btnHeaderPDF = document.getElementById('btnHeaderPDF');
    const btnHeaderExcel = document.getElementById('btnHeaderExcel');

    function copyFiltersTo(form) {
        form.innerHTML = '';
        const filtros = [filtroInicio, filtroFin, filtroCedula, status];
        filtros.forEach(el => {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = el.name;
            input.value = el.value;
            form.appendChild(input);
        });
    }

    btnHeaderPDF.addEventListener('click', function(e){
        e.preventDefault();
        copyFiltersTo(formPDFHeader);
        formPDFHeader.submit();
    });

    btnHeaderExcel.addEventListener('click', function(e){
        e.preventDefault();
        copyFiltersTo(formExcelHeader);
        formExcelHeader.submit();
    });
});