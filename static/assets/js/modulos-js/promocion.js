console.log("Abrió promociones");

const regexPromo = /^[a-zA-ZÁÉÍÓÚáéíóúñÑ0-9\s]+$/;
const regexNumero = /^[0-9]+$/;
const extensionesImagen = ['jpg', 'jpeg', 'png', 'webp'];

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
            .css('color', 'red')
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

        // MÁXIMO 100
        if (nombre.length > 100) {

            mostrarError(
                campo,
                'Máximo 100 caracteres.'
            );

            return false;
        }

        // SOLO LETRAS Y NÚMEROS
        if (!regexPromo.test(nombre)) {

            mostrarError(
                campo,
                'Solo se aceptan letras y números.'
            );

            return false;
        }

        quitarError(campo);

        campo.addClass('is-valid');

        return true;
    }


    // =====================================================
    // VALIDAR DESCRIPCIÓN
    // =====================================================

    function validarDescripcion(campo) {

        const descripcion = campo.val();

        if (descripcion.length > 250) {

            mostrarError(
                campo,
                'Máximo 250 caracteres.'
            );

            return false;
        }

        quitarError(campo);

        if (descripcion.length > 0) {
            campo.addClass('is-valid');
        }

        return true;
    }


    // =====================================================
    // VALIDAR DESCUENTO
    // =====================================================

    function validarDescuento(campo) {

        const descuento = campo.val().trim();

        // VACÍO
        if (descuento === '') {

            mostrarError(
                campo,
                '* Este campo no puede estar vacío.'
            );

            return false;
        }

        // SOLO NÚMEROS
        if (!regexNumero.test(descuento)) {

            mostrarError(
                campo,
                'Solo se aceptan números.'
            );

            return false;
        }

        // MÁXIMO 3 CARACTERES
        if (descuento.length > 3) {

            mostrarError(
                campo,
                'Máximo 3 caracteres.'
            );

            return false;
        }

        // MÁXIMO 100%
        if (parseInt(descuento) > 100) {

            mostrarError(
                campo,
                'El descuento no puede ser mayor a 100%.'
            );

            return false;
        }

        quitarError(campo);

        campo.addClass('is-valid');

        return true;
    }


    // =====================================================
    // VALIDAR IMAGEN
    // =====================================================

    function validarImagen(campo, obligatoria = false) {

        const archivo = campo[0].files[0];

        // Si no hay imagen
        if (!archivo) {

            if (obligatoria) {

                mostrarError(
                    campo,
                    '* Este campo no puede estar vacío.'
                );

                return false;
            }

            quitarError(campo);

            return true;
        }

        // Obtener extensión
        const nombreArchivo = archivo.name;

        const extension = nombreArchivo
            .split('.')
            .pop()
            .toLowerCase();

        // Validar extensión
        if (!extensionesImagen.includes(extension)) {

            mostrarError(
                campo,
                'Solo se permiten imágenes JPG, JPEG, PNG o WEBP.'
            );

            campo.val('');

            return false;
        }

        // Validar MIME
        const tiposPermitidos = [
            'image/jpeg',
            'image/png',
            'image/webp'
        ];

        if (!tiposPermitidos.includes(archivo.type)) {

            mostrarError(
                campo,
                'El formato de imagen no es válido.'
            );

            campo.val('');

            return false;
        }

        quitarError(campo);

        campo.addClass('is-valid');

        return true;
    }


    // =====================================================
    // OBTENER FECHA ACTUAL
    // =====================================================

    function obtenerFechaHoy() {

        const hoy = new Date();

        const año = hoy.getFullYear();

        const mes = String(
            hoy.getMonth() + 1
        ).padStart(2, '0');

        const dia = String(
            hoy.getDate()
        ).padStart(2, '0');

        return `${año}-${mes}-${dia}`;
    }


    // =====================================================
    // CONFIGURAR FECHA DE INICIO
    // =====================================================

    const fechaHoy = obtenerFechaHoy();

    $('#inicio_promo, #edit_inicio_promo')
        .attr('min', fechaHoy);


    // =====================================================
    // VALIDAR FECHA INICIO
    // =====================================================

    function validarFechaInicio(campo) {

        const fecha = campo.val();

        if (fecha === '') {

            mostrarError(
                campo,
                '* Este campo no puede estar vacío.'
            );

            return false;
        }

        if (fecha < fechaHoy) {

            mostrarError(
                campo,
                'La fecha de inicio no puede ser anterior a hoy.'
            );

            return false;
        }

        quitarError(campo);

        campo.addClass('is-valid');

        return true;
    }


    // =====================================================
    // VALIDAR FECHA FIN
    // =====================================================

    function validarFechaFin(campo, campoInicio) {

        const fechaFin = campo.val();

        const fechaInicio = campoInicio.val();

        if (fechaFin === '') {

            mostrarError(
                campo,
                '* Este campo no puede estar vacío.'
            );

            return false;
        }

        if (fechaFin < fechaHoy) {

            mostrarError(
                campo,
                'La fecha no puede ser anterior a hoy.'
            );

            return false;
        }

        if (
            fechaInicio !== '' &&
            fechaFin < fechaInicio
        ) {

            mostrarError(
                campo,
                'La fecha de finalización no puede ser anterior a la fecha de inicio.'
            );

            return false;
        }

        quitarError(campo);

        campo.addClass('is-valid');

        return true;
    }


    // =====================================================
    // NOMBRE - BLOQUEAR CARACTERES
    // =====================================================

    $('#nombre_promo, #edit_nombre_promo')
        .on('keydown', function (e) {

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

            // MÁXIMO 100
            if (valor.length >= 100) {

                e.preventDefault();

                mostrarError(
                    campo,
                    'Máximo 100 caracteres.'
                );

                return;
            }

            // SOLO LETRAS, NÚMEROS Y ESPACIOS
            if (
                e.key.length === 1 &&
                !/^[a-zA-ZÁÉÍÓÚáéíóúñÑ0-9\s]$/.test(e.key)
            ) {

                e.preventDefault();

                mostrarError(
                    campo,
                    'Solo se aceptan letras y números.'
                );
            }

        });


    // =====================================================
    // NOMBRE - PEGAR
    // =====================================================

    $('#nombre_promo, #edit_nombre_promo')
        .on('paste', function (e) {

            const campo = $(this);

            const texto =
                (e.originalEvent.clipboardData ||
                 window.clipboardData)
                .getData('text');

            if (!regexPromo.test(texto)) {

                e.preventDefault();

                mostrarError(
                    campo,
                    'Solo se aceptan letras y números.'
                );

                return;
            }

            if (
                campo.val().length +
                texto.length > 100
            ) {

                e.preventDefault();

                mostrarError(
                    campo,
                    'Máximo 100 caracteres.'
                );
            }

        });


    // =====================================================
    // NOMBRE - INPUT
    // =====================================================

    $('#nombre_promo, #edit_nombre_promo')
        .on('input', function () {

            validarNombre($(this));

        });


    // =====================================================
    // DESCRIPCIÓN - INPUT
    // =====================================================

    $('#descripcion_promo, #edit_descripcion_promo')
        .on('input', function () {

            const campo = $(this);

            // Cortar automáticamente a 250
            if (campo.val().length > 250) {

                campo.val(
                    campo.val().substring(0, 250)
                );
            }

            validarDescripcion(campo);

        });


    // =====================================================
    // DESCRIPCIÓN - PEGAR
    // =====================================================

    $('#descripcion_promo, #edit_descripcion_promo')
        .on('paste', function (e) {

            const campo = $(this);

            const texto =
                (e.originalEvent.clipboardData ||
                 window.clipboardData)
                .getData('text');

            if (
                campo.val().length +
                texto.length > 250
            ) {

                e.preventDefault();

                mostrarError(
                    campo,
                    'Máximo 250 caracteres.'
                );
            }

        });


    // =====================================================
    // DESCUENTO - BLOQUEAR CARACTERES
    // =====================================================

    $('#descuento, #edit_descuento')
        .on('keydown', function (e) {

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

            // SOLO NÚMEROS
            if (!/^\d$/.test(e.key)) {

                e.preventDefault();

                mostrarError(
                    campo,
                    'Solo se aceptan números.'
                );

                return;
            }

            // MÁXIMO 3
            if (valor.length >= 3) {

                e.preventDefault();

                mostrarError(
                    campo,
                    'Máximo 3 caracteres.'
                );

                return;
            }

        });


    // =====================================================
    // DESCUENTO - INPUT
    // =====================================================

    $('#descuento, #edit_descuento')
        .on('input', function () {

            const campo = $(this);

            // Eliminar cualquier cosa que no sea número
            campo.val(
                campo.val().replace(/[^0-9]/g, '')
            );

            // Máximo 3 caracteres
            if (campo.val().length > 3) {

                campo.val(
                    campo.val().substring(0, 3)
                );
            }

            validarDescuento(campo);

        });


    // =====================================================
    // DESCUENTO - PEGAR
    // =====================================================

    $('#descuento, #edit_descuento')
        .on('paste', function (e) {

            const campo = $(this);

            const texto =
                (e.originalEvent.clipboardData ||
                 window.clipboardData)
                .getData('text');

            if (!regexNumero.test(texto)) {

                e.preventDefault();

                mostrarError(
                    campo,
                    'Solo se aceptan números.'
                );

                return;
            }

            if (
                campo.val().length +
                texto.length > 3
            ) {

                e.preventDefault();

                mostrarError(
                    campo,
                    'Máximo 3 caracteres.'
                );
            }

        });


    // =====================================================
    // IMAGEN
    // =====================================================

    $('#imagen_promo, #edit_imagen_promo')
        .on('change', function () {

            validarImagen(
                $(this),
                false
            );

        });


    // =====================================================
    // FECHA INICIO
    // =====================================================

    $('#inicio_promo, #edit_inicio_promo')
        .on('change', function () {

            const campo = $(this);

            validarFechaInicio(campo);

            // Actualizar mínimo de fecha fin
            const fechaFin =
                campo.attr('id') === 'inicio_promo'
                    ? $('#fin_promo')
                    : $('#edit_fin_promo');

            if (campo.val() !== '') {

                fechaFin.attr(
                    'min',
                    campo.val()
                );
            }

        });


    // =====================================================
    // FECHA FIN
    // =====================================================

    $('#fin_promo, #edit_fin_promo')
        .on('change', function () {

            const campo = $(this);

            const campoInicio =
                campo.attr('id') === 'fin_promo'
                    ? $('#inicio_promo')
                    : $('#edit_inicio_promo');

            validarFechaFin(
                campo,
                campoInicio
            );

        });


    // =====================================================
    // BLUR NOMBRE
    // =====================================================

    $('#nombre_promo, #edit_nombre_promo')
        .on('blur', function () {

            const campo = $(this);

            validarNombre(campo);

            const nombre =
                campo.val().trim();

            if (
                nombre === '' ||
                !regexPromo.test(nombre)
            ) {
                return;
            }

            $.post(
                '/admin?ruta=promocion',
                {
                    buscar: nombre
                },
                function (res) {

                    if (res.existe) {

                        mostrarError(
                            campo,
                            'La promoción ya existe.'
                        );

                    }

                },
                'json'
            );

        });


    // =====================================================
    // REGISTRAR
    // =====================================================

    $('#formRegistrarPromocion')
        .on('submit', function (e) {

            e.preventDefault();

            const form = this;

            const formulario = $(form);

            const btn =
                formulario.find(
                    'button[type="submit"]'
                );


            // =============================================
            // VALIDACIONES
            // =============================================

            const nombreValido =
                validarNombre(
                    formulario.find(
                        '#nombre_promo'
                    )
                );

            const descripcionValida =
                validarDescripcion(
                    formulario.find(
                        '#descripcion_promo'
                    )
                );

            const descuentoValido =
                validarDescuento(
                    formulario.find(
                        '#descuento'
                    )
                );

            const imagenValida =
                validarImagen(
                    formulario.find(
                        '#imagen_promo'
                    ),
                    false
                );

            const fechaInicioValida =
                validarFechaInicio(
                    formulario.find(
                        '#inicio_promo'
                    )
                );

            const fechaFinValida =
                validarFechaFin(
                    formulario.find(
                        '#fin_promo'
                    ),
                    formulario.find(
                        '#inicio_promo'
                    )
                );


            // =============================================
            // DETENER SI HAY ERROR
            // =============================================

            if (
                !nombreValido ||
                !descripcionValida ||
                !descuentoValido ||
                !imagenValida ||
                !fechaInicioValida ||
                !fechaFinValida
            ) {

                return;
            }


            // =============================================
            // DESACTIVAR BOTÓN
            // =============================================

            btn.prop(
                'disabled',
                true
            );


            // =============================================
            // ENVIAR
            // =============================================

            const formData =
                new FormData(form);

            $.ajax({

                url:
                    '/admin?ruta=promocion',

                type: 'POST',

                data: formData,

                processData: false,

                contentType: false,

                dataType: 'json',

                success: function (res) {

                    alerta(res)
                        .then(function () {

                            if (
                                res.icon ===
                                'success'
                            ) {

                                form.reset();

                                formulario
                                    .find(
                                        '.is-invalid, .is-valid'
                                    )
                                    .removeClass(
                                        'is-invalid is-valid'
                                    );

                                formulario
                                    .find(
                                        '.invalid-feedback'
                                    )
                                    .hide();

                                cerrarModal(
                                    '#modalRegistrarPromocion'
                                );

                                $('#table1')
                                    .load(
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

                error: function () {

                    btn.prop(
                        'disabled',
                        false
                    );

                    mostrarError(
                        formulario.find(
                            '#nombre_promo'
                        ),
                        'Ocurrió un error al procesar la solicitud.'
                    );
                }

            });

        });


    // =====================================================
    // EDITAR
    // =====================================================

    $('#formEditarPromocion')
        .on('submit', function (e) {

            e.preventDefault();

            const form = this;

            const formulario = $(form);

            const btn =
                formulario.find(
                    'button[type="submit"]'
                );


            const nombreValido =
                validarNombre(
                    formulario.find(
                        '#edit_nombre_promo'
                    )
                );

            const descripcionValida =
                validarDescripcion(
                    formulario.find(
                        '#edit_descripcion_promo'
                    )
                );

            const descuentoValido =
                validarDescuento(
                    formulario.find(
                        '#edit_descuento'
                    )
                );

            const imagenValida =
                validarImagen(
                    formulario.find(
                        '#edit_imagen_promo'
                    ),
                    false
                );

            const fechaInicioValida =
                validarFechaInicio(
                    formulario.find(
                        '#edit_inicio_promo'
                    )
                );

            const fechaFinValida =
                validarFechaFin(
                    formulario.find(
                        '#edit_fin_promo'
                    ),
                    formulario.find(
                        '#edit_inicio_promo'
                    )
                );


            if (
                !nombreValido ||
                !descripcionValida ||
                !descuentoValido ||
                !imagenValida ||
                !fechaInicioValida ||
                !fechaFinValida
            ) {

                return;
            }


            btn.prop(
                'disabled',
                true
            );


            const formData =
                new FormData(form);


            $.ajax({

                url:
                    '/admin?ruta=promocion',

                type: 'POST',

                data: formData,

                processData: false,

                contentType: false,

                dataType: 'json',

                success: function (res) {

                    alerta(res)
                        .then(function () {

                            if (
                                res.icon ===
                                'success'
                            ) {

                                form.reset();

                                formulario
                                    .find(
                                        '.is-invalid, .is-valid'
                                    )
                                    .removeClass(
                                        'is-invalid is-valid'
                                    );

                                formulario
                                    .find(
                                        '.invalid-feedback'
                                    )
                                    .hide();

                                cerrarModal(
                                    '#modalEditarPromocion'
                                );

                                $('#table1')
                                    .load(
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

                error: function () {

                    btn.prop(
                        'disabled',
                        false
                    );

                }

            });

        });


    // =====================================================
    // ELIMINAR
    // =====================================================

    $('#formEliminarPromocion')
        .on('submit', function (e) {

            e.preventDefault();

            $.post(
                '/admin?ruta=promocion',
                $(this).serialize(),
                function (res) {

                    alerta(res)
                        .then(function () {

                            cerrarModal(
                                '#modalEliminarPromocion'
                            );

                            if (
                                res.icon ===
                                'success'
                            ) {

                                $('#table1')
                                    .load(
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
    // MODAL EDITAR
    // =====================================================

    const modalEditar =
        document.getElementById(
            'modalEditarPromocion'
        );

    if (modalEditar) {

        modalEditar.addEventListener(
            'show.bs.modal',
            function (event) {

                const b =
                    event.relatedTarget;

                $('#edit_cod_promo')
                    .val(
                        b.dataset.cod_promo
                    );

                $('#edit_nombre_promo')
                    .val(
                        b.dataset.nombre_promo
                    );

                $('#edit_descripcion_promo')
                    .val(
                        b.dataset.descripcion_promo
                    );

                $('#edit_descuento')
                    .val(
                        b.dataset.descuento
                    );

                $('#edit_inicio_promo')
                    .val(
                        b.dataset.inicio_promo
                    );

                $('#edit_fin_promo')
                    .val(
                        b.dataset.fin_promo
                    );

                $('#edit_status')
                    .val(
                        b.dataset.status
                    );


                // Limpiar errores
                $('#modalEditarPromocion')
                    .find(
                        '.is-invalid, .is-valid'
                    )
                    .removeClass(
                        'is-invalid is-valid'
                    );

                $('#modalEditarPromocion')
                    .find(
                        '.invalid-feedback'
                    )
                    .hide();


                // Fecha mínima
                $('#edit_inicio_promo')
                    .attr(
                        'min',
                        fechaHoy
                    );

                if (
                    $('#edit_inicio_promo')
                    .val() !== ''
                ) {

                    $('#edit_fin_promo')
                        .attr(
                            'min',
                            $('#edit_inicio_promo')
                                .val()
                        );
                }

            }
        );
    }


    // =====================================================
    // MODAL ELIMINAR
    // =====================================================

    const modalEliminar =
        document.getElementById(
            'modalEliminarPromocion'
        );

    if (modalEliminar) {

        modalEliminar.addEventListener(
            'show.bs.modal',
            function (event) {

                const b =
                    event.relatedTarget;

                $('#delete_cod_promo')
                    .val(
                        b.dataset.cod_promo
                    );

            }
        );
    }


    // =====================================================
    // MODAL DETALLE
    // =====================================================

    const modalVer =
        document.getElementById(
            'modalVerPromocion'
        );

    if (modalVer) {

        modalVer.addEventListener(
            'show.bs.modal',
            function (event) {

                const b =
                    event.relatedTarget;

                $('#nombre_promocion')
                    .text(
                        b.dataset.nombre
                    );

                $('#descripcion_promocion')
                    .text(
                        b.dataset.descripcion
                    );

                const img =
                    $('#imagen_promocion');


                if (b.dataset.imagen) {

                    img.attr(
                        'src',
                        '/static/assets/img/promociones/' +
                        b.dataset.imagen
                    );

                    img.show();

                } else {

                    img.hide();

                }

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

            timer: 2000,

            showConfirmButton: true,

            confirmButtonText: 'Aceptar',

            backdrop: false

        });

    }


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
                    .removeClass(
                        'modal-open'
                    );

                $(this).off(
                    'hidden.bs.modal'
                );

            }
        );

    }

});