console.log("Abrio mantenimiento    ");



$('#btnCrearBackup').on('click', function () {

    $.post('/admin?ruta=mantenimiento', {
        crear_backup: 1
    }, function (res) {

        Swal.fire({
            icon: res.icon,
            title: res.title,
            text: res.text,
            timer: 2000,
            showConfirmButton: true
        });

        if (res.icon === 'success') {
            $('#table1').load(location.href + ' #table1>*', '');
        }

    }, 'json');

});

let backupSeleccionado = '';

$('#modalRestaurarBackup').on('show.bs.modal', function (event) {
    backupSeleccionado = $(event.relatedTarget).data('file') || '';
});

$('#modalLimpiarSistema').on('show.bs.modal', function (event) {
    backupSeleccionado = $(event.relatedTarget).data('file') || '';
});

$('#formRestaurarBackup').on('submit', function (event) {
    event.preventDefault();

    $.ajax({
        url: '/admin?ruta=mantenimiento',
        method: 'POST',
        data: new FormData(this),
        processData: false,
        contentType: false,
        dataType: 'json',
        success: function (res) {
            Swal.fire({ icon: res.icon, title: res.title, text: res.text, timer: 2000, showConfirmButton: true });
            if (res.icon === 'success') {
                $('#formRestaurarBackup')[0].reset();
                $('#modalRestaurarBackup').modal('hide');
            }
        },
        error: function () {
            Swal.fire({ icon: 'error', title: 'Error', text: 'No se pudo conectar con el servidor.' });
        }
    });
});

function limpiarSistema() {
    $.post('/admin?ruta=mantenimiento', {
        eliminar_backup: 1,
        backup_name: backupSeleccionado
    }, function (res) {
        const mostrarResultado = function () {
            $('.modal-backdrop').remove();
            $('body').removeClass('modal-open');
            Swal.fire({
                icon: res.icon,
                title: res.title,
                text: res.text,
                timer: 2000,
                showConfirmButton: true,
                backdrop: false
            });
        };

        const modal = $('#modalLimpiarSistema');
        if (modal.length) {
            modal.one('hidden.bs.modal', mostrarResultado);
            modal.modal('hide');
        } else {
            mostrarResultado();
        }

        if (res.icon === 'success') {
            $('#table1').load(location.href + ' #table1>*', '');
        }
    }, 'json');
}

function descargarBackup(nombreArchivo) {
    window.location.href = '/admin/descargar-backup/' + nombreArchivo;
}