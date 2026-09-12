console.log("Abrio personal");

// =====================================================
// 🔠 EXPRESIONES REGULARES
// =====================================================
const regexNoPermitidosLetras = /[^a-zA-ZÁÉÍÓÚáéíóúñÑ\s]/g;
const regexNoPermitidosDireccion = /[^a-zA-Z0-9ÁÉÍÓÚáéíóúÑñ\s.,#\-\/()]/g;
const regexNoPermitidosPassword = /[^a-zA-Z0-9.,;:!¡¿?!@#$%^&*()\/,.?"'()\-_\s]/g;
const regexSoloLetrasPersonal = /^[a-zA-ZÁÉÍÓÚáéíóúñÑ\s]+$/;

document.addEventListener('DOMContentLoaded', function () {

    function recargarTablaPersonal() {
        $('#table1').load(location.href + ' #table1>*', function () {
            if ($.fn.DataTable.isDataTable('#table1')) {
                $('#table1').DataTable().destroy();
            }
            $('#table1').DataTable({
                responsive: true,
                language: {
                    url: '//cdn.datatables.net/plug-ins/1.13.7/i18n/es-ES.json'
                }
            });
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

    $('#formRegistrarPersonal').on('submit', function (e) {
        e.preventDefault();
        if (!$(this).parsley().validate()) return;

        var url = $(this).attr('action') || '/admin?ruta=personal';

        $.post(url, $(this).serialize(), function (res) {
            alerta(res).then(function () {
                if (res.icon === 'success') {
                    $('#formRegistrarPersonal')[0].reset();
                    $('#formRegistrarPersonal').parsley().reset();
                    cerrarModal('#modalRegistrarPersonal');
                    recargarTablaPersonal();
                }
            });
        }, 'json');
    });

    $('#formRegistrarPersonal input[name="nombre_usuario"], #formRegistrarPersonal input[name="apellido_usuario"], #formEditarPersonal input[name="nombre_usuario"], #formEditarPersonal input[name="apellido_usuario"]').on('input', function () {
        validarNombrePersonal(this);
    });

    function validarNombrePersonal(input) {
        const originalValue = input.value;
        input.value = input.value.replace(regexNoPermitidosLetras, '');
        const maxLen = parseInt(input.getAttribute('maxlength') || '0', 10);
        let feedback = $(input).next('.invalid-feedback');
        if (!feedback.length) {
            feedback = $('<div class="invalid-feedback"></div>');
            $(input).after(feedback);
        }

        if (maxLen > 0 && input.value.length >= maxLen) {
            feedback.text('limite de caracteres alcanzado').show();
            $(input).addClass('is-invalid').removeClass('is-valid');
            return;
        }

        if (input.value !== originalValue || !regexSoloLetrasPersonal.test(input.value)) {
            feedback.text('En este campo solo se permiten letras.').show();
            $(input).addClass('is-invalid').removeClass('is-valid');
        } else {
            feedback.hide();
            $(input).parsley().validate();
        }
    }

    $('#correo_reg, #correo_edit').on('input', function () {
        const correo = this.value.trim();
        const regexCorreo = /^[a-zA-Z0-9._%+-]+@(gmail|outlook|hotmail|yahoo)\.com$/;

        if (correo === '') {
            $(this).removeClass('is-invalid is-valid');
            if ($(this).next('.invalid-feedback').length === 0) {
                $(this).after('<div class="invalid-feedback"></div>');
            }
            $(this).next('.invalid-feedback').hide();
            return;
        }

        if (!regexCorreo.test(correo)) {
            if ($(this).next('.invalid-feedback').length === 0) {
                $(this).after('<div class="invalid-feedback"></div>');
            }
            $(this).removeClass('is-valid').addClass('is-invalid');
            $(this).next('.invalid-feedback').text('Ingrese un correo válido como gmail.com, outlook.com, hotmail.com o yahoo.com').show();
        } else {
            $(this).removeClass('is-invalid').addClass('is-valid');
            $(this).next('.invalid-feedback').hide();
        }
    });

    $('#formEditarPersonal').on('submit', function (e) {
        e.preventDefault();
        if (!$(this).parsley().validate()) return;

        var url = $(this).attr('action') || '/admin?ruta=personal';

        $.post(url, $(this).serialize(), function (res) {
            alerta(res).then(function () {
                if (res.icon === 'success') {
                    $('#formEditarPersonal')[0].reset();
                    $('#formEditarPersonal').parsley().reset();
                    cerrarModal('#modalEditar');
                    recargarTablaPersonal();
                }
            });
        }, 'json');
    });

    $('#formEliminarPersonal').on('submit', function (e) {
        e.preventDefault();

        var url = $(this).attr('action') || '/admin?ruta=personal';

        $.post(url, $(this).serialize(), function (res) {
            alerta(res).then(function () {
                if (res.icon === 'success') {
                    $('#formEliminarPersonal')[0].reset();
                    cerrarModal('#modalEliminarPersonal');
                    recargarTablaPersonal();
                }
            });
        }, 'json');
    });

    $('#btnCerrarModal').on('click', function () {
        $('#modalRegistrarPersonal').find('form')[0].reset();
        $('#modalRegistrarPersonal').find('.is-invalid, .is-valid').removeClass('is-invalid is-valid');
        $('#modalRegistrarPersonal').find('.invalid-feedback').hide();
        $('#modalRegistrarPersonal').find('form').parsley().reset();
    });

    $('#btnCerrar, #btnClose').on('click', function () {
        $('#modalEditar').find('.is-invalid, .is-valid').removeClass('is-invalid is-valid');
        $('#modalEditar').find('.invalid-feedback').hide();
    });

    const modalEditar = document.getElementById('modalEditar');

    modalEditar.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const fila = button.closest('tr');
        const celdas = fila.querySelectorAll('td');
        const form = modalEditar.querySelector('#formEditarPersonal');

        form.querySelector('#cedula_edit').value = celdas[0].innerText.trim();
        form.querySelector('#nombre_usuario_edit').value = celdas[1].innerText.trim();
        form.querySelector('#apellido_usuario_edit').value = celdas[2].innerText.trim();
        form.querySelector('#telefono_edit').value = celdas[3].innerText.trim();
        form.querySelector('#direccion_edit').value = celdas[4].innerText.trim();
        form.querySelector('#correo_edit').value = celdas[5].innerText.trim();

        const status = celdas[6].dataset.status;
        form.querySelector('#status_edit').value = status;
        form.querySelector('#cod_rol_edit').value = button.getAttribute('data-rol');
    });

    const modalEliminar = document.getElementById('modalEliminarPersonal');

    modalEliminar.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const form = modalEliminar.querySelector('#formEliminarPersonal');
        form.querySelector('#cedula_eliminar').value = button.getAttribute('data-cedula');
        document.getElementById('nombre_usuario_elim').innerText = button.getAttribute('data-nombre');
    });

    $('#formRegistrarPersonal, #formEditarPersonal').parsley();

    $('#formRegistrarPersonal input, #formEditarPersonal input').on('input', function () {
        const name = this.name;
        const originalValue = this.value;

        if (name === 'cedula' || name === 'telefono') {
            this.value = this.value.replace(/[^\d]/g, '');
            if (name === 'cedula' && this.value.length > 10) this.value = this.value.slice(0, 10);
        } else if (name === 'nombre_usuario' || name === 'apellido_usuario') {
            this.value = this.value.replace(regexNoPermitidosLetras, '');
        } else if (name === 'direccion') {
            this.value = this.value.replace(regexNoPermitidosDireccion, '');
        } else if (name === 'correo') {
            const correo = this.value.trim();
            const regexCorreo = /^[a-zA-Z0-9._%+-]+@(gmail|outlook|hotmail|yahoo)\.com$/;
            if (correo === '') {
                $(this).removeClass('is-invalid is-valid');
                $(this).next('.invalid-feedback').hide();
                return;
            }
            if (!regexCorreo.test(correo)) {
                $(this).addClass('is-invalid').removeClass('is-valid');
                if ($(this).next('.invalid-feedback').length === 0) {
                    $(this).after('<div class="invalid-feedback"></div>');
                }
                $(this).next('.invalid-feedback').text('Ingrese un correo válido como gmail.com, outlook.com, hotmail.com o yahoo.com').show();
                return;
            }
            $(this).removeClass('is-invalid').addClass('is-valid');
            $(this).next('.invalid-feedback').hide();
        } else if (name === 'password_reg' || name === 'password_edit') {
            this.value = this.value.replace(regexNoPermitidosPassword, '');
        }

        // Comprueba si supera maxlength (por ejemplo al pegar)
        const maxAttr = this.getAttribute && this.getAttribute('maxlength');
        const maxLen = maxAttr ? parseInt(maxAttr, 10) : 0;

        if (maxLen > 0 && this.value.length >= maxLen) {
            if ($(this).next('.invalid-feedback').length === 0) {
                $(this).after('<div class="invalid-feedback"></div>');
            }
            $(this).addClass('is-invalid').removeClass('is-valid');
            $(this).next('.invalid-feedback').text('limite de caracteres alcanzado').show();
            $(this).parsley().validate();
            return;
        }

        if (this.value !== originalValue) {
            $(this).addClass('is-invalid').removeClass('is-valid');
            if ($(this).next('.invalid-feedback').length === 0) {
                $(this).after('<div class="invalid-feedback"></div>');
            }
            let mensaje = 'Caracter no permitido.';
            if (name === 'cedula' || name === 'telefono') mensaje = 'Solo se permiten números.';
            else if (name === 'nombre_usuario' || name === 'apellido_usuario') mensaje = 'Solo se permiten letras.';
            else if (name === 'direccion') mensaje = 'Solo se permiten letras, números y signos básicos.';
            else if (name === 'password_reg' || name === 'password_edit') mensaje = 'Caracter no permitido en la contraseña.';
            $(this).next('.invalid-feedback').text(mensaje).show();
        } else {
            $(this).removeClass('is-invalid').addClass('is-valid');
            $(this).next('.invalid-feedback').hide();
        }

        $(this).parsley().validate();
    });

    $('#cedula_reg').blur(function () {
        let buscar = $(this).val();
        if (buscar === '') return;
        $.post('/admin?ruta=personal', { buscar: buscar }, function (response) {
            if (response.existe === true) {
                Swal.fire({
                    title: 'Advertencia',
                    text: 'El personal ya se encuentra registrado',
                    icon: 'warning'
                });
                $('#cedula_reg').val('').focus();
            }
        }, 'json');
    });

    $('#formPDF').on('submit', function (e) {
        e.preventDefault();
        window.open($(this).attr('action'), '_blank');
        Swal.fire({
            title: 'Éxito',
            text: 'Reporte generado correctamente.',
            icon: 'success',
            confirmButtonColor: '#3085d6'
        });
    });

});


