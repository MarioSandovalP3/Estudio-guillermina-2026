console.log("JS registro cliente ");

// ===============================
// EXPRESIONES REGULARES
// ===============================
const regexLetras = /[^a-zA-ZÁÉÍÓÚáéíóúñÑ\s]/;
const regexDireccion = /[^a-zA-Z0-9ÁÉÍÓÚáéíóúÑñ\s.,#\-\/()]/;
const regexNumeros = /[^0-9]/;
const regexCorreoPermitido = /^[a-zA-Z0-9._%+-]+@(gmail|outlook|hotmail|yahoo)\.com$/;

$(document).ready(function () {

$('#formRegistrarCliente').parsley();

$('#formRegistrarCliente input').on('input', function () {
    const name = this.name;
    const valor = this.value;
    let mensaje = '';
    let invalido = false;

    if (name === 'cedula' || name === 'telefono') {
        if (regexNumeros.test(valor)) {
            invalido = true;
            mensaje = "Solo se permiten números.";
        }
        this.value = valor.replace(/[^\d]/g, '');
        if (name === 'cedula' && this.value.length > 10) {
            this.value = this.value.slice(0, 10);
        }
    }

    if (name === 'nombre_usuario' || name === 'apellido_usuario') {
        if (regexLetras.test(valor)) {
            invalido = true;
            mensaje = "Solo se permiten letras.";
        }
        this.value = valor.replace(/[^a-zA-ZÁÉÍÓÚáéíóúñÑ\s]/g, '');
    }

    if (name === 'direccion') {
        if (regexDireccion.test(valor)) {
            invalido = true;
            mensaje = "Solo se permiten letras, números y signos básicos.";
        }
        this.value = valor.replace(/[^a-zA-Z0-9ÁÉÍÓÚáéíóúÑñ\s.,#\-\/()]/g, '');
    }

    if (name === 'correo') {
        const regexCorreo = /^[a-zA-Z0-9._%+-]+@(gmail|outlook|hotmail|yahoo)\.com$/;

        if (valor !== '' && !regexCorreo.test(valor)) {
            invalido = true;
            mensaje = "Correo inválido. Use @gmail.com, @outlook.com, @hotmail.com o @yahoo.com.";
        }
    }

    if (invalido) {
        $(this).addClass('is-invalid').removeClass('is-valid');

        if ($(this).next('.invalid-feedback').length === 0) {
            $(this).after('<div class="invalid-feedback"></div>');
        }

        $(this).next('.invalid-feedback').text(mensaje).show();
    } else {
        $(this).removeClass('is-invalid').addClass('is-valid');
        $(this).next('.invalid-feedback').hide();
    }

    $(this).parsley().validate();
});

    // ===============================
    // VALIDAR CÉDULA DUPLICADA
    // ===============================
    $('#cedula_reg').blur(function () {

        let buscar = $(this).val();

        if (buscar === '') return;

        $.post('/admin?ruta=cliente',
            { buscar: buscar },
            function (response) {

                if (response.existe === true) {

                    Swal.fire({
                        title: 'Advertencia',
                        text: 'El cliente ya se encuentra registrado',
                        icon: 'warning'
                    });

                    $('#cedula_reg').val('').focus();
                }
            },
            'json'
        );
    });

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

    // ===============================
    // ENVIAR FORMULARIO
    // ===============================
    $('#formRegistrarCliente').on('submit', function (e) {

        e.preventDefault();

        if (!$('#formRegistrarCliente').parsley().validate()) return;

        $.ajax({
            url: '/admin?ruta=cliente',
            type: 'POST',
            data: $(this).serialize(),
            dataType: 'json',

            success: function (res) {

                console.log(res);

                Swal.fire({
                    icon: res.icon,
                    title: res.title,
                    text: res.text
                });

                if (res.icon === 'success') {

                    $('#formRegistrarCliente')[0].reset();
                    $('#formRegistrarCliente').parsley().reset();

                    setTimeout(() => {
                        $('#modalRegistrarCliente').modal('hide');
                    }, 1000);
                }
            },

            error: function (xhr) {
                console.log("ERROR:");
                console.log(xhr.responseText);
            }
        });

    });


    // ===============================
    // LIMPIAR MODAL AL CERRAR
    // ===============================
    $('#modalRegistrarCliente').on('hidden.bs.modal', function () {

        const form = $('#formRegistrarCliente');

        form[0].reset();

        form.find('.is-invalid, .is-valid').removeClass('is-invalid is-valid');

        form.find('.invalid-feedback').hide();

        form.parsley().reset();

    });

});