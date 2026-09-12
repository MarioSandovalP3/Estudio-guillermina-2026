console.log('Abrió misdatos.js');
document.addEventListener('DOMContentLoaded', function () {

    const regexLetras =
        /[^a-zA-ZÁÉÍÓÚáéíóúÑñ\s]/g;

    const regexDireccion =
        /[^a-zA-Z0-9ÁÉÍÓÚáéíóúÑñ\s.,#\-\/()]/g;

    const regexTelefono =
        /[^0-9]/g;
    const regexCorreoPermitido = /^[a-zA-Z0-9._%+-]+@(gmail|outlook|hotmail|yahoo)\.com$/;

    const modalEditarSesion =
        document.getElementById('modalEditarsecion');

    const formulario =
        $('#formEditarClientesecion');


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


    $('#formEditarClientesecion').on('submit', function (e) {

        e.preventDefault();

        if (!$(this).parsley().validate()) return;

        $.post('/admin?ruta=cliente', $(this).serialize(), function (res) {

            alerta(res).then(() => {

                if (res.icon === 'success') {

                    cerrarModal('#modalEditarsecion');

                    window.location.reload();

                }

            });

        }, 'json');

    });

    // =====================================================
    // INICIALIZAR PARSLEY
    // =====================================================

    if (formulario.length) {
        formulario.parsley({
            errorsContainer: function (field) {
                return field.$element
                    .closest('.col-md-6')
                    .find('.invalid-feedback');
            },
            errorClass: 'is-invalid',
            successClass: 'is-valid',
            errorsWrapper: false
        });

        formulario.parsley().on('field:error', function () {
            this.$element
                .removeClass('is-valid')
                .addClass('is-invalid');

            this.$element
                .closest('.col-md-6')
                .find('.invalid-feedback')
                .text(this.getErrorsMessages()[0])
                .show();
        });

        formulario.parsley().on('field:success', function () {
            this.$element
                .removeClass('is-invalid')
                .addClass('is-valid');

            this.$element
                .closest('.col-md-6')
                .find('.invalid-feedback')
                .text('')
                .hide();
        });
    }

    if (modalEditarSesion) {
        modalEditarSesion.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;

            document.getElementById('cedula_edit').value =
                button.getAttribute('data-cedula') || '';

            document.getElementById('nombre_usuario_edit').value =
                button.getAttribute('data-nombre') || '';

            document.getElementById('apellido_usuario_edit').value =
                button.getAttribute('data-apellido') || '';

            document.getElementById('telefono_edit').value =
                button.getAttribute('data-telefono') || '';

            document.getElementById('direccion_edit').value =
                button.getAttribute('data-direccion') || '';

            document.getElementById('correo_edit').value =
                button.getAttribute('data-correo') || '';

            document.getElementById('cod_rol_edit').value =
                button.getAttribute('data-rol') || '';

            if (formulario.length) {
                formulario.parsley().reset();

                formulario
                    .find('.form-control')
                    .removeClass('is-valid is-invalid');

                formulario
                    .find('.invalid-feedback')
                    .text('')
                    .hide();
            }
        });
    }

    $('#nombre_usuario_edit').on('input', function () {
        this.value = this.value.replace(regexLetras, '');
        $(this).parsley().validate();
    });

    $('#apellido_usuario_edit').on('input', function () {
        this.value = this.value.replace(regexLetras, '');
        $(this).parsley().validate();
    });

    $('#telefono_edit').on('input', function () {
        this.value = this.value.replace(regexTelefono, '');
        $(this).parsley().validate();
    });

    $('#direccion_edit').on('input', function () {
        this.value = this.value.replace(regexDireccion, '');
        $(this).parsley().validate();
    });

    $('#correo_edit').on('input', function () {
        const correo = this.value.trim();
        const regexCorreo = /^[a-zA-Z0-9._%+-]+@(gmail|outlook|hotmail|yahoo)\.com$/;
        const feedback = $(this)
            .closest('.col-md-6')
            .find('.invalid-feedback');

        if (correo === '') {
            $(this)
                .removeClass('is-invalid is-valid');

            feedback
                .text('')
                .hide();

        } else if (!regexCorreo.test(correo)) {
            $(this)
                .removeClass('is-valid')
                .addClass('is-invalid');

            feedback
                .text('Correo inválido. Use @gmail.com, @outlook.com, @hotmail.com o @yahoo.com.')
                .show();

        } else {
            $(this)
                .removeClass('is-invalid')
                .addClass('is-valid');

            feedback
                .text('')
                .hide();
        }

        $(this).parsley().validate();
    });



    $(document).on('input', '#formEditarClientesecion input[maxlength]', function () {
    const max = parseInt(this.getAttribute('maxlength'));
    let feedback = $(this).next('.invalid-feedback');

    if (!feedback.length) {
        feedback = $('<div class="invalid-feedback"></div>');
        $(this).after(feedback);
    }

    if (this.value.length >= max) {
        feedback.text('Límite de caracteres alcanzado');
        feedback.css({
            'display': 'block',
            'width': '100%'
        });

        $(this).addClass('is-invalid').removeClass('is-valid');
    } else {
        feedback.hide();
        $(this).removeClass('is-invalid');
    }
});
});





