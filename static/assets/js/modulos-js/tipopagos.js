console.log('Abrió tipo.js');


const regexTipoPago = /^[a-zA-ZÁÉÍÓÚáéíóúñÑ\s]+$/;
const regexNoPermitidos = /[^a-zA-ZÁÉÍÓÚáéíóúñÑ\s]/g;

$(document).ready(function () {

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


    // =====================================================
    // 🟢 REGISTRAR TIPO DE PAGO
    // =====================================================
    $('#primary').on('show.bs.modal', function () {
        $('#formTipoPago')[0].reset();
        $('#formTipoPago').parsley().reset();
    });


    // ===============================
    // registar 
    // ===============================
    $('#formTipoPago').on('submit', function (e) {

        e.preventDefault();

        // Validación Parsley
        if (!$('#formTipoPago').parsley().validate()) return;

        // Validación regex
        const nombreTipoPago = $('#nombre_tipo_pago').val();

        if (!regexTipoPago.test(nombreTipoPago)) {

            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'El tipo de pago solo puede contener letras. No se permiten números.'
            });

            return;
        }

        $.post('/admin?ruta=tipopagos', $(this).serialize(), function (res) {

            alerta(res).then(() => {

                if (res.icon === 'success') {

                    // Limpiar formulario
                    $('#formTipoPago')[0].reset();

                    // Limpiar Parsley
                    $('#formTipoPago').parsley().reset();

                    // Limpiar clases de validación
                    $('#primary .is-invalid, #primary .is-valid')
                        .removeClass('is-invalid is-valid');

                    // Cerrar modal
                    cerrarModal('#primary');

                    // Recargar tabla
                    $('#table1').load(location.href + ' #table1>*', '');

                }

            });

        }, 'json');

    });

    // =====================================================
    // 🟡 EDITAR TIPO DE PAGO
    // =====================================================

    $('#formEditTipoPago').on('submit', function (e) {

        e.preventDefault();

        const nombreTipoPago = $('#edit_nombre_tipo_pago').val();

        if (!regexTipoPago.test(nombreTipoPago)) {

            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'El tipo de pago solo puede contener letras. No se permiten números.'
            });

            return;
        }

        $.post('/admin?ruta=tipopagos', $(this).serialize(), function (res) {

            alerta(res).then(() => {

                if (res.icon === 'success') {

                    // LIMPIAR FORMULARIO
                    $('#formEditTipoPago')[0].reset();

                    // LIMPIAR CLASES DE VALIDACIÓN
                    $('#editModal .is-invalid, #editModal .is-valid')
                        .removeClass('is-invalid is-valid');


                    $('#formEditTipoPago').parsley().reset();

                    // CERRAR MODAL
                    cerrarModal('#editModal');

                    // RECARGAR TABLA
                    $('#table1').load(location.href + ' #table1>*', '');

                }

            });

        }, 'json');

    });


    // =====================================================
    // 🔴 ELIMINAR TIPO DE PAGO
    // =====================================================
    $('#elimodal').on('submit', function (e) {

        e.preventDefault();

        $.post('/admin?ruta=tipopagos', $(this).serialize(), function (res) {

            alerta(res).then(() => {

                if (res.icon === 'success' || res.icon === 'warning') {

                    // LIMPIAR FORMULARIO
                    $('#elimodal')[0].reset();

                    // CERRAR MODAL
                    cerrarModal('#deleteModal');

                    // RECARGAR TABLA
                    $('#table1').load(location.href + ' #table1>*', '');

                }

            });

        }, 'json');

    });

    // =====================================================
    // 🔡 VALIDACIÓN Y PARSLEY PERSONALIZADA
    // =====================================================
    $('#formTipoPago').parsley().on('form:submit', function () {
        const nombreTipoPago = $('#nombre_tipo_pago').val();
        if (!regexTipoPago.test(nombreTipoPago)) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'El tipo de pago solo puede contener letras. No se permiten números.'
            });
            return false;
        }
    });

    $('#formEditTipoPago').parsley().on('form:submit', function () {
        const nombreTipoPago = $('#edit_nombre_tipo_pago').val();
        if (!regexTipoPago.test(nombreTipoPago)) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'El tipo de pago solo puede contener letras. No se permiten números.'
            });
            return false;
        }
    });

    // Bloqueo de caracteres
    $('#formTipoPago input, #formEditTipoPago input').on('input', function () {
        validateInput(this);
    });

    function validateInput(input) {
        const originalValue = input.value;
        input.value = input.value.replace(regexNoPermitidos, '');
        // Chequear maxlength 
        const maxAttr = input.getAttribute && input.getAttribute('maxlength');
        const maxLen = maxAttr ? parseInt(maxAttr, 10) : 0;
        if (maxLen > 0 && input.value.length >= maxLen) {
            if ($(input).next('.invalid-feedback').length === 0) {
                $(input).after('<div class="invalid-feedback"></div>');
            }
            $(input).next('.invalid-feedback').text('limite de caracteres alcanzado').show();
            $(input).addClass('is-invalid').removeClass('is-valid');
            return;
        }

        if (input.value !== originalValue) {
            $(input).next('.invalid-feedback').text('En este campo solo se permiten letras.').show();
            $(input).addClass('is-invalid').removeClass('is-valid');
        } else {
            $(input).parsley().validate();
        }
    }

    // =====================================================
    // 🔁 RESETEO DE FORMULARIOS Y VALIDACIÓN VISUAL
    // =====================================================
    $('#btnCerrarModal').on('click', function () {
        $('#formTipoPago')[0].reset();
        $('#formTipoPago').find('.is-invalid').removeClass('is-invalid');
        $('#formTipoPago').find('.is-valid').removeClass('is-valid');
        $('#formTipoPago').find('.invalid-feedback').hide();
        $('#formTipoPago').parsley().reset();
    });

    $('#btnCerrar, #btnClose').on('click', function () {
        $('#formEditTipoPago').find('.is-invalid').removeClass('is-invalid');
        $('#formEditTipoPago').find('.is-valid').removeClass('is-valid');
        $('#formEditTipoPago').find('.invalid-feedback').hide();
    });

    window.Parsley.on('field:error', function () {
        this.$element.addClass('is-invalid');
        this.$element.removeClass('is-valid');
        this.$element.next('.invalid-feedback').show();
    });

    window.Parsley.on('field:success', function () {
        this.$element.removeClass('is-invalid');
        this.$element.addClass('is-valid');
        this.$element.next('.invalid-feedback').hide();
    });

    // =====================================================
    // 🧠 MODALES: EDITAR Y ELIMINAR
    // =====================================================
    const modalEditar = document.getElementById('editModal');
    if (modalEditar) {
        modalEditar.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;

            const cod_tipo_pago = button.getAttribute('data-cod_tipo_pago');
            const nombre_tipo_pago = button.getAttribute('data-nombre_tipo_pago');
            const status = button.getAttribute('data-status');

            const formEditar = modalEditar.querySelector('form');
            if (formEditar) {
                formEditar.querySelector('#edit_cod_tipo_pago').value = cod_tipo_pago;
                formEditar.querySelector('#edit_nombre_tipo_pago').value = nombre_tipo_pago;
                formEditar.querySelector('#edit_estado').value = status;
            }
        });
    }

    const modalEliminar = document.getElementById('deleteModal');
    if (modalEliminar) {
        modalEliminar.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const codTipo_pago = button.getAttribute('data-cod_tipo_pago');
            const nombre_tipo_pago = button.getAttribute('data-nombre_tipo_pago');
            const formEliminar = document.getElementById('elimodal');
            if (formEliminar) {
                formEliminar.querySelector('#TipoPagoCod').value = codTipo_pago;
            }
            modalEliminar.querySelector('#nombreEliminar').textContent = nombre_tipo_pago;

        });
    }

    // =====================================================
    // ⚠️ VALIDACIÓN DE EXISTENCIA DE TIPO DE PAGO
    // =====================================================
    $('#nombre_tipo_pago, #edit_nombre_tipo_pago').blur(function () {

        let buscar = $(this).val();

        if (buscar === '') return;

         $.post('/admin?ruta=tipopagos',
            { buscar: buscar },
            function (response) {

                if (response.existe === true) {

                    Swal.fire({
                        title: 'Advertencia',
                        text: 'El tipo de pago ya se encuentra registrado',
                        icon: 'warning'
                    });

                    $('#nombre_tipo_pago, #edit_nombre_tipo_pago').val('').focus();
                }
            },
            'json'
        );
    });

    // =====================================================
    // 💡 TOOLTIP PERSONALIZADO
    // =====================================================
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl, {
            template: '<div class="tooltip" role="tooltip" style="background-color: white; color: black; border: 1px solid black;"><div class="tooltip-arrow"></div><div class="tooltip-inner"></div></div>'
        });
    });
});
