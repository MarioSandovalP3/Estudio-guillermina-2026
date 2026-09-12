console.log("Abrió productos (inventario)");

const regexProducto = /^[a-zA-ZÁÉÍÓÚáéíóúñÑ0-9\s.,()\-_/+#%&]+$/;
const regexPrecio = /^\d+(\.\d{1,2})?$/;
const regexStock = /^\d+$/;

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
    // VALIDAR NOMBRE
    // =====================================================

    function validarNombre(campo) {

        const nombre = campo.val().trim();

        // VACÍO
        if (nombre === '') {

            mostrarError(
                campo,
                '* Este campo no puede estar vacío.'
            );

            return false;
        }


        // MÁXIMO 50
        if (nombre.length > 50) {

            mostrarError(
                campo,
                'Máximo 50 caracteres.'
            );

            return false;
        }


        // LETRAS, NÚMEROS Y SIGNOS
        if (!regexProducto.test(nombre)) {

            mostrarError(
                campo,
                'Solo se permiten letras, números y signos.'
            );

            return false;
        }


        quitarError(campo);

        campo.addClass('is-valid');

        return true;
    }


    // =====================================================
    // VALIDAR PRECIO
    // =====================================================

    function validarPrecio(campo) {

        const precio = campo.val().trim();

        // VACÍO
        if (precio === '') {

            mostrarError(
                campo,
                '* Este campo no puede estar vacío.'
            );

            return false;
        }


        // MÁXIMO 10 CARACTERES
        if (precio.length > 10) {

            mostrarError(
                campo,
                'El precio permite máximo 10 caracteres.'
            );

            return false;
        }


        // FORMATO
        if (!regexPrecio.test(precio)) {

            mostrarError(
                campo,
                'Ingrese un precio válido con máximo 2 decimales.'
            );

            return false;
        }


        // MAYOR QUE CERO
        if (parseFloat(precio) <= 0) {

            mostrarError(
                campo,
                'El precio debe ser mayor que cero.'
            );

            return false;
        }


        quitarError(campo);

        campo.addClass('is-valid');

        return true;
    }


    // =====================================================
    // VALIDAR STOCK
    // =====================================================

    function validarStock(campo) {

        const stock = campo.val().trim();

        // VACÍO
        if (stock === '') {

            mostrarError(
                campo,
                '* Este campo no puede estar vacío.'
            );

            return false;
        }


        // SOLO ENTEROS
        if (!regexStock.test(stock)) {

            mostrarError(
                campo,
                'El stock solo permite números enteros.'
            );

            return false;
        }


        quitarError(campo);

        campo.addClass('is-valid');

        return true;
    }


    // =====================================================
    // VALIDAR FECHA DE VENCIMIENTO
    // =====================================================

    function validarFechaVencimiento(campo) {

    const fecha = campo.val().trim();

    // CAMPO VACÍO
    if (fecha === '') {

        mostrarError(
            campo,
            '* La fecha de vencimiento es obligatoria.'
        );

        return false;
    }

    // FECHA ACTUAL
    const hoy = new Date();

    hoy.setHours(0, 0, 0, 0);

    // FECHA SELECCIONADA
    const fechaSeleccionada =
        new Date(fecha + 'T00:00:00');

    // NO PERMITIR FECHAS ANTERIORES
    if (fechaSeleccionada < hoy) {

        mostrarError(
            campo,
            'La fecha de vencimiento no puede ser anterior a hoy.'
        );

        return false;
    }

    quitarError(campo);

    campo.addClass('is-valid');

    return true;
}


    // =====================================================
    // NOMBRE - BLOQUEAR CARACTERES Y 50
    // =====================================================

    $(document).on(
        'keydown',
        '#nombre_producto, #edit_nombre_producto',
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


            // CTRL + A / CTRL + C / CTRL + V / CTRL + X
            if (e.ctrlKey || e.metaKey) {
                return;
            }


            // MÁXIMO 50
            if (valor.length >= 50) {

                e.preventDefault();

                mostrarError(
                    campo,
                    'Máximo 50 caracteres.'
                );

                return;
            }


            // VALIDAR CARÁCTER
            if (
                e.key.length === 1 &&
                !regexProducto.test(e.key)
            ) {

                e.preventDefault();

                mostrarError(
                    campo,
                    'Solo se permiten letras, números y signos.'
                );

                return;
            }

        }
    );


    // =====================================================
    // NOMBRE - PEGAR
    // =====================================================

    $(document).on(
        'paste',
        '#nombre_producto, #edit_nombre_producto',
        function (e) {

            const campo = $(this);

            const texto =
                (e.originalEvent.clipboardData ||
                 window.clipboardData)
                .getData('text');


            // MÁXIMO 50
            if (
                campo.val().length +
                texto.length > 50
            ) {

                e.preventDefault();

                mostrarError(
                    campo,
                    'Máximo 50 caracteres.'
                );

                return;
            }


            // CARACTERES PERMITIDOS
            if (!regexProducto.test(texto)) {

                e.preventDefault();

                mostrarError(
                    campo,
                    'Solo se permiten letras, números y signos.'
                );

                return;
            }

        }
    );


    // =====================================================
    // NOMBRE - INPUT
    // =====================================================

    $(document).on(
        'input',
        '#nombre_producto, #edit_nombre_producto',
        function () {

            const campo = $(this);

            // Seguridad adicional
            if (campo.val().length > 50) {

                campo.val(
                    campo.val().substring(0, 50)
                );

                mostrarError(
                    campo,
                    'Máximo 50 caracteres.'
                );

                return;
            }

            validarNombre(campo);
        }
    );


    // =====================================================
    // PRECIO - BLOQUEAR
    // =====================================================

    $(document).on(
        'keydown',
        '#precio_producto, #edit_precio_producto',
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


            if (teclasPermitidas.includes(e.key)) {
                return;
            }


            if (e.ctrlKey || e.metaKey) {
                return;
            }


            // MÁXIMO 10 CARACTERES
            if (valor.length >= 10) {

                e.preventDefault();

                mostrarError(
                    campo,
                    'El precio permite máximo 10 caracteres.'
                );

                return;
            }


            // SOLO NÚMEROS
            if (/^\d$/.test(e.key)) {

                // Comprobar máximo 2 decimales
                if (valor.includes('.')) {

                    const decimales =
                        valor.split('.')[1];

                    if (
                        decimales.length >= 2 &&
                        campo[0].selectionStart >
                        valor.indexOf('.')
                    ) {

                        e.preventDefault();

                        mostrarError(
                            campo,
                            'El precio solo permite 2 decimales.'
                        );

                        return;
                    }
                }

                return;
            }


            // UN SOLO PUNTO
            if (
                e.key === '.' &&
                !valor.includes('.')
            ) {

                return;
            }


            // BLOQUEAR TODO LO DEMÁS
            e.preventDefault();

            mostrarError(
                campo,
                'El precio solo permite números.'
            );

        }
    );


    // =====================================================
    // PRECIO - PEGAR
    // =====================================================

    $(document).on(
        'paste',
        '#precio_producto, #edit_precio_producto',
        function (e) {

            const campo = $(this);

            const texto =
                (e.originalEvent.clipboardData ||
                 window.clipboardData)
                .getData('text');


            if (texto.length > 10) {

                e.preventDefault();

                mostrarError(
                    campo,
                    'El precio permite máximo 10 caracteres.'
                );

                return;
            }


            if (!regexPrecio.test(texto)) {

                e.preventDefault();

                mostrarError(
                    campo,
                    'El precio solo permite números y máximo 2 decimales.'
                );

                return;
            }

        }
    );


    // =====================================================
    // PRECIO - INPUT
    // =====================================================

    $(document).on(
        'input',
        '#precio_producto, #edit_precio_producto',
        function () {

            const campo = $(this);

            let valor = campo.val();


            // MÁXIMO 10
            if (valor.length > 10) {

                campo.val(
                    valor.substring(0, 10)
                );

                mostrarError(
                    campo,
                    'El precio permite máximo 10 caracteres.'
                );

                return;
            }


            // CONTROLAR DECIMALES
            if (valor.includes('.')) {

                const partes = valor.split('.');

                if (partes[1].length > 2) {

                    campo.val(
                        partes[0] + '.' +
                        partes[1].substring(0, 2)
                    );

                    mostrarError(
                        campo,
                        'El precio solo permite 2 decimales.'
                    );

                    return;
                }
            }


            validarPrecio(campo);
        }
    );


    // =====================================================
    // STOCK - BLOQUEAR
    // =====================================================

    $(document).on(
        'keydown',
        '#stock, #edit_stock',
        function (e) {

            const campo = $(this);

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


            if (teclasPermitidas.includes(e.key)) {
                return;
            }


            if (e.ctrlKey || e.metaKey) {
                return;
            }


            if (!/^\d$/.test(e.key)) {

                e.preventDefault();

                mostrarError(
                    campo,
                    'El stock solo permite números enteros.'
                );
            }

        }
    );


    // =====================================================
    // STOCK - INPUT
    // =====================================================

    $(document).on(
        'input',
        '#stock, #edit_stock',
        function () {

            const campo = $(this);

            // Eliminar cualquier carácter que no sea número
            campo.val(
                campo.val().replace(/\D/g, '')
            );

            validarStock(campo);
        }
    );


    // =====================================================
    // FECHA DE VENCIMIENTO
    // =====================================================

    function establecerFechaMinima() {

        const hoy = new Date();

        const año = hoy.getFullYear();

        const mes =
            String(hoy.getMonth() + 1)
            .padStart(2, '0');

        const dia =
            String(hoy.getDate())
            .padStart(2, '0');

        const fechaHoy =
            `${año}-${mes}-${dia}`;


        $('#fecha_vencimiento')
            .attr('min', fechaHoy);
    }


    // =====================================================
