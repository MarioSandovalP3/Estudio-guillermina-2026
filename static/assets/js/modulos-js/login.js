console.log("abrio loginnn");

document.addEventListener('DOMContentLoaded', function () {
    $('#loginForm').on('submit', function (e) {
        e.preventDefault();
        if (!$(this).parsley().validate()) return;
        $.post('/admin?ruta=login', $(this).serialize(), function (res) {
            Swal.fire({
                icon: res.icon,
                title: res.title,
                text: res.text
            }).then(() => {
                if (res.icon === "success") {
                    window.location.href = res.redirect;
                }
            });
        }, 'json');
    });

    $('#formRegistrarCliente').on('submit', function (e) {
        e.preventDefault();
        if (!$('#formRegistrarCliente').parsley().validate()) return;
        $.ajax({
            url: '/admin?ruta=cliente',
            type: 'POST',
            data: $(this).serialize(),
            dataType: 'json',
            success: function (res) {
                Swal.fire({
                    icon: res.icon,
                    title: res.title,
                    text: res.text,
                    showConfirmButton: true,
                    confirmButtonText: 'Aceptar',
                    timer: 2000,
                    timerProgressBar: true
                }).then(() => {
                    if (res.icon === 'success') {
                        $('#formRegistrarCliente')[0].reset();
                        $('#formRegistrarCliente').parsley().reset();
                        document.getElementById('back-to-login-register').click();
                    }
                });
            },
            error: function (xhr, status, error) {
                console.log("========== ERROR AJAX ==========");
                console.log("HTTP:", xhr.status);
                console.log("Status:", status);
                console.log("Error:", error);
                console.log("Respuesta:", xhr.responseText);
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Error.'
                });
            }
        });
    });

    $('#resetPasswordForm').on('submit', function (e) {
        e.preventDefault();
        const pass = $('#newPassword').val();
        const confirm = $('#confirmPassword').val();

        if (pass !== confirm) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Las contraseñas no coinciden'
            });
            return;
        }

        $.ajax({
            url: '/admin?ruta=login',
            type: 'POST',
            data: $(this).serialize(),
            dataType: 'json',
            success: function (res) {
                Swal.fire({
                    icon: res.icon,
                    title: res.title,
                    text: res.text
                });

                if (res.icon === 'success') {
                    $('#resetPasswordForm')[0].reset();
                    $('#back-to-login-reset').click();
                }
            },
            error: function () {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Error en el servidor'
                });
            }
        });
    });

    const registrarceLink = document.getElementById('registrarce-link');
    const backToLoginResetButton = document.getElementById('back-to-login-reset');
    const backToLoginRegisterButton = document.getElementById('back-to-login-register');
    const forgotPasswordLink = document.getElementById('forgot-password-link');

    if (registrarceLink) {
        registrarceLink.addEventListener('click', function (e) {
            e.preventDefault();
            document.getElementById('loginForm').style.display = 'none';
            document.getElementById('resetPasswordContainer').style.display = 'none';
            document.getElementById('registerContainer').style.display = 'block';
        });
    }

    if (backToLoginResetButton) {
        backToLoginResetButton.addEventListener('click', function () {
            document.getElementById('resetPasswordContainer').style.display = 'none';
            document.getElementById('registerContainer').style.display = 'none';
            document.getElementById('loginForm').style.display = 'block';
        });
    }

    if (backToLoginRegisterButton) {
        backToLoginRegisterButton.addEventListener('click', function () {
            document.getElementById('resetPasswordContainer').style.display = 'none';
            document.getElementById('registerContainer').style.display = 'none';
            document.getElementById('loginForm').style.display = 'block';
        });
    }

    if (forgotPasswordLink) {
        forgotPasswordLink.addEventListener('click', function (e) {
            e.preventDefault();
            document.getElementById('loginForm').style.display = 'none';
            document.getElementById('registerContainer').style.display = 'none';
            document.getElementById('resetPasswordContainer').style.display = 'block';
        });
    }

    function limpiarResetPassword() {
        const form = $('#resetPasswordForm');
        form[0].reset();
        form.parsley().reset();
        $('#resetPasswordForm').find('.is-invalid, .is-valid').removeClass('is-invalid is-valid');
        $('#resetPasswordForm .parsley-errors-list').remove();
    }

    function togglePasswordVisibility(toggleId, inputId, iconId) {
        const toggle = document.getElementById(toggleId);

        if (toggle) {
            toggle.addEventListener('click', function () {
                const input = document.getElementById(inputId);
                const icon = document.getElementById(iconId);

                if (input.type === 'password') {
                    input.type = 'text';
                    icon.classList.remove('fa-eye');
                    icon.classList.add('fa-eye-slash');
                } else {
                    input.type = 'password';
                    icon.classList.remove('fa-eye-slash');
                    icon.classList.add('fa-eye');
                }
            });
        }
    }

    togglePasswordVisibility('toggle-login-password', 'login-password', 'eye-icon-login');
    togglePasswordVisibility('toggle-new-password', 'newPassword', 'eye-icon-new');
    togglePasswordVisibility('toggle-confirm-password', 'confirmPassword', 'eye-icon-confirm');
    togglePasswordVisibility('toggle-register-password', 'register-password', 'eye-icon-register');

    const form = document.getElementById('formRegistrarCliente');

    function mostrarError(input, mensaje) {
        ocultarError(input);

        const error = document.createElement('div');
        error.className = 'error-message';
        error.style.color = 'red';
        error.innerText = mensaje;

        input.parentNode.insertBefore(error, input.nextSibling);
        input.classList.remove('is-valid');
        input.classList.add('is-invalid');
    }

    function ocultarError(input) {
        const error = input.parentNode.querySelector('.error-message');

        if (error) {
            error.remove();
        }

        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
    }

    function validarLetras(event) {
        const input = event.target;
        const valorOriginal = input.value;
        const valor = valorOriginal.replace(/[^a-zA-ZñÑáéíóúÁÉÍÓÚ]/g, '');

        input.value = valor;

        if (valorOriginal !== valor) {
            mostrarError(input, 'Solo se permiten letras.');
        } else if (valor === '') {
            mostrarError(input, 'Solo se permiten letras.');
        } else {
            ocultarError(input);
        }
    }

    function validarNumeros(event) {
        const input = event.target;
        const valorOriginal = input.value;
        const valor = valorOriginal.replace(/[^0-9]/g, '');

        input.value = valor;

        if (valorOriginal !== valor) {
            mostrarError(input, 'Solo se permiten números.');
        } else if (valor === '') {
            mostrarError(input, 'Solo se permiten números.');
        } else {
            ocultarError(input);
        }
    }

    function validarCorreo(event) {
        const input = event.target;
        const valorOriginal = input.value;
        const valor = valorOriginal.replace(/[^a-zA-Z0-9ñÑ._%+\-@]/g, '');

        input.value = valor;

        const regexCorreo = /^[a-zA-Z0-9ñÑ._%+\-]+@[a-zA-Z0-9ñÑ.-]+\.[a-zA-Z]{2,}$/;

        if (valorOriginal !== valor) {
            mostrarError(input, 'Caracter no permitido en el correo.');
        } else if (valor === '') {
            mostrarError(input, 'El correo es obligatorio.');
        } else if (!regexCorreo.test(valor)) {
            mostrarError(input, 'Formato de correo no válido.');
        } else {
            ocultarError(input);
        }
    }

    function validarContraseña(event) {
        const input = event.target;

        if (input.value.length < 6) {
            mostrarError(input, 'La contraseña debe tener al menos 6 caracteres.');
        } else {
            ocultarError(input);
        }
    }

    if (form) {
        const cedulaReg = document.getElementById('cedula_reg');
        const correoReg = document.getElementById('correo_reg');
        const telefonoReg = document.getElementById('telefono_reg');
        const nombreUsuarioReg = document.getElementById('nombre_usuario_reg');
        const apellidoUsuarioReg = document.getElementById('apellido_usuario_reg');
        const registerPassword = document.getElementById('register-password');

        if (cedulaReg) {
            cedulaReg.addEventListener('input', validarNumeros);
        }

        if (correoReg) {
            correoReg.addEventListener('input', validarCorreo);
        }

        if (telefonoReg) {
            telefonoReg.addEventListener('input', validarNumeros);
        }

        if (nombreUsuarioReg) {
            nombreUsuarioReg.addEventListener('input', validarLetras);
        }

        if (apellidoUsuarioReg) {
            apellidoUsuarioReg.addEventListener('input', validarLetras);
        }

        if (registerPassword) {
            registerPassword.addEventListener('input', validarContraseña);
        }
    }

    const cedulaInput = document.getElementById('reset-cedula');

    if (cedulaInput) {
        const errorContainer = document.createElement('div');
        errorContainer.style.color = 'red';
        errorContainer.style.marginTop = '5px';
        errorContainer.style.fontSize = '0.9rem';
        errorContainer.style.display = 'none';

        cedulaInput.parentNode.appendChild(errorContainer);

        cedulaInput.addEventListener('input', function (event) {
            const input = event.target;
            const valorOriginal = input.value;
            const valorFiltrado = valorOriginal.replace(/[^0-9]/g, '');

            if (valorOriginal !== valorFiltrado) {
                input.value = valorFiltrado;
                errorContainer.innerText = 'Solo se permiten números';
                errorContainer.style.display = 'block';
            } else {
                errorContainer.innerText = '';
                errorContainer.style.display = 'none';
            }
        });
    }

    const regexRol = /^[a-zA-ZÁÉÍÓÚáéíóúñÑ\s]+$/;
    const regexNoPermitidosRol = /[^a-zA-ZÁÉÍÓÚáéíóúñÑ\s]/g;

    $('#formRol input, #formEditRol input').on('input', function () {
        const originalValue = this.value;
        this.value = this.value.replace(regexNoPermitidosRol, '');

        if (this.value !== originalValue) {
            $(this).addClass('is-invalid').removeClass('is-valid');

            if ($(this).next('.invalid-feedback').length === 0) {
                $(this).after('<div class="invalid-feedback">En este campo solo se permiten letras.</div>');
            } else {
                $(this).next('.invalid-feedback').text('En este campo solo se permiten letras.').show();
            }
        } else {
            $(this).removeClass('is-invalid').addClass('is-valid');
            $(this).next('.invalid-feedback').hide();
        }
    });

    if (window.Parsley) {
        window.Parsley.on('field:error', function () {
            this.$element.addClass('is-invalid').removeClass('is-valid');

            if (this.$element.next('.invalid-feedback').length === 0) {
                this.$element.after('<div class="invalid-feedback">' + this.getErrorsMessages()[0] + '</div>');
            } else {
                this.$element.next('.invalid-feedback').text(this.getErrorsMessages()[0]).show();
            }
        });

        window.Parsley.on('field:success', function () {
            this.$element.removeClass('is-invalid').addClass('is-valid');
            this.$element.next('.invalid-feedback').hide();
        });
    }

    $('#back-to-login-register').on('click', function () {
        const form = $('#formRegistrarCliente');

        form.find('.is-invalid, .is-valid').removeClass('is-invalid is-valid');
        form.find('.invalid-feedback').remove();

        form.find('input, textarea, select').each(function () {
            const type = $(this).attr('type');

            if (type === 'checkbox' || type === 'radio') {
                $(this).prop('checked', false);
            } else {
                $(this).val('');
            }
        });
    });
    // ================== captcha ==================
    let captchaValor = "";

    function generarCaptcha() {
        const chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
        let texto = "";

        for (let i = 0; i < 5; i++) {
            texto += chars.charAt(Math.floor(Math.random() * chars.length));
        }

        captchaValor = texto;

        let html = "";

        for (let i = 0; i < texto.length; i++) {
            const colores = ["#0d6efd", "#198754", "#dc3545", "#fd7e14", "#6f42c1"];
            const color = colores[Math.floor(Math.random() * colores.length)];

            html += `<span style="color:${color}; font-size:32px; letter-spacing:4px;">${texto[i]}</span>`;
        }

        $("#captchaTexto").html(html);
        $("#captchaRespuesta").val("");
        $("#captchaMensaje").html("");
        $("#captchaEstado").html("");
    }

    $(document).on("click", "#registrarce-link", function (e) {
        e.preventDefault();
        generarCaptcha();
        $("#modalCaptchaSimple").modal("show");
    });

    $(document).on("click", "#nuevoCaptchaSimple", function () {
        generarCaptcha();
        $("#captchaRespuesta").focus();
    });

    $(document).on("input", "#captchaRespuesta", function () {
        let valor = $(this).val().toUpperCase();
        valor = valor.replace(/[^A-Z2-9]/g, '');
        $(this).val(valor);
    });

    $(document).on("click", "#verificarCaptchaSimple", function () {
        const respuesta = $("#captchaRespuesta").val().trim().toUpperCase();

        if (respuesta === "") {
            $("#captchaEstado").html(`
            <div class="alert alert-danger py-2 mb-0">
                Debes ingresar el código
            </div>
        `);
            $("#captchaRespuesta").focus();
            return;
        }

        if (respuesta === captchaValor) {
            $("#captchaEstado").html(`
            <div class="alert alert-success py-2 mb-0">
                ✔ Verificación exitosa
            </div>
        `);

            setTimeout(() => {
                $("#modalCaptchaSimple").modal("hide");
                $("#captchaEstado").html("");
                $("#loginForm").hide();
                $("#registerContainer").show();
            }, 900);
        } else {
            $("#captchaEstado").html(`
            <div class="alert alert-danger py-2 mb-0">
                ✖ Código incorrecto
            </div>
        `);

            $("#captchaRespuesta").val("").focus();
        }
    });


    $('#cedula_reg').on('blur', function () {
        const buscar = $(this).val().trim();

        if (buscar === '') {
            console.log('Campo vacío');
            return;
        }

        $.ajax({
            url: '/admin?ruta=cliente',
            type: 'POST',
            data: {
                buscar: buscar
            },
            dataType: 'json',
            success: function (response) {
                if (response.existe === true) {
                    Swal.fire({
                        title: 'Advertencia',
                        text: 'La cédula ya se encuentra registrada.',
                        icon: 'warning'
                    }).then(function () {
                        $('#cedula_reg').val('').focus();
                    });
                }
            }
        });
    });


    $(document).ready(function () {

        let captchaVerificado = false;

        $("#pow-checkbox").on("change", function () {

            if (!this.checked) {

                captchaVerificado = false;

                $("#pow-operation").hide();
                $("#pow-answer").val("");
                $("#pow-message").hide();

                $("#pow-status")
                    .text("Pendiente")
                    .css({
                        "color": "#6c757d",
                        "font-weight": "normal"
                    });

                return;
            }

            $("#pow-status")
                .text("Generando...")
                .css("color", "#6c757d");

            $.post("/admin?ruta=login", {
                generar_captcha: 1
            }, function (respuesta) {

                console.log("CAPTCHA:", respuesta);

                if (respuesta.status) {

                    $("#pow-question").text(
                        respuesta.numero1 + " + " + respuesta.numero2 + " = ?"
                    );

                    $("#pow-operation").slideDown(200);

                    $("#pow-status")
                        .text("Resuelve la operación")
                        .css("color", "#6c757d");

                    $("#pow-answer")
                        .val("")
                        .focus();

                    captchaVerificado = false;

                } else {

                    $("#pow-status")
                        .text("Error")
                        .css("color", "#dc3545");

                }

            }, "json").fail(function (xhr) {

                console.log("ERROR CAPTCHA:", xhr.responseText);

                $("#pow-status")
                    .text("Error")
                    .css("color", "#dc3545");

            });

        });

        $("#pow-answer").on("input", function () {

            this.value = this.value.replace(/[^0-9]/g, "");

            let respuesta = $(this).val();

            captchaVerificado = false;

            $("#pow-message").hide();

            if (respuesta === "") {

                $("#pow-status")
                    .text("Pendiente")
                    .css("color", "#6c757d");

                return;
            }

            if (respuesta.length >= 1) {

                $.post("/admin?ruta=login", {
                    verificar_captcha: 1,
                    respuesta: respuesta
                }, function (resultado) {

                    console.log("VERIFICACIÓN:", resultado);

                    if (resultado.verificado) {

                        captchaVerificado = true;

                        $("#pow-status")
                            .html("✓ Verificado")
                            .css({
                                "color": "#198754",
                                "font-weight": "bold"
                            });

                        $("#pow-message")
                            .html('<span style="color:#198754;">✓ CAPTCHA correcto</span>')
                            .fadeIn(150);

                        setTimeout(function () {

                            $("#pow-captcha").fadeOut(400);

                        }, 800);

                    } else {

                        captchaVerificado = false;

                        $("#pow-status")
                            .text("Incorrecto")
                            .css("color", "#dc3545");

                        $("#pow-message")
                            .html('<span style="color:#dc3545;">✗ Respuesta incorrecta</span>')
                            .fadeIn(150);

                    }

                }, "json").fail(function (xhr) {

                    console.log("ERROR VERIFICACIÓN:", xhr.responseText);

                    captchaVerificado = false;

                });

            }

        });

        $("#loginButton").on("click", function (e) {

            e.preventDefault();
            e.stopPropagation();

            if (!captchaVerificado) {

                $("#pow-message")
                    .html('<span style="color:#dc3545;">⚠ Verifica el CAPTCHA primero</span>')
                    .stop(true, true)
                    .fadeIn(200);

                $("#pow-status")
                    .text("Verifica el CAPTCHA")
                    .css({
                        "color": "#dc3545",
                        "font-weight": "bold"
                    });

                return false;
            }

            if (!$("#loginForm").parsley().isValid()) {

                return false;
            }

            $.post("/admin?ruta=login", $("#loginForm").serialize(), function (respuesta) {

                console.log("LOGIN:", respuesta);

                if (respuesta.redirect) {

                    Swal.fire({
                        icon: respuesta.icon,
                        title: respuesta.title,
                        text: respuesta.text,
                        timer: 1500,
                        showConfirmButton: false
                    }).then(function () {

                        window.location.href = respuesta.redirect;

                    });

                } else {

                    Swal.fire({
                        icon: respuesta.icon,
                        title: respuesta.title,
                        text: respuesta.text
                    });

                }

            }, "json").fail(function (xhr) {

                console.log("ERROR LOGIN:", xhr.responseText);

                Swal.fire({
                    icon: "error",
                    title: "Error",
                    text: "No se pudo procesar el inicio de sesión."
                });

            });

            return false;

        });

    });







});