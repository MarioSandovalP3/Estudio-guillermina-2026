console.log('Abrio presentacion.js');

$(document).ready(function () {

    const regexPresentacion = /^[a-zA-ZÁÉÍÓÚáéíóúÑñ\s]+$/;
    const regexNoPermitidosPresentacion = /[^a-zA-ZÁÉÍÓÚáéíóúÑñ\s]/g;

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

    function ocultarError(input) {
        const $input = $(input);

        $input.removeClass('is-invalid').addClass('is-valid');
        $input.next('.invalid-feedback').hide();
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

    $('#presentacion_reg, #presentacion_edit').on('keydown', function (e) {
        if (e.key.length !== 1) {
            return;
        }

        if (!/^[a-zA-ZÁÉÍÓÚáéíóúÑñ\s]$/.test(e.key)) {
            e.preventDefault();

            mostrarError(
                this,
                'En este campo solo se permiten letras.'
            );
        }
    });

    $('#presentacion_reg, #presentacion_edit').on('paste', function (e) {
        const texto = e.originalEvent.clipboardData.getData('text');

        if (!regexPresentacion.test(texto)) {
            e.preventDefault();

            mostrarError(
                this,
                'En este campo solo se permiten letras.'
            );
        }
    });

    $('#presentacion_reg, #presentacion_edit').on('input', function () {
        const valorOriginal = this.value;
        const valorFiltrado = valorOriginal.replace(
            regexNoPermitidosPresentacion,
            ''
        );

        if (valorOriginal !== valorFiltrado) {
            this.value = valorFiltrado;

            mostrarError(
                this,
                'En este campo solo se permiten letras.'
            );

            return;
        }

        if (this.value.trim() === '') {
            $(this).removeClass('is-invalid is-valid');
            $(this).next('.invalid-feedback').hide();
            return;
        }

        if (!regexPresentacion.test(this.value)) {
            mostrarError(
                this,
                'En este campo solo se permiten letras.'
            );
        } else {
            ocultarError(this);
        }

        $(this).parsley().validate();
    });

    $('#formRegistrarPresentacion').on('submit', function (e) {
        e.preventDefault();

        const formulario = $(this);
        const parsley = formulario.parsley();

        if (!parsley.validate()) {
            return false;
        }

        const presentacion = $('#presentacion_reg').val().trim();

        if (!regexPresentacion.test(presentacion)) {
            mostrarError(
                $('#presentacion_reg'),
                'En este campo solo se permiten letras.'
            );
            return false;
        }

        $.post(
            '/admin?ruta=presentacion',
            formulario.serialize(),
            function (res) {
                alerta(res).then(() => {
                    if (res.icon === 'success') {
                        formulario[0].reset();
                        parsley.reset();

                        formulario.find('.is-invalid, .is-valid')
                            .removeClass('is-invalid is-valid');

                        formulario.find('.invalid-feedback').hide();

                        cerrarModal('#modalRegistrarPresentacion');

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

    $('#formEditarPresentacion').on('submit', function (e) {
        e.preventDefault();

        const formulario = $(this);
        const parsley = formulario.parsley();

        if (!parsley.validate()) {
            return false;
        }

        const presentacion = $('#presentacion_edit').val().trim();

        if (!regexPresentacion.test(presentacion)) {
            mostrarError(
                $('#presentacion_edit'),
                'En este campo solo se permiten letras.'
            );
            return false;
        }

        $.post(
            '/admin?ruta=presentacion',
            formulario.serialize(),
            function (res) {
                alerta(res).then(() => {
                    if (res.icon === 'success') {
                        formulario[0].reset();
                        parsley.reset();

                        formulario.find('.is-invalid, .is-valid')
                            .removeClass('is-invalid is-valid');

                        formulario.find('.invalid-feedback').hide();

                        cerrarModal('#modalEditarPresentacion');

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

    $('#formEliminarPresentacion').on('submit', function (e) {
        e.preventDefault();

        $.post(
            '/admin?ruta=presentacion',
            $(this).serialize(),
            function (res) {
                alerta(res).then(() => {
                    if (
                        res.icon === 'success' ||
                        res.icon === 'warning'
                    ) {
                        $('#formEliminarPresentacion')[0].reset();

                        cerrarModal('#modalEliminarPresentacion');

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

    const modalEditarPresentacion = document.getElementById(
        'modalEditarPresentacion'
    );

    if (modalEditarPresentacion) {
        modalEditarPresentacion.addEventListener(
            'show.bs.modal',
            function (event) {
                const button = event.relatedTarget;

                const cod_presentacion =
                    button.getAttribute('data-cod_presentacion');

                const presentacion =
                    button.getAttribute('data-presentacion');

                const status =
                    button.getAttribute('data-status');

                const formEditar =
                    modalEditarPresentacion.querySelector('form');

                if (formEditar) {
                    formEditar.querySelector(
                        '#cod_presentacion_edit'
                    ).value = cod_presentacion;

                    formEditar.querySelector(
                        '#presentacion_edit'
                    ).value = presentacion;

                    formEditar.querySelector(
                        '#status_presentacion_edit'
                    ).value = status;
                }
            }
        );
    }

    const modalEliminarPresentacion = document.getElementById(
        'modalEliminarPresentacion'
    );

    if (modalEliminarPresentacion) {
        modalEliminarPresentacion.addEventListener(
            'show.bs.modal',
            function (event) {
                const button = event.relatedTarget;

                const cod_presentacion =
                    button.getAttribute('data-cod_presentacion');

                const presentacion =
                    button.getAttribute('data-presentacion');

                const formEliminar =
                    document.getElementById(
                        'formEliminarPresentacion'
                    );

                if (formEliminar) {
                    formEliminar.querySelector(
                        '#cod_presentacion_eliminar'
                    ).value = cod_presentacion;
                }

                modalEliminarPresentacion.querySelector(
                    '#nombre_presentacion'
                ).textContent = presentacion;
            }
        );
    }

    $('#modalRegistrarPresentacion').on(
        'hidden.bs.modal',
        function () {
            const formulario =
                $('#formRegistrarPresentacion');

            formulario[0].reset();
            formulario.parsley().reset();

            formulario.find('.is-invalid, .is-valid')
                .removeClass('is-invalid is-valid');

            formulario.find('.parsley-error, .parsley-success')
                .removeClass('parsley-error parsley-success');

            formulario.find('.invalid-feedback').remove();
            formulario.find('.parsley-errors-list').remove();
        }
    );

    $('#modalEditarPresentacion').on(
        'hidden.bs.modal',
        function () {
            const formulario =
                $('#formEditarPresentacion');

            formulario[0].reset();
            formulario.parsley().reset();

            formulario.find('.is-invalid, .is-valid')
                .removeClass('is-invalid is-valid');

            formulario.find('.parsley-error, .parsley-success')
                .removeClass('parsley-error parsley-success');

            formulario.find('.invalid-feedback').remove();
            formulario.find('.parsley-errors-list').remove();
        }
    );

    $('#presentacion_reg, #presentacion_edit').on(
        'blur',
        function () {
            const campo = $(this);
            const buscar = campo.val().trim();

            if (buscar === '') {
                return;
            }

            const datos = {
                buscar: buscar
            };

            if (campo.attr('id') === 'presentacion_edit') {
                datos.cod_presentacion =
                    $('#cod_presentacion_edit').val();
            }

            $.post(
                '/admin?ruta=presentacion',
                datos,
                function (response) {
                    if (response.existe === true) {
                        Swal.fire({
                            title: 'Advertencia',
                            text: 'La presentación ya se encuentra registrada',
                            icon: 'warning'
                        }).then(function () {
                            campo.val('').focus();
                            campo.removeClass(
                                'is-invalid is-valid'
                            );
                            campo.next(
                                '.invalid-feedback'
                            ).hide();
                        });
                    }
                },
                'json'
            );
        }
    );

    $(document).on(
        'input',
        '#formRegistrarPresentacion input[maxlength], #formEditarPresentacion input[maxlength]',
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
                if (regexPresentacion.test(this.value)) {
                    feedback.hide();

                    $(this)
                        .removeClass('is-invalid')
                        .addClass('is-valid');
                }
            }
        }
    );

    if (window.Parsley) {
        window.Parsley.on('field:error', function () {
            this.$element
                .addClass('is-invalid')
                .removeClass('is-valid');

            let feedback =
                this.$element.next('.invalid-feedback');

            if (!feedback.length) {
                feedback =
                    $('<div class="invalid-feedback"></div>');

                this.$element.after(feedback);
            }

            feedback
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

});