console.log('Abrio unidad.js');

// =====================================================
// 🔢 EXPRESIONES REGULARES
// =====================================================
const regexUnidad = /^[0-9]+$/;
const regexNoPermitidosUnidad = /[^0-9]/g;

// =====================================================
// ✅ VALIDACIONES
// =====================================================
$(document).ready(function () {

    // =====================================================
    // 🔢 BLOQUEO DE CARACTERES INVÁLIDOS (TIEMPO REAL)
    // =====================================================
    $('#formRegistrarUnidad input[name="nombre_unidad"], #formEditarUnidad input[name="nombre_unidad"]')
        .on('input', function () {

            const originalValue = this.value;
            this.value = this.value.replace(regexNoPermitidosUnidad, '');

            if (this.value !== originalValue) {

                $(this).addClass('is-invalid').removeClass('is-valid');

                if ($(this).next('.invalid-feedback').length === 0) {

                    $(this).after('<div class="invalid-feedback">Solo se permiten números.</div>');

                } else {

                    $(this).next('.invalid-feedback')
                        .text('Solo se permiten números.')
                        .show();
                }

            } else {

                if (this.value.trim() === '') {

                    $(this).addClass('is-invalid').removeClass('is-valid');

                    $(this).next('.invalid-feedback')
                        .text('Este campo es obligatorio.')
                        .show();

                } else {

                    $(this).removeClass('is-invalid').addClass('is-valid');
                    $(this).next('.invalid-feedback').hide();
                }
            }

        });

    // =====================================================
    // 🔁 LIMPIAR REGISTRAR
    // =====================================================
    $('#modalRegistrarUnidad').on('hidden.bs.modal', function () {

        $('#formRegistrarUnidad')[0].reset();
        $('#formRegistrarUnidad').parsley().reset();

        $(this).find('.is-invalid, .is-valid')
            .removeClass('is-invalid is-valid');

        $(this).find('.invalid-feedback').remove();
    });

    // =====================================================
    // 🔁 LIMPIAR EDITAR
    // =====================================================
    $('#modalEditarUnidad').on('hidden.bs.modal', function () {

        $('#formEditarUnidad')[0].reset();
        $('#formEditarUnidad').parsley().reset();

        $(this).find('.is-invalid, .is-valid')
            .removeClass('is-invalid is-valid');

        $(this).find('.invalid-feedback').remove();
    });

    // =====================================================
    // 🔔 PARSLEY ESTILOS
    // =====================================================
    window.Parsley.on('field:error', function () {

        this.$element.addClass('is-invalid').removeClass('is-valid');

        if (this.$element.next('.invalid-feedback').length === 0) {

            this.$element.after(
                '<div class="invalid-feedback">' +
                this.getErrorsMessages()[0] +
                '</div>'
            );

        } else {

            this.$element.next('.invalid-feedback')
                .text(this.getErrorsMessages()[0])
                .show();
        }

    });

    window.Parsley.on('field:success', function () {

        this.$element.removeClass('is-invalid').addClass('is-valid');
        this.$element.next('.invalid-feedback').hide();
    });

    // =====================================================
    // ⚙️ FUNCIONES
    // =====================================================
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
    // 🟢 REGISTRAR UNIDAD
    // =====================================================
    $('#formRegistrarUnidad').on('submit', function (e) {

        e.preventDefault();

        if (!$(this).parsley().validate()) return;

        $.post('/admin?ruta=unidad', $(this).serialize(), function (res) {

            alerta(res).then(() => {

                if (res.icon === 'success') {

                    $('#formRegistrarUnidad')[0].reset();
                    $('#formRegistrarUnidad').parsley().reset();

                    cerrarModal('#modalRegistrarUnidad');

                    $('#table1').load(location.href + ' #table1>*', '');
                }

            });

        }, 'json');

    });

    // =====================================================
    // ✏️ EDITAR UNIDAD
    // =====================================================
    $('#formEditarUnidad').on('submit', function (e) {

        e.preventDefault();

        if (!$(this).parsley().validate()) return;

        $.post('/admin?ruta=unidad', $(this).serialize(), function (res) {

            alerta(res).then(() => {

                if (res.icon === 'success') {

                    $('#formEditarUnidad')[0].reset();

                    $('#modalEditarUnidad .is-invalid, #modalEditarUnidad .is-valid')
                        .removeClass('is-invalid is-valid');

                    $('#formEditarUnidad').parsley().reset();

                    cerrarModal('#modalEditarUnidad');

                    $('#table1').load(location.href + ' #table1>*', '');
                }

            });

        }, 'json');

    });

    // =====================================================
    // 🗑️ ELIMINAR UNIDAD
    // =====================================================
    $('#formEliminarUnidad').on('submit', function (e) {

        e.preventDefault();

        $.post('/admin?ruta=unidad', $(this).serialize(), function (res) {

            alerta(res).then(() => {

                if (res.icon === 'success' || res.icon === 'warning') {

                    $('#formEliminarUnidad')[0].reset();

                    cerrarModal('#modalEliminarUnidad');

                    $('#table1').load(location.href + ' #table1>*', '');
                }

            });

        }, 'json');

    });

    // =====================================================
    // ✏️ CARGAR DATOS MODAL EDITAR
    // =====================================================
    const modalEditarUnidad = document.getElementById('modalEditarUnidad');

    if (modalEditarUnidad) {

        modalEditarUnidad.addEventListener('show.bs.modal', function (event) {

            const button = event.relatedTarget;

            const cod_unidad = button.getAttribute('data-cod_unidad');
            const nombre_unidad = button.getAttribute('data-nombre_unidad');
            const cod_presentacion = button.getAttribute('data-cod_presentacion');
            const cod_medida = button.getAttribute('data-cod_medida');
            const status = button.getAttribute('data-status');

            modalEditarUnidad.querySelector('#cod_unidad_edit').value = cod_unidad;
            modalEditarUnidad.querySelector('#nombre_unidad_edit').value = nombre_unidad;
            modalEditarUnidad.querySelector('#cod_presentacion_edit').value = cod_presentacion;
            modalEditarUnidad.querySelector('#cod_medida_edit').value = cod_medida;
            modalEditarUnidad.querySelector('#status_unidad_edit').value = status;

        });

    }


    // =====================================================
    // EN MODAL DE ELIMINACIÓN DE UNIDAD
    // =====================================================
    const modalEliminarUnidad = document.getElementById('modalEliminarUnidad');

    if (modalEliminarUnidad) {
        modalEliminarUnidad.addEventListener('show.bs.modal', function (event) {

            const button = event.relatedTarget;

            const codUnidad = button.getAttribute('data-cod_unidad');
            const nombreUnidad = button.getAttribute('data-nombre_unidad');

            const formEliminar = document.getElementById('formEliminarUnidad');

            if (formEliminar) {
                formEliminar.querySelector('#cod_unidad_eliminar').value = codUnidad;
            }

            // Mostrar nombre de la unidad en el modal
            modalEliminarUnidad.querySelector('#nombre_unidad').textContent = nombreUnidad;

        });
    }


    // =====================================================
    // 🔍 VALIDAR UNIDAD DUPLICADA
    // =====================================================
    $('#nombre_unidad_reg, #nombre_unidad_edit').on('input', function () {
        verificarUnidad($(this));
    });
    $('#cod_presentacion_reg, #cod_presentacion_edit, #cod_medida_reg, #cod_medida_edit').on('change', function () {
        verificarUnidad($(this));
    });
    function verificarUnidad(campo) {
        let editar = campo.attr('id').includes('_edit');
        let nombre_unidad = editar ? $('#nombre_unidad_edit').val().trim() : $('#nombre_unidad_reg').val().trim();
        let cod_presentacion = editar ? $('#cod_presentacion_edit').val() : $('#cod_presentacion_reg').val();
        let cod_medida = editar ? $('#cod_medida_edit').val() : $('#cod_medida_reg').val();
        if (nombre_unidad === '' || cod_presentacion === '' || cod_medida === '') {
            return;
        }
        let datos = {
            buscar: nombre_unidad,
            cod_presentacion: cod_presentacion,
            cod_medida: cod_medida
        };
        if (editar) {
            datos.cod_unidad = $('#cod_unidad_edit').val();
        }
        $.post('/admin?ruta=unidad', datos, function (response) {
            if (response.existe === true) {
                Swal.fire({
                    title: 'Advertencia',
                    text: 'La unidad ya se encuentra registrada con esa presentación y medida',
                    icon: 'warning'
                });
                if (editar) {
                    $('#nombre_unidad_edit').val('').focus();
                } else {
                    $('#nombre_unidad_reg').val('').focus();
                }
            }
        }, 'json');
    }

    $(document).on('input', '#formRegistrarUnidad input[maxlength], #formEditarUnidad input[maxlength]', function () {
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