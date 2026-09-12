console.log("Abrió tipo de producto");

const regexTipoProducto = /^[a-zA-ZÁÉÍÓÚáéíóúÑñ\s]+$/;
const regexSoloLetras = /^[a-zA-ZÁÉÍÓÚáéíóúÑñ\s]$/;

$(document).ready(function () {

    // =====================================================
    // MOSTRAR ERROR
    // =====================================================

    function mostrarError(campo, mensaje) {

        campo.addClass('is-invalid').removeClass('is-valid');

        let feedback = campo.next('.invalid-feedback');

        if (feedback.length === 0) {

            campo.after(
                '<div class="invalid-feedback"></div>'
            );

            feedback = campo.next('.invalid-feedback');
        }

        feedback
            .text(mensaje)
            .show();
    }


    // =====================================================
    // QUITAR ERROR
    // =====================================================

    function quitarError(campo) {

        campo.removeClass('is-invalid');

        const feedback = campo.next('.invalid-feedback');

        if (feedback.length > 0) {
            feedback.hide();
        }
    }


    // =====================================================
    // VALIDAR TIPO DE PRODUCTO
    // =====================================================

    function validarTipoProducto(campo) {

        const valor = campo.val().trim();

        // CAMPO VACÍO
        if (valor === '') {

            mostrarError(
                campo,
                '* Este campo no puede estar vacío.'
            );

            return false;
        }


        // MÁXIMO 20 CARACTERES
        if (valor.length > 20) {

            mostrarError(
                campo,
                'Máximo 20 caracteres.'
            );

            return false;
        }


        // SOLO LETRAS
        if (!regexTipoProducto.test(valor)) {

            mostrarError(
                campo,
                'Solo se permiten letras.'
            );

            return false;
        }


        quitarError(campo);

        campo.addClass('is-valid');

        return true;
    }


    // =====================================================
    // REGISTRAR
    // =====================================================

    $('#formRegistrarTipoProducto').on('submit', function (e) {

        e.preventDefault();

        const form = this;

        const btn = $(form).find('button[type="submit"]');

        const nombre = $(form).find(
            'input[name="nombre_tipo_producto"]'
        );

        // VALIDAR
        if (!validarTipoProducto(nombre)) {
            return;
        }

        btn.prop('disabled', true);

        $.post(
            '/admin?ruta=tipoproducto',
            $(form).serialize(),
            function (res) {

                Swal.fire(res).then(() => {

                    if (res.icon === 'success') {

                        form.reset();

                        $(form)
                            .find('.is-invalid, .is-valid')
                            .removeClass('is-invalid is-valid');

                        $(form)
                            .find('.invalid-feedback')
                            .hide();

                        cerrarModal('#modalRegistrar');

                        $('#table1').load(
                            location.href + ' #table1>*',
                            ''
                        );
                    }

                    btn.prop('disabled', false);

                });

            },
            'json'
        );

    });


    // =====================================================
    // EDITAR
    // =====================================================

    $('#formEditarTipoProducto').on('submit', function (e) {

        e.preventDefault();

        const form = this;

        const btn = $(form).find('button[type="submit"]');

        const nombre = $('#edit_nombre');

        // VALIDAR
        if (!validarTipoProducto(nombre)) {
            return;
        }

        btn.prop('disabled', true);

        $.post(
            '/admin?ruta=tipoproducto',
            $(form).serialize(),
            function (res) {

                Swal.fire(res).then(() => {

                    if (res.icon === 'success') {

                        form.reset();

                        $(form)
                            .find('.is-invalid, .is-valid')
                            .removeClass('is-invalid is-valid');

                        $(form)
                            .find('.invalid-feedback')
                            .hide();

                        cerrarModal('#modalEditar');

                        $('#table1').load(
                            location.href + ' #table1>*',
                            ''
                        );
                    }

                    btn.prop('disabled', false);

                });

            },
            'json'
        );

    });


    // =====================================================
    // BLOQUEAR TECLAS
    // =====================================================

    $(document).on(
        'keydown',
        '#nombre_tipo_producto, #edit_nombre',
        function (e) {

            const campo = $(this);

            const valor = campo.val();

            const teclasPermitidas = [
                'Backspace',
                'Delete',
                'ArrowLeft',
                'ArrowRight',
                'ArrowUp',
                'ArrowDown',
                'Tab',
                'Home',
                'End'
            ];


            // TECLAS DE CONTROL
            if (teclasPermitidas.includes(e.key)) {
                return;
            }


            // CTRL / CMD
            if (e.ctrlKey || e.metaKey) {
                return;
            }


            // MÁXIMO 20 CARACTERES
            if (valor.length >= 20) {

                e.preventDefault();

                mostrarError(
                    campo,
                    'Máximo 20 caracteres.'
                );

                return;
            }


            // SOLO LETRAS
            if (
                e.key.length === 1 &&
                !regexSoloLetras.test(e.key)
            ) {

                e.preventDefault();

                mostrarError(
                    campo,
                    'Solo se permiten letras.'
                );

                return;
            }

        }
    );


    // =====================================================
    // BLOQUEAR PEGAR
    // =====================================================

    $(document).on(
        'paste',
        '#nombre_tipo_producto, #edit_nombre',
        function (e) {

            const campo = $(this);

            const texto =
                (e.originalEvent.clipboardData ||
                 window.clipboardData)
                .getData('text');


            // MÁXIMO 20
            if (
                campo.val().length +
                texto.length > 20
            ) {

                e.preventDefault();

                mostrarError(
                    campo,
                    'Máximo 20 caracteres.'
                );

                return;
            }


            // SOLO LETRAS Y ESPACIOS
            if (!regexTipoProducto.test(texto)) {

                e.preventDefault();

                mostrarError(
                    campo,
                    'Solo se permiten letras.'
                );

                return;
            }

        }
    );


    // =====================================================
    // INPUT
    // =====================================================

    $(document).on(
        'input',
        '#nombre_tipo_producto, #edit_nombre',
        function () {

            const campo = $(this);

            let valor = campo.val();


            // ELIMINAR CARACTERES NO PERMITIDOS
            valor = valor.replace(
                /[^a-zA-ZÁÉÍÓÚáéíóúÑñ\s]/g,
                ''
            );


            // MÁXIMO 20
            if (valor.length > 20) {

                valor = valor.substring(0, 20);

                mostrarError(
                    campo,
                    'Máximo 20 caracteres.'
                );
            }


            campo.val(valor);

            validarTipoProducto(campo);

        }
    );


    // =====================================================
    // VALIDAR AL SALIR DEL CAMPO
    // =====================================================

    $(document).on(
        'blur',
        '#nombre_tipo_producto, #edit_nombre',
        function () {

            validarTipoProducto($(this));

        }
    );


    // =====================================================
    // ELIMINAR
    // =====================================================

    $('#formEliminarTipoProducto').on('submit', function (e) {

        e.preventDefault();

        $.post(
            '/admin?ruta=tipoproducto',
            $(this).serialize(),
            function (res) {

                Swal.fire(res).then(() => {

                    cerrarModal('#modalEliminar');

                    if (res.icon === 'success') {

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
    // ABRIR MODAL EDITAR
    // =====================================================

    const modalEditar =
        document.getElementById('modalEditar');

    if (modalEditar) {

        modalEditar.addEventListener(
            'show.bs.modal',
            function (event) {

                const button = event.relatedTarget;

                const id =
                    button.getAttribute('data-id');

                const nombre =
                    button.getAttribute('data-nombre');

                const status =
                    button.getAttribute('data-status');


                $('#edit_id').val(id);

                $('#edit_nombre').val(nombre);

                $('#edit_status').val(status);

            }
        );
    }


    // =====================================================
    // ABRIR MODAL ELIMINAR
    // =====================================================

    const modalEliminar =
        document.getElementById('modalEliminar');

    if (modalEliminar) {

        modalEliminar.addEventListener(
            'show.bs.modal',
            function (event) {

                const button = event.relatedTarget;

                const id =
                    button.getAttribute('data-id');

                $('#delete_id').val(id);

            }
        );
    }


    // =====================================================
    // CERRAR MODAL
    // =====================================================

    function cerrarModal(id) {

        $(id).modal('hide');

    }

});