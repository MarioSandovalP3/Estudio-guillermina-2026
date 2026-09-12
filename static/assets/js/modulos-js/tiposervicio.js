console.log("Abrió tipos de servicio");

const regexServicio = /^[a-zA-ZÁÉÍÓÚáéíóúñÑ\s]+$/;
const regexPrecio = /^\d{1,23}(\.\d{1,2})?$/;

$(document).ready(function () {

      $('#formRegistrartiposservicios, #formEditarTiposervicio')
        .attr('novalidate', 'novalidate');

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

        const feedback =
            campo.next('.invalid-feedback');

        if (feedback.length > 0) {
            feedback.hide();
        }
    }


    // =====================================================
    // VALIDAR CAMPO VACÍO
    // =====================================================

    function validarCampoVacio(campo, nombreCampo) {

        const valor = campo.val().trim();

        if (valor === '') {

            mostrarError(
                campo,
                '* Este campo no puede estar vacío.'
            );

            return false;
        }

        return true;
    }


    // =====================================================
// VALIDAR NOMBRE
// =====================================================

function validarNombre(campo) {

    const nombre = campo.val().trim();

    // ================================================
    // VACÍO
    // ================================================

    if (nombre === '') {

        mostrarError(
            campo,
            '* Este campo no puede estar vacío.'
        );

        return false;
    }

    // ================================================
    // MÁXIMO 25 CARACTERES
    // ================================================

    if (nombre.length > 25) {

        mostrarError(
            campo,
            'Máximo 25 caracteres.'
        );

        return false;
    }

    // ================================================
    // SOLO LETRAS
    // ================================================

    if (!regexServicio.test(nombre)) {

        mostrarError(
            campo,
            'Solo se aceptan letras.'
        );

        return false;
    }

    // ================================================
    // CORRECTO
    // ================================================

    quitarError(campo);

    campo.addClass('is-valid');

    return true;
}


    // =====================================================
    // VALIDAR PRECIO
    // =====================================================

    function validarPrecio(campo) {

        const precio = campo.val().trim();


        // ================================================
        // VACÍO
        // ================================================

        if (precio === '') {

            mostrarError(
                campo,
                '* Este campo no puede estar vacío.'
            );

            return false;
        }


        // ================================================
        // FORMATO
        // ================================================

        if (!regexPrecio.test(precio)) {

            mostrarError(
                campo,
                'Ingrese un precio válido.'
            );

            return false;
        }


        // ================================================
        // MAYOR QUE CERO
        // ================================================

        if (parseFloat(precio) <= 0) {

            mostrarError(
                campo,
                'El precio debe ser mayor que cero.'
            );

            return false;
        }


        // ================================================
        // CORRECTO
        // ================================================

        quitarError(campo);

        campo.addClass('is-valid');

        return true;
    }


    // =====================================================
    // BLOQUEAR CARACTERES EN NOMBRE
    // =====================================================

    $('#nombre_servicio, #edit_nombre_servicio')
        .on('keydown', function (e) {

            const campo = $(this);
            const valor = campo.val();


            // ---------------------------------------------
            // TECLAS DE CONTROL
            // ---------------------------------------------

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


            // ---------------------------------------------
            // BLOQUEAR SI YA LLEGÓ A 25
            // ---------------------------------------------

            if (valor.length >= 25) {

                e.preventDefault();

                mostrarError(
                    campo,
                    'Máximo 25 caracteres.'
                );

                return;
            }


            // ---------------------------------------------
            // SOLO LETRAS Y ESPACIO
            // ---------------------------------------------

            if (
                e.key.length === 1 &&
                !/^[a-zA-ZÁÉÍÓÚáéíóúñÑ\s]$/.test(e.key)
            ) {

                e.preventDefault();

                mostrarError(
                    campo,
                    'Solo se aceptan letras.'
                );

                return;
            }

        });


    // =====================================================
    // PEGAR TEXTO EN NOMBRE
    // =====================================================

    $('#nombre_servicio, #edit_nombre_servicio')
        .on('paste', function (e) {

            const campo = $(this);

            const texto =
                (e.originalEvent.clipboardData ||
                 window.clipboardData)
                .getData('text');


            // Si contiene caracteres inválidos
            if (!regexServicio.test(texto)) {

                e.preventDefault();

                mostrarError(
                    campo,
                    'Solo se aceptan letras.'
                );

                return;
            }


            // Si supera 25 caracteres
            if (
                campo.val().length +
                texto.length > 25
            ) {

                e.preventDefault();

                mostrarError(
                    campo,
                    'Máximo 25 caracteres.'
                );

                return;
            }

        });


    $('#precio, #edit_precio')
    .on('keydown', function (e) {

        const campo = $(this);
        const valor = campo.val();

        // ---------------------------------------------
        // TECLAS DE CONTROL
        // ---------------------------------------------

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

        // ---------------------------------------------
        // MÁXIMO 25 CARACTERES
        // ---------------------------------------------

        if (valor.length >= 25) {

            e.preventDefault();

            mostrarError(
                campo,
                'Máximo 25 caracteres.'
            );

            return;
        }

        // ---------------------------------------------
        // SOLO NÚMEROS
        // ---------------------------------------------

        if (/^\d$/.test(e.key)) {

            // Si ya existe punto
            if (valor.includes('.')) {

                const decimales =
                    valor.split('.')[1];

                // Máximo 2 decimales
                if (
                    decimales.length >= 2 &&
                    campo[0].selectionStart > valor.indexOf('.')
                ) {

                    e.preventDefault();

                    mostrarError(
                        campo,
                        'Solo se permiten 2 decimales.'
                    );

                    return;
                }
            }

            return;
        }

        // ---------------------------------------------
        // PERMITIR UN SOLO PUNTO
        // ---------------------------------------------

        if (e.key === '.') {

            if (valor.includes('.')) {

                e.preventDefault();

                mostrarError(
                    campo,
                    'Solo se permite un punto decimal.'
                );

                return;
            }

            return;
        }

        // ---------------------------------------------
        // BLOQUEAR TODO LO DEMÁS
        // ---------------------------------------------

        e.preventDefault();

        mostrarError(
            campo,
            'Solo se aceptan números.'
        );
    });


    // =====================================================
    // PEGAR EN PRECIO
    // =====================================================

    $('#precio, #edit_precio')
        .on('paste', function (e) {

            const campo = $(this);

            const texto =
                (e.originalEvent.clipboardData ||
                 window.clipboardData)
                .getData('text');


            if (!regexPrecio.test(texto)) {

                e.preventDefault();

                mostrarError(
                    campo,
                    'Solo se aceptan números.'
                );

                return;
            }

        });


    // =====================================================
    // VALIDAR PRECIO MIENTRAS ESCRIBE
    // =====================================================

    $('#precio, #edit_precio')
        .on('input', function () {

            validarPrecio($(this));

        });


    // =====================================================
    // VALIDAR AL SALIR DEL CAMPO
    // =====================================================

    $('#nombre_servicio, #edit_nombre_servicio')
        .on('blur', function () {

            validarNombre($(this));

        });


    $('#precio, #edit_precio')
        .on('blur', function () {

            validarPrecio($(this));

        });


    // =====================================================
    // REGISTRAR TIPO SERVICIO
    // =====================================================

    $('#formRegistrartiposservicios')
        .on('submit', function (e) {

            e.preventDefault();

            const formulario = $(this);

            const nombre =
                $('#nombre_servicio');

            const precio =
                $('#precio');


            // ---------------------------------------------
            // VALIDAR NOMBRE
            // ---------------------------------------------

            const nombreValido =
                validarNombre(nombre);


            // ---------------------------------------------
            // VALIDAR PRECIO
            // ---------------------------------------------

            const precioValido =
                validarPrecio(precio);


            // ---------------------------------------------
            // DETENER SI HAY ERRORES
            // ---------------------------------------------

            if (!nombreValido || !precioValido) {

                return;
            }


            $.post(
                '/admin?ruta=tiposervicio',
                formulario.serialize(),
                function (res) {

                    alerta(res).then(function () {

                        if (res.icon === 'success') {

                            formulario[0].reset();

                            

                            formulario
                                .find('.is-invalid, .is-valid')
                                .removeClass(
                                    'is-invalid is-valid'
                                );

                            formulario
                                .find('.invalid-feedback')
                                .hide();

                            cerrarModal('#primary');

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

        });


    // =====================================================
    // EDITAR TIPO SERVICIO
    // =====================================================

    $('#formEditarTiposervicio')
        .on('submit', function (e) {

            e.preventDefault();

            const formulario = $(this);

            const nombre =
                $('#edit_nombre_servicio');

            const precio =
                $('#edit_precio');


            // ---------------------------------------------
            // VALIDAR NOMBRE
            // ---------------------------------------------

            const nombreValido =
                validarNombre(nombre);


            // ---------------------------------------------
            // VALIDAR PRECIO
            // ---------------------------------------------

            const precioValido =
                validarPrecio(precio);


            // ---------------------------------------------
            // DETENER SI HAY ERRORES
            // ---------------------------------------------

            if (!nombreValido || !precioValido) {

                return;
            }


            // ---------------------------------------------
            // PARSLEY
            // ---------------------------------------------


            $.post(
                '/admin?ruta=tiposervicio',
                formulario.serialize(),
                function (res) {

                    alerta(res).then(function () {

                        if (res.icon === 'success') {

                            formulario[0].reset();

                            formulario
                                .parsley()
                                .reset();

                            formulario
                                .find('.is-invalid, .is-valid')
                                .removeClass(
                                    'is-invalid is-valid'
                                );

                            formulario
                                .find('.invalid-feedback')
                                .hide();

                            cerrarModal('#modalEditar');

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

        });


    // =====================================================
    // ELIMINAR
    // =====================================================

    $('#formEliminartiposervicio')
        .on('submit', function (e) {

            e.preventDefault();

            $.post(
                '/admin?ruta=tiposervicio',
                $(this).serialize(),
                function (res) {

                    alerta(res).then(function () {

                        cerrarModal(
                            '#modalEliminartiposervicio'
                        );

                        if (
                            res.icon === 'success' ||
                            res.icon === 'warning'
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

        });


    // =====================================================
    // VALIDAR EXISTENCIA
    // =====================================================

    $('#nombre_servicio, #edit_nombre_servicio')
        .on('blur', function () {

            const campo = $(this);

            const nombre =
                campo.val().trim();


            if (nombre === '') {
                return;
            }


            if (!regexServicio.test(nombre)) {
                return;
            }


            $.post(
                '/admin?ruta=tiposervicio',
                {
                    buscar: nombre
                },
                function (response) {

                    if (
                        response &&
                        response.existe
                    ) {

                        mostrarError(
                            campo,
                            'El tipo de servicio ya se encuentra registrado.'
                        );

                    }

                },
                'json'
            );

        });


    // =====================================================
    // CERRAR MODAL
    // =====================================================

    function cerrarModal(id) {

        $(id).modal('hide');

        $(id).on(
            'hidden.bs.modal',
            function () {

                $('.modal-backdrop').remove();

                $('body')
                    .removeClass('modal-open');

                $(this)
                    .off('hidden.bs.modal');

            }
        );
    }


    // =====================================================
    // ALERTA
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

    const modalEditar =
        document.getElementById('modalEditar');

    if (modalEditar) {

        modalEditar.addEventListener(
            'show.bs.modal',
            function (event) {

                const button =
                    event.relatedTarget;

                const cod =
                    button.getAttribute(
                        'data-cod_tipo_servicio'
                    );

                const nombre =
                    button.getAttribute(
                        'data-nombre_servicio'
                    );

                const precio =
                    button.getAttribute(
                        'data-precio'
                    );

                const status =
                    button.getAttribute(
                        'data-status'
                    );

                const form =
                    modalEditar.querySelector('form');


                if (form) {

                    form.querySelector(
                        '#edit_cod_tipo_servicio'
                    ).value = cod;

                    form.querySelector(
                        '#edit_nombre_servicio'
                    ).value = nombre;

                    form.querySelector(
                        '#edit_precio'
                    ).value = precio;

                    form.querySelector(
                        '#edit_estado'
                    ).value = status;


                    $('#edit_nombre_servicio')
                        .removeClass(
                            'is-invalid is-valid'
                        );

                    $('#edit_precio')
                        .removeClass(
                            'is-invalid is-valid'
                        );

                    $('#modalEditar .invalid-feedback')
                        .hide();
                }

            }
        );
    }


    // =====================================================
    // MODAL ELIMINAR
    // =====================================================

    const modalEliminar =
        document.getElementById(
            'modalEliminartiposservicio'
        );

    if (modalEliminar) {

        modalEliminar.addEventListener(
            'show.bs.modal',
            function (event) {

                const button =
                    event.relatedTarget;

                const cod =
                    button.getAttribute(
                        'data-cod_tipo_servicio'
                    );

                const form =
                    document.getElementById(
                        'formEliminartiposervicio'
                    );

                if (form) {

                    form.querySelector(
                        '#delete_cod_tipo_servicio'
                    ).value = cod;

                }

            }
        );
    }



});