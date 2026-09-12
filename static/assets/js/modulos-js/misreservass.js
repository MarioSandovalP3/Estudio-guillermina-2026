console.log("Abrio misresevas  ");
document.addEventListener('DOMContentLoaded', function () {


    const modalEliminar = document.getElementById('deleteModalReservas');

    if (modalEliminar) {
        modalEliminar.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;

            const codigo = button.getAttribute('data-codigo');
            const fecha_reserva = button.getAttribute('data-fecha_reserva');

            document.getElementById('delete_cod_servicio').value = codigo;
            document.getElementById('fecha_reserva_eliminar').textContent = fecha_reserva;
        });
    }

    function cerrarModal(idModal) {
        $(idModal).modal('hide');

        $(idModal).on('hidden.bs.modal', function () {
            $('.modal-backdrop').remove();
            $('body').removeClass('modal-open');
            $(this).off('hidden.bs.modal');
        });
    }

    function alerta(res) {
        return Swal.fire({
            icon: res.icon,
            title: res.title,
            text: res.text,
            showConfirmButton: true,
            confirmButtonText: 'Aceptar',
            timer: 2000,
            timerProgressBar: true,
            backdrop: false
        });
    }

    $('#formDeleteReserva').on('submit', function (e) {

        e.preventDefault();

        $.post('/admin?ruta=misreservas', $(this).serialize(), function (res) {

            alerta(res).then(() => {

                if (res.icon === 'success' || res.icon === 'warning') {

                    // LIMPIAR FORMULARIO
                    $('#formDeleteReserva')[0].reset();

                    // CERRAR MODAL
                    cerrarModal('#deleteModalReservas');

                    // RECARGAR TABLA
                    $('#table1').load(location.href + ' #table1>*', '');

                }

            });

        }, 'json');

    });

    // Captura el envío del formulario de cancelación
    $('#formDeleteReserva').on('submit', function (e) {
        e.preventDefault();

        $.ajax({
            url: 'index.php?pagina=misreservas',
            type: 'POST',
            dataType: 'json',
            data: $(this).serialize(),
            success: function (res) {
                Swal.fire({
                    icon: res.icon,
                    title: res.title,
                    text: res.text,
                    showConfirmButton: true,
                    confirmButtonText: 'Aceptar',
                    timer: 2000,
                    timerProgressBar: true
                }).then(() => {
                    // Cerrar modal
                    $('#deleteModalReservas').modal('hide');
                    if (res.icon === 'success') {
                      
                        $('#table1').load(location.href + ' #table1>*', '');

                    }
                });
            },

        });
    });

});