console.log("Abrió marcas");

const regexMarca = /^[a-zA-ZÁÉÍÓÚáéíóúÑñ\s]+$/;
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
    // VALIDAR MARCA
    // =====================================================

    function validarMarca(campo) {

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
        if (!regexMarca.test(valor)) {

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
    // REGISTRAR MARCA
    // =====================================================

    $('#formRegistrarMarca').on('submit', function (e) {

        e.preventDefault();

        const form = this;

        const btn = $(form).find(
            'button[type="submit"]'
        );

        const nombreMarca = $('#nombre_marca');


        // VALIDAR MARCA
        if (!validarMarca(nombreMarca)) {
            return;
        }


        btn.prop('disabled', true);


        $.post(
            '/admin?ruta=marca',
            $(form).serialize(),
            function (res) {

                alerta(res).then(() => {

                    if (res.icon === 'success') {

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

                        cerrarModal('#modalRegistrar');

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

    });


    // =====================================================
    // EDITAR MARCA
    // =====================================================

    $('#formEditarMarca').on('submit', function (e) {

        e.preventDefault();

        const form = this;

        const btn = $(form).find(
            'button[type="submit"]'
        );

        const nombreMarca =
            $('#edit_nombre_marca');


        // VALIDAR MARCA
        if (!validarMarca(nombreMarca)) {
            return;
        }


        btn.prop('disabled', true);


        $.post(
            '/admin?ruta=marca',
            $(form).serialize(),
            function (res) {

                alerta(res).then(() => {

                    if (res.icon === 'success') {

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

                        cerrarModal('#modalEditar');

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

    });


    // =====================================================
    // ELIMINAR MARCA
    // =====================================================

    $('#formEliminarMarca').on('submit', function (e) {

        e.preventDefault();

        $.post(
            '/admin?ruta=marca',
            $(this).serialize(),
            function (res) {

                alerta(res).then(() => {

                    cerrarModal('#modalEliminar');

                    if (res.icon === 'success') {

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
    // BLOQUEAR TECLAS
    // =====================================================

    $(document).on(
        'keydown',
        '#nombre_marca, #edit_nombre_marca',
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


            // MÁXIMO 20
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
        '#nombre_marca, #edit_nombre_marca',
        function (e) {

            const campo = $(this);

            const texto =
                (
                    e.originalEvent.clipboardData ||
                    window.clipboardData
                ).getData('text');


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
            if (!regexMarca.test(texto)) {

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
        '#nombre_marca, #edit_nombre_marca',
        function () {

            const campo = $(this);

            let valor = campo.val();


            // ELIMINAR NÚMEROS Y SIGNOS
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

            validarMarca(campo);

        }
    );


    // =====================================================
    // VALIDAR AL SALIR DEL CAMPO
    // =====================================================

    $(document).on(
        'blur',
        '#nombre_marca, #edit_nombre_marca',
        function () {

            validarMarca($(this));

        }
    );


    // =====================================================
    // VALIDAR EXISTENCIA
    // =====================================================

    let ultimaMarcaConsultada = '';


    $('#nombre_marca, #edit_nombre_marca').blur(function () {

        const buscar = $(this).val().trim();


        if (
            buscar === '' ||
            buscar === ultimaMarcaConsultada
        ) {
            return;
        }


        ultimaMarcaConsultada = buscar;


        $.post(
            '/admin?ruta=marca',
            { buscar },
            function (response) {

                if (response.existe) {

                    Swal.fire({
                        title: 'Advertencia',
                        text: 'La marca ya se encuentra registrada',
                        icon: 'warning'
                    });

                }

            },
            'json'
        );

    });


    // =====================================================
    // CERRAR MODALES
    // =====================================================

    function cerrarModal(id) {

        $(id).modal('hide');

        $(id).on(
            'hidden.bs.modal',
            function () {

                $('.modal-backdrop').remove();

                $('body').removeClass(
                    'modal-open'
                );

                $(this).off(
                    'hidden.bs.modal'
                );

            }
        );

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


                const cod =
                    button.getAttribute(
                        'data-cod_marca'
                    );


                const nombre =
                    button.getAttribute(
                        'data-nombre_marca'
                    );


                const status =
                    button.getAttribute(
                        'data-status'
                    );


                const form =
                    modalEditar.querySelector(
                        'form'
                    );


                if (form) {

                    form.querySelector(
                        '#edit_cod_marca'
                    ).value = cod;


                    form.querySelector(
                        '#edit_nombre_marca'
                    ).value = nombre;


                    form.querySelector(
                        '#edit_status'
                    ).value = status;

                }

            }
        );

    }


    // =====================================================
    // MODAL ELIMINAR
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


                const cod =
                    button.getAttribute(
                        'data-cod_marca'
                    );


                const form =
                    document.getElementById(
                        'formEliminarMarca'
                    );


                if (form) {

                    form.querySelector(
                        '#delete_cod_marca'
                    ).value = cod;

                }

            }
        );

    }

});