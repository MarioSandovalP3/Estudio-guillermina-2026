console.log('Abrio empresasss');

$(document).ready(function () {
    const regexTexto = /^[a-zA-ZÁÉÍÓÚáéíóúñÑ\s.,;¿?()]+$/;
    const regexDireccion = /^[a-zA-Z0-9ÁÉÍÓÚáéíóúÑñ\s.,#\/\-()]+$/;
    const regexTelefono = /^[0-9]+$/;
    const regexCorreo = /^[a-zA-Z0-9._%+-]+@(gmail|outlook|hotmail|yahoo)\.com$/i;
    const regexNoPermitidosTexto = /[^a-zA-ZÁÉÍÓÚáéíóúñÑ\s.,;¿?()]/g;
    const regexNoPermitidosDireccion = /[^a-zA-Z0-9ÁÉÍÓÚáéíóúÑñ\s.,#\/\-()]/g;
    const regexNoPermitidosTelefono = /[^0-9]/g;

    function alerta(res) {
        return Swal.fire({
            icon: res.icon,
            title: res.title,
            text: res.text,
            showConfirmButton: true,
            confirmButtonText: 'Aceptar',
            timer: 2000,
            timerProgressBar: true
        });
    }

    function cerrarModal(id) {
        $(id).modal('hide');
        $(id).one('hidden.bs.modal', function () {
            $('.modal-backdrop').remove();
            $('body').removeClass('modal-open');
        });
    }

    function showError($input, message) {
        let $feedback = $input.next('.invalid-feedback');
        if (!$feedback.length) {
            $feedback = $('<div class="invalid-feedback"></div>');
            $input.after($feedback);
        }
        $input.addClass('is-invalid').removeClass('is-valid');
        $feedback.text(message).show();
    }

    function validateInput(input) {
        const $input = $(input);
        const name = input.name;
        let message = '';

        if (name === 'nombre' || name === 'descripcion_empresa') {
            input.value = input.value.replace(regexNoPermitidosTexto, '');
            if (!regexTexto.test(input.value) && input.value !== '') {
                message = 'Solo se permiten letras y signos básicos.';
            }
        } else if (name === 'direccion') {
            input.value = input.value.replace(regexNoPermitidosDireccion, '');
            if (!regexDireccion.test(input.value) && input.value !== '') {
                message = 'Solo se permiten letras, números y signos básicos.';
            }
        } else if (name === 'telefono') {
            input.value = input.value.replace(regexNoPermitidosTelefono, '');
            if (!regexTelefono.test(input.value) && input.value !== '') {
                message = 'Solo se permiten números.';
            }
        } else if (name === 'logo') {
            const file = input.files[0];
            if (file) {
                const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml'];
                const maxSize = 5 * 1024 * 1024;
                const forbiddenExtensions = /\.(mp3|mp4|avi|mkv|pdf|doc|docx|xls|xlsx|ppt|pptx|zip|rar|txt|csv)$/i;

                if (forbiddenExtensions.test(file.name)) {
                    message = 'Formato no permitido. Solo imágenes.';
                    input.value = '';
                } else if (!allowedTypes.includes(file.type)) {
                    message = 'Tipo de archivo no válido. Solo imágenes.';
                    input.value = '';
                } else if (file.size > maxSize) {
                    message = 'La imagen no debe superar los 5 MB.';
                    input.value = '';
                }
            } else {
                message = 'Debe seleccionar una imagen válida.';
            }
        }

        if (message) {
            showError($input, message);
        } else {
            $input.next('.invalid-feedback').hide();
            $input.removeClass('is-invalid').addClass('is-valid');
        }
    }

    document.getElementById('modalRegistrarEmpresa')?.addEventListener('shown.bs.modal', function () {
        const fecha = document.getElementById('fechaEmpresa');
        if (fecha) {
            fecha.value = new Date().toISOString().split('T')[0];
        }
    });

    $('#empresaForm').on('submit', function (e) {
        e.preventDefault();
        const form = $(this);

        if (!form.parsley().validate()) return;

        const nombre = $('#empresaForm #nombre').val().trim();
        const descripcion = $('#empresaForm #descripcion').val().trim();
        const direccion = $('#empresaForm #direccion').val().trim();
        const telefono = $('#empresaForm #telefono').val().trim();
        const correo = $('#empresaForm #email').val().trim();

        if (!regexTexto.test(nombre)) {
            return showError($('#empresaForm #nombre'), 'El nombre solo puede contener letras y signos básicos.');
        }

        if (!regexTexto.test(descripcion)) {
            return showError($('#empresaForm #descripcion'), 'La descripción solo puede contener letras y signos básicos.');
        }

        if (!regexDireccion.test(direccion)) {
            return showError($('#empresaForm #direccion'), 'La dirección solo puede contener letras, números y signos básicos.');
        }

        if (!regexTelefono.test(telefono)) {
            return showError($('#empresaForm #telefono'), 'El teléfono solo puede contener números.');
        }

        if (!regexCorreo.test(correo)) {
            return showError($('#empresaForm #email'), 'Ingrese un correo válido como gmail.com, outlook.com, hotmail.com o yahoo.com.');
        }

        $.ajax({
            url: '/admin?ruta=empresa',
            type: 'POST',
            data: new FormData(this),
            processData: false,
            contentType: false,
            dataType: 'json',
            success: function (res) {
                alerta(res).then(function () {
                    if (res.icon !== 'success') return;

                    $('#empresaForm')[0].reset();
                    $('#empresaForm').parsley().reset();
                    $('#empresaForm').find('.is-invalid, .is-valid').removeClass('is-invalid is-valid');
                    $('#empresaForm').find('.invalid-feedback').hide();

                    cerrarModal('#modalRegistrarEmpresa');

                    $('#contenedorEmpresas').load(location.href + ' #contenedorEmpresas>*');

                    if (res.data) {
                        if (res.data.nombre) {
                            $('#nombreEmpresaSidebar').text(res.data.nombre);
                            $('#footerEmpresa').text('Copyright © 2026 ' + res.data.nombre);
                        }

                        if (res.data.logo) {
                            $('#logoEmpresa').attr('src', res.data.logo).show();
                            $('#textoEmpresaSidebar').hide();
                        }
                    }
                    /* =========== ACTUALIZAR NOTIFICACIÓN Y SIDEBAR
                     ========================= */ consultarEmpresaNoRegistrada();
                });
            },

        });
    });



    $('#editar').on('submit', function (e) {
        e.preventDefault();
        const form = $(this);

        if (!form.parsley().validate()) return;

        const correo = $('#editar #email').val().trim();

        if (!regexCorreo.test(correo)) {
            return showError($('#editar #email'), 'Ingrese un correo válido como gmail.com, outlook.com, hotmail.com o yahoo.com.');
        }

        $.ajax({
            url: '/admin?ruta=empresa',
            type: 'POST',
            data: new FormData(this),
            processData: false,
            contentType: false,
            dataType: 'json',
            success: function (res) {
                alerta(res).then(function () {
                    if (res.icon !== 'success') return;

                    $('#editar')[0].reset();
                    $('#editar').parsley().reset();
                    $('#editar').find('.is-invalid, .is-valid').removeClass('is-invalid is-valid');
                    $('#editar').find('.invalid-feedback').hide();

                    cerrarModal('#exampleModal');

                    $('#contenedorEmpresas').load(location.href + ' #contenedorEmpresas>*');

                    if (res.data) {
                        if (res.data.logo) {
                            $('#logoEmpresa').attr('src', res.data.logo).show();
                        }

                        if (res.data.nombre) {
                            $('#nombreEmpresaSidebar').text(res.data.nombre);
                            $('#footerEmpresa').text('Copyright © 2026 ' + res.data.nombre);
                        }
                    }
                });
            },
            error: function () {
                alerta({
                    icon: 'error',
                    title: 'Error',
                    text: 'Ocurrió un error al actualizar la empresa.'
                });
            }
        });
    });

    $('#exampleModal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget);
        const modal = $(this);

        modal.find('#nombre').val(button.data('nombre'));
        modal.find('input[name="nombre_original"]').val(button.data('nombre'));
        modal.find('#direccion').val(button.data('direccion'));
        modal.find('#telefono').val(button.data('telefono'));
        modal.find('#email').val(button.data('email'));
        modal.find('#descripcion_empresa').val(button.data('descripcion_empresa'));

        const logo = button.data('logo');

        if (logo) {
            modal.find('#previewLogo').attr('src', logo).show();
        } else {
            modal.find('#previewLogo').hide();
        }

        modal.find('#logo').val('');
        modal.find('#email').removeClass('is-invalid is-valid');
        modal.find('#email').next('.invalid-feedback').hide();
    });

    $('#empresaForm, #editar').parsley();

    $('#empresaForm input, #empresaForm textarea, #empresaForm input[type="file"], #editar input, #editar textarea, #editar input[type="file"]').on('input change', function () {
        if (this.name === 'email') return;
        validateInput(this);
    });

    $('#empresaForm #email, #editar #email').on('input', function () {
        const correo = this.value.trim();
        let feedback = $(this).next('.invalid-feedback');

        if (!feedback.length) {
            feedback = $('<div class="invalid-feedback"></div>');
            $(this).after(feedback);
        }

        if (correo === '') {
            $(this).removeClass('is-invalid is-valid');
            feedback.hide();
            return;
        }

        if (!regexCorreo.test(correo)) {
            $(this).removeClass('is-valid').addClass('is-invalid');
            feedback.text('Ingrese un correo válido como gmail.com, outlook.com, hotmail.com o yahoo.com.').show();
        } else {
            $(this).removeClass('is-invalid').addClass('is-valid');
            feedback.hide();
        }
    });

    window.Parsley.on('field:error', function () {
        const name = this.$element.attr('name');
        const id = this.$element.attr('id');

        if (name === 'email' || id === 'email') return;

        this.$element.addClass('is-invalid').removeClass('is-valid');

        let feedback = this.$element.next('.invalid-feedback');

        if (!feedback.length) {
            feedback = $('<div class="invalid-feedback"></div>');
            this.$element.after(feedback);
        }

        feedback.text(this.getErrorsMessages()[0]).show();
    });

    window.Parsley.on('field:success', function () {
        const name = this.$element.attr('name');
        const id = this.$element.attr('id');

        if (name === 'email' || id === 'email') return;

        this.$element.removeClass('is-invalid').addClass('is-valid');
        this.$element.next('.invalid-feedback').hide();
    });

    $('#empresaForm, #editar').on('keydown', 'input', function (e) {
        const name = this.name;

        if (name === 'email') return;

        let regexPermitido = null;
        let mensaje = 'Caracter no permitido.';

        if (name === 'telefono') {
            regexPermitido = /^[0-9]$/;
            mensaje = 'Solo se permiten números.';
        } else if (name === 'nombre' || name === 'descripcion_empresa') {
            regexPermitido = /^[a-zA-ZÁÉÍÓÚáéíóúñÑ\s.,;¿?()]$/;
            mensaje = 'Solo se permiten letras y signos básicos.';
        } else if (name === 'direccion') {
            regexPermitido = /^[a-zA-Z0-9ÁÉÍÓÚáéíóúÑñ\s.,#\/\-()]$/;
            mensaje = 'Solo se permiten letras, números y signos básicos.';
        }

        if (regexPermitido && e.key.length === 1 && !regexPermitido.test(e.key)) {
            e.preventDefault();
            showError($(this), mensaje);
            return;
        }

        const max = parseInt(this.getAttribute('maxlength'));

        if (max && this.value.length >= max && e.key.length === 1 && !e.ctrlKey && !e.metaKey) {
            e.preventDefault();
            showError($(this), 'Límite de caracteres alcanzado.');
        }
    });

    $('#empresaForm, #editar').on('paste', 'input', function (e) {
        const name = this.name;

        if (name === 'email') return;

        let regexPermitido = null;
        let mensaje = 'Caracter no permitido.';

        if (name === 'telefono') {
            regexPermitido = /^[0-9]+$/;
            mensaje = 'Solo se permiten números.';
        } else if (name === 'nombre' || name === 'descripcion_empresa') {
            regexPermitido = /^[a-zA-ZÁÉÍÓÚáéíóúñÑ\s.,;¿?()]+$/;
            mensaje = 'Solo se permiten letras y signos básicos.';
        } else if (name === 'direccion') {
            regexPermitido = /^[a-zA-Z0-9ÁÉÍÓÚáéíóúÑñ\s.,#\/\-()]+$/;
            mensaje = 'Solo se permiten letras, números y signos básicos.';
        }

        if (!regexPermitido) return;

        const texto = e.originalEvent.clipboardData.getData('text');

        if (!regexPermitido.test(texto)) {
            e.preventDefault();
            showError($(this), mensaje);
            return;
        }

        const max = parseInt(this.getAttribute('maxlength'));

        if (max) {
            const seleccion = this.selectionEnd - this.selectionStart;

            if (this.value.length - seleccion + texto.length > max) {
                e.preventDefault();
                showError($(this), 'Límite de ' + max + ' caracteres alcanzado.');
            }
        }
    });

    $('#empresaForm input, #editar input').on('input', function () {
        const name = this.name;

        if (name === 'email') return;

        const originalValue = this.value;

        if (name === 'telefono') {
            this.value = this.value.replace(regexNoPermitidosTelefono, '');
        } else if (name === 'nombre' || name === 'descripcion_empresa') {
            this.value = this.value.replace(regexNoPermitidosTexto, '');
        } else if (name === 'direccion') {
            this.value = this.value.replace(regexNoPermitidosDireccion, '');
        }

        if (this.value !== originalValue) {
            let mensaje = 'Caracter no permitido.';

            if (name === 'telefono') {
                mensaje = 'Solo se permiten números.';
            } else if (name === 'nombre' || name === 'descripcion_empresa') {
                mensaje = 'Solo se permiten letras y signos básicos.';
            } else if (name === 'direccion') {
                mensaje = 'Solo se permiten letras, números y signos básicos.';
            }

            showError($(this), mensaje);
        } else {
            $(this).removeClass('is-invalid').addClass('is-valid');
            $(this).next('.invalid-feedback').hide();
        }

        $(this).parsley().validate();
    });

    $(document).on('input', '#empresaForm input[maxlength], #editar input[maxlength]', function () {
        if (this.name === 'email') return;

        const max = parseInt(this.getAttribute('maxlength'));

        if (!max) return;

        let feedback = $(this).next('.invalid-feedback');

        if (!feedback.length) {
            feedback = $('<div class="invalid-feedback"></div>');
            $(this).after(feedback);
        }

        if (this.value.length >= max) {
            feedback.text('Límite de caracteres alcanzado').css({
                display: 'block',
                width: '100%'
            });

            $(this).addClass('is-invalid').removeClass('is-valid');
        } else {
            feedback.hide();
            $(this).removeClass('is-invalid');
        }
    });

    $('#empresaForm, #editar').on('change', 'input[type="file"]', function () {
        validateInput(this);
    });

    $('#exampleModalScrollable, #exampleModal').on('hidden.bs.modal', function () {
        const $modal = $(this);
        const form = $modal.find('form')[0];

        if (form) form.reset();

        $modal.find('form').parsley().reset();
        $modal.find('.is-invalid, .is-valid').removeClass('is-invalid is-valid');
        $modal.find('.invalid-feedback').hide();
        $modal.find('#previewLogo').hide();
    });

    $('#btnCerrarModal').on('click', function () {
        const $modal = $('#modalRegistrarEmpresa');
        const form = $modal.find('form')[0];

        if (form) form.reset();

        $modal.find('.is-invalid, .is-valid').removeClass('is-invalid is-valid');
        $modal.find('.invalid-feedback').hide();
        $modal.find('form').parsley().reset();
    });

    $('#btnCerrar, #btnClose').on('click', function () {
        const $modal = $('#exampleModal');

        $modal.find('.is-invalid, .is-valid').removeClass('is-invalid is-valid');
        $modal.find('.invalid-feedback').hide();
        $modal.find('form').parsley().reset();
    });
});