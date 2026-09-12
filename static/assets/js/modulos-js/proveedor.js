console.log("Abrió proveedores");

const regexTexto = /^[a-zA-ZÁÉÍÓÚáéíóúñÑ0-9@.\s]+$/;
const regexNoPermitidos = /[^a-zA-ZÁÉÍÓÚáéíóúñÑ0-9@.\s]/g;

$(document).ready(function () {

    // =====================================================
    // REGISTRAR PROVEEDOR
    // =====================================================
    $('#formRegistrarProveedor').on('submit', function (e) {
        e.preventDefault();

        if (!$(this).parsley().validate()) return;

        const form = this;
        const btn = $(form).find('button[type="submit"]');

        btn.prop('disabled', true);

        const cedula = $('#cedula').val().trim();
        const nombre = $('#nombre').val().trim();

        if (!regexTexto.test(nombre)) {
            $('#nombre').addClass('is-invalid');

            if ($('#nombre').next('.invalid-feedback').length === 0) {
                $('#nombre').after('<div class="invalid-feedback">Nombre inválido.</div>');
            } else {
                $('#nombre').next('.invalid-feedback')
                    .text('Nombre inválido.')
                    .show();
            }

            btn.prop('disabled', false);
            return;
        }

        $.post('/admin?ruta=proveedor', $(form).serialize(), function (res) {

            alerta(res).then(() => {

                if (res.icon === 'success') {

                    form.reset();
                    $(form).parsley().reset();

                    cerrarModal('#modalRegistrar');

                    $('#table1').load(location.href + ' #table1>*', '');
                }

                btn.prop('disabled', false);
            });

        }, 'json');
    });

    // =====================================================
    // EDITAR PROVEEDOR
    // =====================================================
    $('#formEditarProveedor').on('submit', function (e) {
        e.preventDefault();

        const form = this;
        const btn = $(form).find('button[type="submit"]');

        btn.prop('disabled', true);

        const nombre = $('#edit_nombre').val().trim();

        if (!regexTexto.test(nombre)) {
            $('#edit_nombre').addClass('is-invalid');

            if ($('#edit_nombre').next('.invalid-feedback').length === 0) {
                $('#edit_nombre').after('<div class="invalid-feedback">Nombre inválido.</div>');
            } else {
                $('#edit_nombre').next('.invalid-feedback')
                    .text('Nombre inválido.')
                    .show();
            }

            btn.prop('disabled', false);
            return;
        }

        $.post('/admin?ruta=proveedor', $(form).serialize(), function (res) {

            alerta(res).then(() => {

                if (res.icon === 'success') {

                    form.reset();

                    $('#modalEditar .invalid-feedback').hide();
                    $('#modalEditar .is-invalid, #modalEditar .is-valid')
                        .removeClass('is-invalid is-valid');

                    cerrarModal('#modalEditar');

                    $('#table1').load(location.href + ' #table1>*', '');
                }

                btn.prop('disabled', false);
            });

        }, 'json');
    });

    // =====================================================
    // ELIMINAR PROVEEDOR
    // =====================================================
    $('#formEliminarProveedor').on('submit', function (e) {
        e.preventDefault();

        $.post('/admin?ruta=proveedor', $(this).serialize(), function (res) {

            alerta(res).then(() => {

                cerrarModal('#modalEliminar');

                if (res.icon === 'success') {
                    $('#table1').load(location.href + ' #table1>*', '');
                }
            });

        }, 'json');
    });

    // =====================================================
    // BLOQUEO DE CARACTERES
    // =====================================================
    $('#formRegistrarProveedor input, #formEditarProveedor input').on('input', function () {

        const originalValue = this.value;

        this.value = this.value.replace(regexNoPermitidos, '');

        if (this.value !== originalValue) {
            $(this).addClass('is-invalid').removeClass('is-valid');

            if ($(this).next('.invalid-feedback').length === 0) {
                $(this).after('<div class="invalid-feedback">Entrada no válida.</div>');
            } else {
                $(this).next('.invalid-feedback')
                    .text('Entrada no válida.')
                    .show();
            }
        } else {
            $(this).removeClass('is-invalid');
            $(this).parsley().validate();
        }
    });

    // =====================================================
    // CERRAR MODALES
    // =====================================================
    function cerrarModal(id) {
        $(id).modal('hide');

        $(id).on('hidden.bs.modal', function () {
            $('.modal-backdrop').remove();
            $('body').removeClass('modal-open');
            $(this).off('hidden.bs.modal');
        });
    }

    // =====================================================
    // ALERTA SWAL
    // =====================================================
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

    // =====================================================
    // MODAL EDITAR
    // =====================================================
    const modalEditar = document.getElementById('modalEditar');

    if (modalEditar) {
        modalEditar.addEventListener('show.bs.modal', function (event) {

            const button = event.relatedTarget;

            const cod = button.getAttribute('data-cod_proveedor');
            const cedula = button.getAttribute('data-cedula');
            const nombre = button.getAttribute('data-nombre');
            const apellido = button.getAttribute('data-apellido');
            const rif = button.getAttribute('data-rif');
            const telefono = button.getAttribute('data-telefono');
            const correo = button.getAttribute('data-correo');
            const status = button.getAttribute('data-status');

            const form = modalEditar.querySelector('form');

            if (form) {
                form.querySelector('#edit_cod_proveedor').value = cod;
                form.querySelector('#edit_cedula').value = cedula;
                form.querySelector('#edit_nombre').value = nombre;
                form.querySelector('#edit_apellido').value = apellido;
                form.querySelector('#edit_rif').value = rif;
                form.querySelector('#edit_telefono').value = telefono;
                form.querySelector('#edit_correo').value = correo;
                form.querySelector('#edit_status').value = status;
            }
        });
    }

    // =====================================================
    // MODAL ELIMINAR
    // =====================================================
    const modalEliminar = document.getElementById('modalEliminar');

    if (modalEliminar) {
        modalEliminar.addEventListener('show.bs.modal', function (event) {

            const button = event.relatedTarget;

            const cod = button.getAttribute('data-cod_proveedor');

            const form = document.getElementById('formEliminarProveedor');

            if (form) {
                form.querySelector('#delete_cod_proveedor').value = cod;
            }
        });
    }

    // =====================================================
    // PARSLEY VALIDACIÓN
    // =====================================================
    window.Parsley.on('field:error', function () {
        this.$element.addClass('is-invalid').removeClass('is-valid');
    });

    window.Parsley.on('field:success', function () {
        this.$element.removeClass('is-invalid').addClass('is-valid');
    });

});