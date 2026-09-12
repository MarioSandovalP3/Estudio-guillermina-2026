console.log('Abrio usuario.js');

const regexRol = /^[a-zA-ZÁÉÍÓÚáéíóúñÑ\s]+$/;
const regexNoPermitidosRol = /[^a-zA-ZÁÉÍÓÚáéíóúñÑ\s]/g;

const regexLetras = /^[a-zA-ZÁÉÍÓÚáéíóúñÑ\s]+$/;
const regexNoPermitidosLetras = /[^a-zA-ZÁÉÍÓÚáéíóúñÑ\s]/g;

const regexDireccion = /^[a-zA-Z0-9ÁÉÍÓÚáéíóúÑñ\s.,#\-\/()]+$/;
const regexNoPermitidosDireccion = /[^a-zA-Z0-9ÁÉÍÓÚáéíóúÑñ\s.,#\-\/()]/g;

const regexPassword = /^[a-zA-Z0-9.,;:!¡¿?!@#$%^&*()\/,.?"'\-_\s\\]+$/;
const regexNoPermitidosPassword = /[^a-zA-Z0-9.,;:!¡¿?!@#$%^&*()\/,.?"'\-_\s\\]/g;

document.addEventListener('DOMContentLoaded', function () {

    function mostrarError(input, mensaje) {
        let feedback = $(input).next('.invalid-feedback');

        if (!feedback.length) {
            feedback = $('<div class="invalid-feedback"></div>');
            $(input).after(feedback);
        }

        $(input)
            .addClass('is-invalid')
            .removeClass('is-valid');

        feedback.text(mensaje).show();

        clearTimeout(input.errorTimer);

        input.errorTimer = setTimeout(function () {
            feedback.hide();
            $(input).removeClass('is-invalid');
        }, 1800);
    }

    const modalEditar = document.getElementById('editModal');

    if (modalEditar) {
        modalEditar.addEventListener('show.bs.modal', function (event) {

            const button = event.relatedTarget;

            const cedula = button.getAttribute('data-cedula');
            const nombre = button.getAttribute('data-nombre');
            const apellido = button.getAttribute('data-apellido');
            const telefono = button.getAttribute('data-telefono');
            const direccion = button.getAttribute('data-direccion');
            const correo = button.getAttribute('data-correo');
            const rol = button.getAttribute('data-rol');
            const status = button.getAttribute('data-status');

            modalEditar.querySelector('#cedula_edit').value = cedula;
            modalEditar.querySelector('#nombre_usuario_edit').value = nombre;
            modalEditar.querySelector('#apellido_usuario_edit').value = apellido;
            modalEditar.querySelector('#telefono_edit').value = telefono;
            modalEditar.querySelector('#direccion_edit').value = direccion;
            modalEditar.querySelector('#correo_edit').value = correo;

            const selectRol = modalEditar.querySelector('#cod_rol_edit');

            Array.from(selectRol.options).forEach(option => {
                option.selected = option.value === rol;
            });

            modalEditar.querySelector('#status_edit').value = status;
        });
    }

    const btnChangePassword = document.getElementById('changePasswordBtn');

    if (btnChangePassword) {
        btnChangePassword.addEventListener('click', function () {

            const passwordField = document.getElementById('passwordField');

            if (passwordField) {
                passwordField.style.display = 'block';
            }
        });
    }

    const tooltipTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );

    tooltipTriggerList.map(function (tooltipTriggerEl) {

        return new bootstrap.Tooltip(tooltipTriggerEl, {
            template:
                '<div class="tooltip" role="tooltip" style="background-color: white; color: black; border: 1px solid black;">' +
                '<div class="tooltip-arrow"></div>' +
                '<div class="tooltip-inner"></div>' +
                '</div>'
        });

    });

    const togglePasswordEdit = document.getElementById('togglePasswordEdit');
    const passwordEditInput = document.getElementById('password_edit');
    const eyeIconEdit = document.getElementById('eyeIconEdit');

    if (togglePasswordEdit && passwordEditInput && eyeIconEdit) {

        togglePasswordEdit.addEventListener('click', function () {

            const type =
                passwordEditInput.getAttribute('type') === 'password'
                    ? 'text'
                    : 'password';

            passwordEditInput.setAttribute('type', type);

            eyeIconEdit.classList.toggle('bi-eye');
            eyeIconEdit.classList.toggle('bi-eye-slash');
        });
    }

    const passwordInput = document.getElementById('password');

    if (passwordInput) {

        const invalidFeedback = passwordInput.nextElementSibling;

        passwordInput.addEventListener('input', function () {

            if (passwordInput.value.length < 6) {

                passwordInput.classList.add('is-invalid');
                passwordInput.classList.remove('is-valid');

                if (invalidFeedback) {
                    invalidFeedback.style.display = 'block';
                }

            } else {

                passwordInput.classList.remove('is-invalid');
                passwordInput.classList.add('is-valid');

                if (invalidFeedback) {
                    invalidFeedback.style.display = 'none';
                }
            }
        });
    }

    const modalEliminar = document.getElementById('deleteModal');

    if (modalEliminar) {

        modalEliminar.addEventListener('show.bs.modal', function (event) {

            const button = event.relatedTarget;

            const cedula = button.getAttribute('data-cedula');
            const nombre = button.getAttribute('data-nombre');

            const formEliminar = document.getElementById('elimodal');

            if (formEliminar) {
                formEliminar.querySelector('#usuariosdCedula').value = cedula;
            }

            modalEliminar.querySelector('#nombreEliminar').textContent = nombre;
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

    $('#fromUsuarios').on('submit', function (e) {

        e.preventDefault();

        if (!$(this).parsley().validate()) {
            return;
        }

        $.post(
            '/admin?ruta=usuarios',
            $(this).serialize(),
            function (res) {

                alerta(res).then(() => {

                    if (res.icon === 'success') {

                        $('#fromUsuarios')[0].reset();
                        $('#fromUsuarios').parsley().reset();

                        cerrarModal('#primary');

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

    $('#formEditarusuario').on('submit', function (e) {

        e.preventDefault();

        if (!$(this).parsley().validate()) {
            return;
        }

        $.post(
            '/admin?ruta=usuarios',
            $(this).serialize(),
            function (res) {

                alerta(res).then(() => {

                    if (res.icon === 'success') {

                        $('#formEditarusuario')[0].reset();
                        $('#formEditarusuario').parsley().reset();

                        cerrarModal('#editModal');

                        $('#table1').load(
                            location.href + ' #table1>*'
                        );
                    }
                });
            },
            'json'
        );
    });

    $('#elimodal').on('submit', function (e) {

        e.preventDefault();

        $.post(
            '/admin?ruta=usuarios',
            $(this).serialize(),
            function (res) {

                alerta(res).then(() => {

                    if (
                        res.icon === 'success' ||
                        res.icon === 'warning'
                    ) {

                        $('#elimodal')[0].reset();

                        cerrarModal('#deleteModal');

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

    $('#btnCerrarModal').on('click', function () {

        const form = $('#fromUsuarios');

        form[0].reset();

        form.find('.is-invalid, .is-valid')
            .removeClass('is-invalid is-valid');

        form.find('.invalid-feedback').hide();

        form.parsley().reset();
    });

    $('#btnCerrar, #btnClose').on('click', function () {

        const form = $('#formEditarusuario');

        form.find('.is-invalid, .is-valid')
            .removeClass('is-invalid is-valid');

        form.find('.invalid-feedback').hide();

        form.parsley().reset();
    });

    $('#fromUsuarios').parsley();
    $('#formEditarusuario').parsley();

    $(document).on(
        'keydown',
        '#fromUsuarios input, #formEditarusuario input',
        function (e) {

            const name = this.name;

            if (
                name === 'correo' ||
                name === 'correo_reg' ||
                name === 'correo_edit'
            ) {
                return;
            }

            let regexPermitido = null;
            let mensaje = 'Caracter no permitido.';

            if (name === 'cedula' || name === 'telefono') {

                regexPermitido = /^[0-9]$/;
                mensaje = 'Solo se permiten números.';

            } else if (
                name === 'nombre_usuario' ||
                name === 'apellido_usuario'
            ) {

                regexPermitido = /^[a-zA-ZÁÉÍÓÚáéíóúñÑ\s]$/;
                mensaje = 'Solo se permiten letras.';

            } else if (name === 'direccion') {

                regexPermitido =
                    /^[a-zA-Z0-9ÁÉÍÓÚáéíóúÑñ\s.,#\-\/()]$/;

                mensaje =
                    'Solo se permiten letras, números y signos básicos.';

            } else if (
                name === 'password' ||
                name === 'password_edit'
            ) {

                regexPermitido =
                    /^[a-zA-Z0-9.,;:!¡¿?!@#$%^&*()\/,.?"'\-_\s\\]$/;

                mensaje =
                    'Caracter no permitido en la contraseña.';
            }

            if (
                regexPermitido &&
                e.key.length === 1 &&
                !regexPermitido.test(e.key)
            ) {

                e.preventDefault();

                mostrarError(this, mensaje);

                return;
            }

            if (
                (name === 'cedula' && this.value.length >= 10) ||
                (name === 'telefono' && this.value.length >= 12)
            ) {

                if (
                    e.key.length === 1 &&
                    !e.ctrlKey &&
                    !e.metaKey
                ) {

                    e.preventDefault();

                    mostrarError(
                        this,
                        'Límite de caracteres alcanzado.'
                    );
                }
            }
        }
    );

    $(document).on(
        'paste',
        '#fromUsuarios input, #formEditarusuario input',
        function (e) {

            const name = this.name;

            if (
                name === 'correo' ||
                name === 'correo_reg' ||
                name === 'correo_edit'
            ) {
                return;
            }

            let regexPermitido = null;
            let mensaje = 'Caracter no permitido.';

            if (name === 'cedula' || name === 'telefono') {

                regexPermitido = /^[0-9]+$/;
                mensaje = 'Solo se permiten números.';

            } else if (
                name === 'nombre_usuario' ||
                name === 'apellido_usuario'
            ) {

                regexPermitido =
                    /^[a-zA-ZÁÉÍÓÚáéíóúñÑ\s]+$/;

                mensaje = 'Solo se permiten letras.';

            } else if (name === 'direccion') {

                regexPermitido =
                    /^[a-zA-Z0-9ÁÉÍÓÚáéíóúÑñ\s.,#\-\/()]+$/;

                mensaje =
                    'Solo se permiten letras, números y signos básicos.';

            } else if (
                name === 'password' ||
                name === 'password_edit'
            ) {

                regexPermitido =
                    /^[a-zA-Z0-9.,;:!¡¿?!@#$%^&*()\/,.?"'\-_\s\\]+$/;

                mensaje =
                    'Caracter no permitido en la contraseña.';
            }

            if (!regexPermitido) {
                return;
            }

            const texto =
                e.originalEvent.clipboardData.getData('text');

            if (!regexPermitido.test(texto)) {

                e.preventDefault();

                mostrarError(this, mensaje);

                return;
            }

            let max = null;

            if (name === 'cedula') {
                max = 10;
            } else if (name === 'telefono') {
                max = 12;
            } else if (
                name === 'nombre_usuario' ||
                name === 'apellido_usuario'
            ) {
                max = 12;
            } else if (name === 'direccion') {
                max = 40;
            }

            if (max) {

                const seleccion =
                    this.selectionEnd - this.selectionStart;

                if (
                    this.value.length -
                    seleccion +
                    texto.length >
                    max
                ) {

                    e.preventDefault();

                    mostrarError(
                        this,
                        'Límite de ' + max + ' caracteres alcanzado.'
                    );
                }
            }
        }
    );

    $('#fromUsuarios input, #formEditarusuario input').on(
        'input',
        function () {

            const name = this.name;

            if (
                name === 'correo' ||
                name === 'correo_reg' ||
                name === 'correo_edit'
            ) {
                return;
            }

            const originalValue = this.value;

            if (name === 'cedula' || name === 'telefono') {

                this.value = this.value.replace(/[^\d]/g, '');

                if (
                    name === 'cedula' &&
                    this.value.length > 10
                ) {
                    this.value = this.value.slice(0, 10);
                }

            } else if (
                name === 'nombre_usuario' ||
                name === 'apellido_usuario'
            ) {

                this.value = this.value.replace(
                    regexNoPermitidosLetras,
                    ''
                );

            } else if (name === 'direccion') {

                this.value = this.value.replace(
                    regexNoPermitidosDireccion,
                    ''
                );

            } else if (
                name === 'password' ||
                name === 'password_edit'
            ) {

                this.value = this.value.replace(
                    regexNoPermitidosPassword,
                    ''
                );
            }

            if (this.value !== originalValue) {

                $(this)
                    .addClass('is-invalid')
                    .removeClass('is-valid');

                if (
                    $(this).next('.invalid-feedback').length === 0
                ) {

                    $(this).after(
                        '<div class="invalid-feedback"></div>'
                    );
                }

                let mensaje = 'Caracter no permitido.';

                if (
                    name === 'cedula' ||
                    name === 'telefono'
                ) {

                    mensaje = 'Solo se permiten números.';

                } else if (
                    name === 'nombre_usuario' ||
                    name === 'apellido_usuario'
                ) {

                    mensaje = 'Solo se permiten letras.';

                } else if (name === 'direccion') {

                    mensaje =
                        'Solo se permiten letras, números y signos básicos.';

                } else if (
                    name === 'password' ||
                    name === 'password_edit'
                ) {

                    mensaje =
                        'Caracter no permitido en la contraseña.';
                }

                $(this)
                    .next('.invalid-feedback')
                    .text(mensaje)
                    .show();

            } else {

                $(this)
                    .removeClass('is-invalid')
                    .addClass('is-valid');

                $(this)
                    .next('.invalid-feedback')
                    .hide();
            }

            $(this).parsley().validate();
        }
    );

    $(document).on(
        'input',
        '#fromUsuarios input[maxlength], #formEditarusuario input[maxlength]',
        function () {

            if (
                this.name === 'correo' ||
                this.name === 'correo_reg' ||
                this.name === 'correo_edit'
            ) {
                return;
            }

            const max = parseInt(
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

            } else {

                feedback.hide();

                $(this).removeClass('is-invalid');
            }
        }
    );

    $('#correo_reg, #correo_edit').on(
        'input',
        function () {

            const correo = this.value.trim();

            let feedback =
                $(this).next('.invalid-feedback');

            if (!feedback.length) {

                feedback =
                    $('<div class="invalid-feedback"></div>');

                $(this).after(feedback);
            }

            if (correo === '') {

                $(this)
                    .removeClass('is-invalid is-valid');

                feedback.hide();

                return;
            }

            const regexCorreo =
                /^[a-zA-Z0-9._%+-]+@(gmail|outlook|hotmail|yahoo)\.com$/i;

            if (!regexCorreo.test(correo)) {

                $(this)
                    .removeClass('is-valid')
                    .addClass('is-invalid');

                feedback
                    .text(
                        'Ingrese un correo válido como gmail.com, outlook.com, hotmail.com o yahoo.com'
                    )
                    .show();

            } else {

                $(this)
                    .removeClass('is-invalid')
                    .addClass('is-valid');

                feedback.hide();
            }
        }
    );

    window.Parsley.on(
        'field:error',
        function () {

            const name =
                this.$element.attr('name');

            if (
                name === 'correo' ||
                name === 'correo_reg' ||
                name === 'correo_edit'
            ) {
                return;
            }

            this.$element
                .addClass('is-invalid')
                .removeClass('is-valid');

            if (
                this.$element
                    .next('.invalid-feedback')
                    .length === 0
            ) {

                this.$element.after(
                    '<div class="invalid-feedback">' +
                    this.getErrorsMessages()[0] +
                    '</div>'
                );

            } else {

                this.$element
                    .next('.invalid-feedback')
                    .text(
                        this.getErrorsMessages()[0]
                    )
                    .show();
            }
        }
    );

    window.Parsley.on(
        'field:success',
        function () {

            const name =
                this.$element.attr('name');

            if (
                name === 'correo' ||
                name === 'correo_reg' ||
                name === 'correo_edit'
            ) {
                return;
            }

            this.$element
                .removeClass('is-invalid')
                .addClass('is-valid');

            this.$element
                .next('.invalid-feedback')
                .hide();
        }
    );

    $('#togglePassword').on(
        'click',
        function () {

            const password = $('#password');
            const eyeIcon = $('#eyeIcon');

            if (
                password.attr('type') === 'password'
            ) {

                password.attr('type', 'text');

                eyeIcon
                    .removeClass('bi-eye')
                    .addClass('bi-eye-slash');

            } else {

                password.attr('type', 'password');

                eyeIcon
                    .removeClass('bi-eye-slash')
                    .addClass('bi-eye');
            }
        }
    );

    $('#cedula').blur(function () {

        const buscar = $(this).val().trim();

        if (buscar === '') {
            return;
        }

        $.post(
            '/admin?ruta=usuarios',
            { buscar: buscar },
            function (response) {

                if (response.existe === true) {

                    Swal.fire({
                        title: 'Advertencia',
                        text: 'El Usuario ya se encuentra registrado',
                        icon: 'warning'
                    });

                    $('#cedula')
                        .val('')
                        .focus();
                }
            },
            'json'
        );
    });

});