// ESTABLECER FECHA MÍNIMA
// =====================================================

function establecerFechaMinima() {

    const hoy = new Date();

    const año = hoy.getFullYear();

    const mes = String(hoy.getMonth() + 1).padStart(2, '0');

    const dia = String(hoy.getDate()).padStart(2, '0');

    const fechaHoy = `${año}-${mes}-${dia}`;

    $('#fecha_vencimiento').attr('min', fechaHoy);
}

    // =====================================================
    // BLUR
    // =====================================================

    $(document).on(
        'blur',
        '#nombre_producto, #edit_nombre_producto',
        function () {

            validarNombre($(this));

        }
    );


    $(document).on(
        'blur',
        '#precio_producto, #edit_precio_producto',
        function () {

            validarPrecio($(this));

        }
    );


    $(document).on(
        'blur',
        '#stock, #edit_stock',
        function () {

            validarStock($(this));

        }
    );


    // =====================================================
    // REGISTRAR
    // =====================================================

    $('#formRegistrarProducto').on(
        'submit',
        function (e) {

            e.preventDefault();

            const form = this;

            const btn =
                $(form).find(
                    'button[type="submit"]'
                );


            const nombre =
                $(form).find(
                    'input[name="nombre_producto"]'
                );

            const precio =
                $(form).find(
                    'input[name="precio_producto"]'
                );

            const stock =
                $(form).find(
                    'input[name="stock"]'
                );

            const fecha =
                $(form).find(
                    'input[name="fecha_vencimiento"]'
                );


            const nombreValido =
                validarNombre(nombre);

            const precioValido =
                validarPrecio(precio);

            const stockValido =
                validarStock(stock);

            const fechaValida =
                validarFechaVencimiento(fecha);


            if (
                !nombreValido ||
                !precioValido ||
                !stockValido ||
                !fechaValida
            ) {

                return;
            }


            btn.prop('disabled', true);


            $.post(
                '/admin?ruta=producto',
                $(form).serialize(),
                function (res) {

                    Swal.fire(res).then(() => {

                        if (
                            res.icon === 'success'
                        ) {

                            form.reset();

                            $(form)
                                .find(
                                    '.is-invalid, .is-valid'
                                )
                                .removeClass(
                                    'is-invalid is-valid'
                                );

                            $(form)
                                .find(
                                    '.invalid-feedback'
                                )
                                .hide();

                            cerrarModal(
                                '#modalRegistrar'
                            );

                            $('#table1').load(
                                location.href +
                                ' #table1>*',
                                ''
                            );
                        }

                        btn.prop(
                            'disabled',
                            false
                        );

                    });

                },
                'json'
            );

        }
    );


    // =====================================================
    // EDITAR
    // =====================================================

    $('#formEditarProducto').on(
        'submit',
        function (e) {

            e.preventDefault();

            const form = this;

            const btn =
                $(form).find(
                    'button[type="submit"]'
                );


            const nombre =
                $('#edit_nombre_producto');

            const precio =
                $('#edit_precio_producto');

            const stock =
                $('#edit_stock');

            const fecha =
                $('#edit_fecha_vencimiento');

            const fechaOriginal =
                $('#edit_fecha_vencimiento_original').val();


            const nombreValido =
                validarNombre(nombre);

            const precioValido =
                validarPrecio(precio);

            const stockValido =
                validarStock(stock);

            const fechaValida = fecha.val().trim() !== '' &&
                (fecha.val() === fechaOriginal || validarFechaVencimiento(fecha));


            if (
                !nombreValido ||
                !precioValido ||
                !stockValido ||
                !fechaValida
            ) {

                return;
            }


            btn.prop('disabled', true);


            $.post(
                '/admin?ruta=producto',
                $(form).serialize(),
                function (res) {

                    Swal.fire(res).then(() => {

                        if (
                            res.icon === 'success'
                        ) {

                            form.reset();

                            $(form)
                                .find(
                                    '.is-invalid, .is-valid'
                                )
                                .removeClass(
                                    'is-invalid is-valid'
                                );

                            $(form)
                                .find(
                                    '.invalid-feedback'
                                )
                                .hide();

                            cerrarModal(
                                '#modalEditar'
                            );

                            $('#table1').load(
                                location.href +
                                ' #table1>*',
                                ''
                            );
                        }

                        btn.prop(
                            'disabled',
                            false
                        );

                    });

                },
                'json'
            );

        }
    );


    // =====================================================
    // ELIMINAR
    // =====================================================

    $('#formEliminarProducto').on(
        'submit',
        function (e) {

            e.preventDefault();

            $.post(
                '/admin?ruta=producto',
                $(this).serialize(),
                function (res) {

                    Swal.fire(res).then(() => {

                        cerrarModal(
                            '#modalEliminar'
                        );

                        if (
                            res.icon === 'success'
                        ) {

                            $('#table1').load(
                                location.href +
                                ' #table1>*',
                                ''
                            );
                        }

                    });

                },
                'json'
            );

        }
    );


    // =====================================================
    // ABRIR MODAL EDITAR
    // =====================================================

    const modalEditar =
        document.getElementById(
            'modalEditar'
        );

    if (modalEditar) {

        modalEditar.addEventListener(
            'show.bs.modal',
            function (event) {

                const button =
                    event.relatedTarget;

                $('#edit_cod_producto').val(
                    button.getAttribute(
                        'data-cod_producto'
                    )
                );

                $('#edit_nombre_producto').val(
                    button.getAttribute(
                        'data-nombre_producto'
                    )
                );

                $('#edit_precio_producto').val(
                    button.getAttribute(
                        'data-precio_producto'
                    )
                );

                $('#edit_stock').val(
                    button.getAttribute(
                        'data-stock'
                    )
                );

                $('#edit_fecha_vencimiento').val(
                    button.getAttribute(
                        'data-fecha_vencimiento'
                    )
                );

                $('#edit_fecha_vencimiento_original').val(
                    button.getAttribute(
                        'data-fecha_vencimiento'
                    )
                );

                $('#edit_cod_categoria').val(
                    button.getAttribute(
                        'data-cod_categoria'
                    )
                );

                $('#edit_cod_marca').val(
                    button.getAttribute(
                        'data-cod_marca'
                    )
                );

                $('#edit_cod_unidad').val(
                    button.getAttribute(
                        'data-cod_unidad'
                    )
                );

                $('#edit_cod_presentacion').val(
                    button.getAttribute(
                        'data-cod_presentacion'
                    )
                );

                $('#edit_cod_medida').val(
                    button.getAttribute(
                        'data-cod_medida'
                    )
                );

                $('#edit_cod_tipo_producto').val(
                    button.getAttribute(
                        'data-cod_tipo_producto'
                    )
                );

                $('#edit_status').val(
                    button.getAttribute(
                        'data-status'
                    )
                );

                establecerFechaMinima();

            }
        );
    }


    // =====================================================
    // ABRIR MODAL ELIMINAR
    // =====================================================

    const modalEliminar =
        document.getElementById(
            'modalEliminar'
        );

    if (modalEliminar) {

        modalEliminar.addEventListener(
            'show.bs.modal',
            function (event) {

                const button =
                    event.relatedTarget;

                $('#delete_cod_producto').val(
                    button.getAttribute(
                        'data-cod_producto'
                    )
                );

            }
        );
    }


    // =====================================================
    // MODAL VER
    // =====================================================

    const modalVer =
        document.getElementById(
            'modalVer'
        );

    if (modalVer) {

        modalVer.addEventListener(
            'show.bs.modal',
            function (event) {

                const button =
                    event.relatedTarget;

                $('#ver_nombre').text(
                    button.getAttribute(
                        'data-nombre'
                    )
                );

                $('#ver_marca').text(
                    button.getAttribute(
                        'data-marca'
                    )
                );

                $('#ver_categoria').text(
                    button.getAttribute(
                        'data-categoria'
                    )
                );

                $('#ver_unidad').text(
                    button.getAttribute(
                        'data-unidad'
                    )
                );

                $('#ver_presentacion').text(
                    button.getAttribute(
                        'data-presentacion'
                    )
                );

                $('#ver_medida').text(
                    button.getAttribute(
                        'data-medida'
                    )
                );

                $('#ver_tipo').text(
                    button.getAttribute(
                        'data-tipo'
                    )
                );

                $('#ver_precio').text(
                    button.getAttribute(
                        'data-precio'
                    )
                );

                $('#ver_stock').text(
                    button.getAttribute(
                        'data-stock'
                    )
                );

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