console.log('Abrio medida .js');

const regexMedida = /^[a-zA-ZÁÉÍÓÚáéíóúñÑ\s]+$/;
const regexNoPermitidosMedida = /[^a-zA-ZÁÉÍÓÚáéíóúñÑ\s]/g;

$(document).ready(function () {

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

    $('#formRegistrarMedida input, #formEditarMedida input').on('input', function () {
        const originalValue = this.value;
        const valorFiltrado = this.value.replace(regexNoPermitidosMedida, '');

        if (originalValue !== valorFiltrado) {
            this.value = valorFiltrado;
            mostrarError(this, 'En este campo solo se permiten letras.');
            return;
        }

        if (this.value.trim() === '') {
            $(this).removeClass('is-valid is-invalid');
            $(this).next('.invalid-feedback').hide();
            return;
        }

        if (!regexMedida.test(this.value)) {
            mostrarError(this, 'En este campo solo se permiten letras.');
        } else {
            ocultarError(this);
        }

        $(this).parsley().validate();
    });

    $('#formRegistrarMedida input, #formEditarMedida input').on('keydown', function (e) {
        if (e.key.length !== 1) {
            return;
        }

        if (!regexMedida.test(e.key)) {
            e.preventDefault();
            mostrarError(this, 'En este campo solo se permiten letras.');
        }
    });

    $('#formRegistrarMedida input, #formEditarMedida input').on('paste', function (e) {
        const texto = e.originalEvent.clipboardData.getData('text');

        if (!regexMedida.test(texto)) {
            e.preventDefault();
            mostrarError(this, 'En este campo solo se permiten letras.');
        }
    });

    $('#modalRegistrarMedida').on('hidden.bs.modal', function () {
        const form = $('#formRegistrarMedida')[0];

        if (form) {
            form.reset();
        }

        $('#formRegistrarMedida').parsley().reset();

        $(this).find('.is-invalid, .is-valid')
            .removeClass('is-invalid is-valid');

        $(this).find('.invalid-feedback').hide();
    });

    $('#modalEditarMedida').on('hidden.bs.modal', function () {
        const form = $('#formEditarMedida')[0];

        if (form) {
            form.reset();
        }

        $('#formEditarMedida').parsley().reset();

        $(this).find('.is-invalid, .is-valid')
            .removeClass('is-invalid is-valid');

        $(this).find('.invalid-feedback').hide();
    });

    if (window.Parsley) {
        window.Parsley.on('field:error', function () {
            const name = this.$element.attr('name');

            if (name === 'medida' || name === 'medida_edit') {
                this.$element.addClass('is-invalid').removeClass('is-valid');

                let $feedback = this.$element.next('.invalid-feedback');

                if (!$feedback.length) {
                    $feedback = $('<div class="invalid-feedback"></div>');
                    this.$element.after($feedback);
                }

                $feedback.text(this.getErrorsMessages()[0]).show();
            } else {
                this.$element.addClass('is-invalid').removeClass('is-valid');

                let $feedback = this.$element.next('.invalid-feedback');

                if (!$feedback.length) {
                    $feedback = $('<div class="invalid-feedback"></div>');
                    this.$element.after($feedback);
                }

                $feedback.text(this.getErrorsMessages()[0]).show();
            }
        });

        window.Parsley.on('field:success', function () {
            this.$element.removeClass('is-invalid').addClass('is-valid');
            this.$element.next('.invalid-feedback').hide();
        });
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

    $('#formRegistrarMedida').on('submit', function (e) {
        e.preventDefault();

        if (!$(this).parsley().validate()) {
            return;
        }

        const medida = $('#medida_reg').val().trim();

        if (!regexMedida.test(medida)) {
            mostrarError(
                $('#medida_reg'),
                'En este campo solo se permiten letras.'
            );
            return;
        }

        $.post(
            '/admin?ruta=unidadmedida',
            $(this).serialize(),
            function (res) {
                alerta(res).then(() => {
                    if (res.icon === 'success') {
                        $('#formRegistrarMedida')[0].reset();
                        $('#formRegistrarMedida').parsley().reset();
                        $('#formRegistrarMedida')
                            .find('.is-invalid, .is-valid')
                            .removeClass('is-invalid is-valid');
                        $('#formRegistrarMedida')
                            .find('.invalid-feedback')
                            .hide();

                        cerrarModal('#modalRegistrarMedida');

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

    $('#formEditarMedida').on('submit', function (e) {
        e.preventDefault();

        if (!$(this).parsley().validate()) {
            return;
        }

        const medida = $('#medida_edit').val().trim();

        if (!regexMedida.test(medida)) {
            mostrarError(
                $('#medida_edit'),
                'En este campo solo se permiten letras.'
            );
            return;
        }

        $.post(
            '/admin?ruta=unidadmedida',
            $(this).serialize(),
            function (res) {
                alerta(res).then(() => {
                    if (res.icon === 'success') {
                        $('#formEditarMedida')[0].reset();

                        $('#modalEditarMedida .is-invalid, #modalEditarMedida .is-valid')
                            .removeClass('is-invalid is-valid');

                        $('#formEditarMedida').parsley().reset();

                        $('#modalEditarMedida')
                            .find('.invalid-feedback')
                            .hide();

                        cerrarModal('#modalEditarMedida');

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

    $('#formEliminarMedida').on('submit', function (e) {
        e.preventDefault();

        $.post(
            '/admin?ruta=unidadmedida',
            $(this).serialize(),
            function (res) {
                alerta(res).then(() => {
                    if (res.icon === 'success' || res.icon === 'warning') {
                        $('#formEliminarMedida')[0].reset();

                        cerrarModal('#modalEliminarMedida');

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

    const modalEditarMedida = document.getElementById('modalEditarMedida');

    if (modalEditarMedida) {
        modalEditarMedida.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;

            const cod_medida = button.getAttribute('data-cod_medida');
            const medida = button.getAttribute('data-medida');
            const status = button.getAttribute('data-status');

            const formEditar = modalEditarMedida.querySelector('form');

            if (formEditar) {
                formEditar.querySelector('#cod_medida_edit').value = cod_medida;
                formEditar.querySelector('#medida_edit').value = medida;
                formEditar.querySelector('#status_edit').value = status;
            }
        });
    }

    const modalEliminarMedida = document.getElementById('modalEliminarMedida');

    if (modalEliminarMedida) {
        modalEliminarMedida.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;

            const cod_medida = button.getAttribute('data-cod_medida');
            const medida = button.getAttribute('data-medida');

            const formEliminar = document.getElementById('formEliminarMedida');

            if (formEliminar) {
                formEliminar.querySelector('#cod_medida_eliminar').value = cod_medida;
            }

            modalEliminarMedida
                .querySelector('#nombre_medida')
                .textContent = medida;
        });
    }

    $('#medida_reg, #medida_edit').on('blur', function () {
        const campo = $(this);
        const buscar = campo.val().trim();

        if (buscar === '') {
            return;
        }

        const datos = {
            buscar: buscar
        };

        if (campo.attr('id') === 'medida_edit') {
            datos.cod_medida = $('#cod_medida_edit').val();
        }

        $.post(
            '/admin?ruta=unidadmedida',
            datos,
            function (response) {
                if (response.existe === true) {
                    Swal.fire({
                        title: 'Advertencia',
                        text: 'La medida ya se encuentra registrada',
                        icon: 'warning'
                    }).then(function () {
                        campo.val('').focus();
                        campo.removeClass('is-valid is-invalid');
                        campo.next('.invalid-feedback').hide();
                    });
                }
            },
            'json'
        );
    });

    $(document).on(
        'input',
        '#formRegistrarMedida input[maxlength], #formEditarMedida input[maxlength]',
        function () {
            const max = parseInt(this.getAttribute('maxlength'));

            if (!max) {
                return;
            }

            let feedback = $(this).next('.invalid-feedback');

            if (!feedback.length) {
                feedback = $('<div class="invalid-feedback"></div>');
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

                if (regexMedida.test(this.value)) {
                    $(this)
                        .removeClass('is-invalid')
                        .addClass('is-valid');
                }
            }
        }
    );

});