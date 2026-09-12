
console.log('Abrio rol.js');

const regexRol = /^[a-zA-ZÁÉÍÓÚáéíóúñÑ\s]+$/;
const regexNoPermitidosRol = /[^a-zA-ZÁÉÍÓÚáéíóúñÑ\s]/g;

$(document).ready(function () {

    // =====================================================
    // 💬 MOSTRAR ERROR
    // =====================================================

    function mostrarError(input, mensaje) {
        const $input = $(input);
        let $feedback = $input.next('.invalid-feedback');

        if (!$feedback.length) {
            $feedback = $('<div class="invalid-feedback"></div>');
            $input.after($feedback);
        }

        $input.addClass('is-invalid').removeClass('is-valid');
        $feedback.text(mensaje).show();
    }

    // =====================================================
    // ✅ OCULTAR ERROR
    // =====================================================

    function ocultarError(input) {
        const $input = $(input);

        $input.removeClass('is-invalid').addClass('is-valid');
        $input.next('.invalid-feedback').hide();
    }

    // =====================================================
    // 🔒 CERRAR MODAL
    // =====================================================

    function cerrarModal(idModal) {
        $(idModal).modal('hide');

        $(idModal).on('hidden.bs.modal', function () {
            $('.modal-backdrop').remove();
            $('body').removeClass('modal-open');
            $(this).off('hidden.bs.modal');
        });
    }

    // =====================================================
    // 🔔 ALERTA
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
    // 🔠 VALIDACIÓN EN TIEMPO REAL
    // =====================================================

    $('#nombre_rol, #edit_rol').on('input', function () {

        const originalValue = this.value;
        const valorFiltrado = this.value.replace(regexNoPermitidosRol, '');

        // -------------------------------------------------
        // SI SE ESCRIBIÓ UN CARÁCTER NO PERMITIDO
        // -------------------------------------------------

        if (originalValue !== valorFiltrado) {

            this.value = valorFiltrado;

            mostrarError(
                this,
                'En este campo solo se permiten letras.'
            );

            return;
        }

        // -------------------------------------------------
        // SI EL CAMPO ESTÁ VACÍO
        // -------------------------------------------------

        if (this.value.trim() === '') {

            $(this).removeClass('is-valid is-invalid');
            $(this).next('.invalid-feedback').hide();

            return;
        }

        // -------------------------------------------------
        // VALIDAR CONTENIDO
        // -------------------------------------------------

        if (!regexRol.test(this.value)) {

            mostrarError(
                this,
                'En este campo solo se permiten letras.'
            );

        } else {

            ocultarError(this);
        }

        $(this).parsley().validate();
    });

    // =====================================================
    // ⌨️ BLOQUEAR CARACTERES NO PERMITIDOS
    // =====================================================

    $('#nombre_rol, #edit_rol').on('keydown', function (e) {

        // Permitir teclas especiales
        if (e.key.length !== 1) {
            return;
        }

        // Bloquear números y símbolos
        if (!regexRol.test(e.key)) {

            e.preventDefault();

            mostrarError(
                this,
                'En este campo solo se permiten letras.'
            );
        }
    });

    // =====================================================
    // 📋 BLOQUEAR PEGADO INVÁLIDO
    // =====================================================

    $('#nombre_rol, #edit_rol').on('paste', function (e) {

        const texto = e.originalEvent.clipboardData.getData('text');

        if (!regexRol.test(texto)) {

            e.preventDefault();

            mostrarError(
                this,
                'En este campo solo se permiten letras.'
            );
        }
    });

    // =====================================================
    // 📝 REGISTRAR ROL
    // =====================================================

    $('#Rol').on('show.bs.modal', function () {

        const formulario = $('#formRol');

        formulario[0].reset();
        formulario.parsley().reset();

        formulario.find('.invalid-feedback').hide();

        formulario.find('.is-invalid, .is-valid')
            .removeClass('is-invalid is-valid');
    });

    $('#formRol').on('submit', function (e) {

        e.preventDefault();

        const formulario = $(this);
        const parsley = formulario.parsley();

        if (!parsley.validate()) {
            return;
        }

        const nombreRol = $('#nombre_rol').val().trim();

        if (!regexRol.test(nombreRol)) {

            mostrarError(
                $('#nombre_rol'),
                'En este campo solo se permiten letras.'
            );

            return;
        }

        $.post(
            '/admin?ruta=rol',
            formulario.serialize(),
            function (res) {

                alerta(res).then(() => {

                    if (res.icon === 'success') {

                        formulario[0].reset();
                        parsley.reset();

                        formulario.find('.is-invalid, .is-valid')
                            .removeClass('is-invalid is-valid');

                        formulario.find('.invalid-feedback').hide();

                        cerrarModal('#Rol');

                        $('#table1').load(
                            location.href + ' #table1>*',
                            ''
                        );
                    }
                });

            },
            'json'
        );
    });

    // =====================================================
    // ✏️ EDITAR ROL
    // =====================================================

    $('#formEditRol').on('submit', function (e) {

        e.preventDefault();

        const formulario = $(this);
        const nombreRol = $('#edit_rol').val().trim();

        if (!formulario.parsley().validate()) {
            return;
        }

        if (!regexRol.test(nombreRol)) {

            mostrarError(
                $('#edit_rol'),
                'En este campo solo se permiten letras.'
            );

            return;
        }

        $.post(
            '/admin?ruta=rol',
            formulario.serialize(),
            function (res) {

                alerta(res).then(() => {

                    if (res.icon === 'success') {

                        formulario[0].reset();

                        formulario.parsley().reset();

                        formulario.find('.is-invalid, .is-valid')
                            .removeClass('is-invalid is-valid');

                        formulario.find('.invalid-feedback').hide();

                        cerrarModal('#editModal');

                        $('#table1').load(
                            location.href + ' #table1>*',
                            ''
                        );
                    }
                });

            },
            'json'
        );
    });

    // =====================================================
    // 🗑️ ELIMINAR ROL
    // =====================================================

    $('#elimodal').on('submit', function (e) {

        e.preventDefault();

        $.post(
            '/admin?ruta=rol',
            $(this).serialize(),
            function (res) {

                alerta(res).then(() => {

                    cerrarModal('#deleteModal');

                    if (
                        res.icon === 'success' ||
                        res.icon === 'warning'
                    ) {

                        $('#table1').load(
                            location.href + ' #table1>*',
                            ''
                        );
                    }
                });

            },
            'json'
        );
    });

    // =====================================================
    // 🔁 REINICIAR MODAL REGISTRAR
    // =====================================================

    $('#btnCerrarModal').on('click', function () {

        const formulario = $('#formRol');

        formulario[0].reset();
        formulario.parsley().reset();

        formulario.find('.is-invalid, .is-valid')
            .removeClass('is-invalid is-valid');

        formulario.find('.invalid-feedback').hide();
    });

    $('#Rol').on('hidden.bs.modal', function () {

        const formulario = $('#formRol');

        formulario[0].reset();
        formulario.parsley().reset();

        formulario.find('.is-invalid, .is-valid')
            .removeClass('is-invalid is-valid');

        formulario.find('.invalid-feedback').hide();
    });

    // =====================================================
    // 🔁 REINICIAR MODAL EDITAR
    // =====================================================

    $('#btnCerrar, #btnClose').on('click', function () {

        const formulario = $('#formEditRol');

        formulario.find('.is-invalid, .is-valid')
            .removeClass('is-invalid is-valid');

        formulario.find('.invalid-feedback').hide();

        formulario.parsley().reset();
    });

    $('#editModal').on('hidden.bs.modal', function () {

        const formulario = $('#formEditRol');

        formulario[0].reset();
        formulario.parsley().reset();

        formulario.find('.is-invalid, .is-valid')
            .removeClass('is-invalid is-valid');

        formulario.find('.invalid-feedback').hide();
    });

    // =====================================================
    // 🔄 CAMBIO DE ESTILOS SEGÚN PARSLEY
    // =====================================================

    if (window.Parsley) {

        window.Parsley.on('field:error', function () {

            this.$element
                .addClass('is-invalid')
                .removeClass('is-valid');

            let $feedback = this.$element.next('.invalid-feedback');

            if (!$feedback.length) {

                $feedback = $('<div class="invalid-feedback"></div>');

                this.$element.after($feedback);
            }

            $feedback
                .text(this.getErrorsMessages()[0])
                .show();
        });

        window.Parsley.on('field:success', function () {

            this.$element
                .removeClass('is-invalid')
                .addClass('is-valid');

            this.$element
                .next('.invalid-feedback')
                .hide();
        });
    }

    // =====================================================
    // ✏️ CARGAR DATOS EN MODAL EDITAR
    // =====================================================

    const editModal = document.getElementById('editModal');

    if (editModal) {

        editModal.addEventListener(
            'show.bs.modal',
            function (event) {

                const button = event.relatedTarget;

                const cod_rol =
                    button.getAttribute('data-id');

                const nombre_rol =
                    button.getAttribute('data-nombre');

                const status =
                    button.getAttribute('data-status');

                const formEditar =
                    editModal.querySelector('form');

                if (formEditar) {

                    formEditar.querySelector(
                        '#edit_cod_rol'
                    ).value = cod_rol;

                    formEditar.querySelector(
                        '#edit_rol'
                    ).value = nombre_rol;

                    formEditar.querySelector(
                        '#edit_estado'
                    ).value = status;
                }
            }
        );
    }

    // =====================================================
    // 🗑️ CARGAR DATOS EN MODAL ELIMINAR
    // =====================================================

    const modalEliminar =
        document.getElementById('deleteModal');

    if (modalEliminar) {

        modalEliminar.addEventListener(
            'show.bs.modal',
            function (event) {

                const button = event.relatedTarget;

                const codRol =
                    button.getAttribute('data-codigo');

                const nombre =
                    button.getAttribute('data-nombre');

                const formEliminar =
                    document.getElementById('elimodal');

                if (formEliminar) {

                    formEliminar.querySelector(
                        '#rolCodigo'
                    ).value = codRol;
                }

                modalEliminar.querySelector(
                    '#nombreEliminar'
                ).textContent = nombre;
            }
        );
    }

    // =====================================================
    // 💬 TOOLTIP PERSONALIZADO
    // =====================================================

    const tooltipTriggerList =
        [].slice.call(
            document.querySelectorAll(
                '[data-bs-toggle="tooltip"]'
            )
        );

    tooltipTriggerList.map(function (tooltipTriggerEl) {

        return new bootstrap.Tooltip(
            tooltipTriggerEl,
            {
                template: `
                    <div class="tooltip" role="tooltip"
                        style="background-color:white;
                        color:black;
                        border:1px solid black;">
                        <div class="tooltip-arrow"></div>
                        <div class="tooltip-inner"></div>
                    </div>
                `
            }
        );
    });

    // =====================================================
    // 🔎 VALIDAR SI EL ROL YA EXISTE
    // =====================================================

    $('#nombre_rol, #edit_rol').on('blur', function () {

        const campo = $(this);
        const buscar = campo.val().trim();

        if (buscar === '') {
            return;
        }

        const datos = {
            buscar: buscar
        };

        if (campo.attr('id') === 'edit_rol') {

            datos.cod_rol =
                $('#edit_cod_rol').val();
        }

        $.post(
            '/admin?ruta=rol',
            datos,
            function (response) {

                if (response.existe === true) {

                    Swal.fire({
                        title: 'Advertencia',
                        text: 'El rol ya se encuentra registrado',
                        icon: 'warning'
                    }).then(function () {

                        campo.val('').focus();

                        campo.removeClass(
                            'is-valid is-invalid'
                        );

                        campo.next(
                            '.invalid-feedback'
                        ).hide();
                    });
                }
            },
            'json'
        );
    });

    // =====================================================
    // 🔢 CONTROL DE MAXLENGTH
    // =====================================================

    $(document).on(
        'input',
        '#formRol input[maxlength], #formEditRol input[maxlength]',
        function () {

            const max =
                parseInt(
                    this.getAttribute('maxlength')
                );

            if (!max) {
                return;
            }

            let feedback =
                $(this).next('.invalid-feedback');

            if (!feedback.length) {

                feedback =
                    $('<div class="invalid-feedback"></div>');

                $(this).after(feedback);
            }

            if (this.value.length >= max) {

                feedback
                    .text('Límite de caracteres alcanzado')
                    .css({
                        display: 'block',
                        width: '100%'
                    });

                $(this)
                    .addClass('is-invalid')
                    .removeClass('is-valid');

            } else if (this.value.trim() !== '') {

                feedback.hide();

                if (regexRol.test(this.value)) {

                    $(this)
                        .removeClass('is-invalid')
                        .addClass('is-valid');
                }
            }
        }
    );

});
