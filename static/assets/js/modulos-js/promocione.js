console.log('Abrio .js');
$(document).ready(function () {
    // Inicializar Parsley en el formulario de registro
    $('#RegistrarPromocion').parsley();
    $('#RegistrarPromocion input, #RegistrarPromocion textarea').on('input', function () {
        validateInput(this);
    });

    // Inicializar Parsley en el formulario de edición
    $('#EditarPromocion').parsley();
    $('#EditarPromocion input, #EditarPromocion textarea').on('input', function () {
        validateInput(this);
    });

    function validateInput(input) {
        const originalValue = input.value;
        let regex;

        if (input.name === 'nombre_promo' || input.name === 'descripcion_promo') {
            // Permitr letras, números y caracteres
            regex = /^[a-zA-ZÁÉÍÓÚáéíóúñÑ0-9\s@*+#$%&,./\\():;¡!]+$/;
            input.value = input.value.replace(/[^a-zA-ZÁÉÍÓÚáéíóúñÑ0-9\s@*+#$%&,./\\():;¡!]/g, '');
        } else if (input.name === 'descuento') {
            regex = /^[0-9]*$/;
            input.value = input.value.replace(/[^0-9]/g, '');
        }
        // No se aplica validación a los campos de fecha y archivo
        if (input.name !== 'inicio_promo' && input.name !== 'fin_promo' && input.name !== 'imagen_promo') {
            if (input.value !== originalValue) {
                $(input).next('.invalid-feedback').text('En este campo solo se permiten letras, números y caracteres especiales permitidos.').show();
                $(input).addClass('is-invalid').removeClass('is-valid');
            } else {
                $(input).parsley().validate();
            }
        }
    }

    // Validación de fechas
    function validarFechas(inicio, fin) {
        const fechaInicio = new Date(inicio);
        const fechaFin = new Date(fin);
        return fechaInicio < fechaFin;
    }

    // Validación de imagen
    function validarImagen(imagen) {
        const tipoImagen = imagen.type;
        const tamanoImagen = imagen.size;
        const tiposPermitidos = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
        const tamanoMaximo = 1024 * 1024 * 5;

        if (!tiposPermitidos.includes(tipoImagen)) {
            return { valido: false, mensaje: "El tipo de imagen no es permitido." };
        }
        if (tamanoImagen > tamanoMaximo) {
            return { valido: false, mensaje: "El tamaño de la imagen es demasiado grande." };
        }
        return { valido: true };
    }

    $('#RegistrarPromocion').on('submit', function (e) {
        e.preventDefault();
        
        const inicio = $('#inicio_promo').val();
        const fin = $('#fin_promo').val();
        const imagen = $('#imagen_promo')[0].files[0];

        if (!validarFechas(inicio, fin)) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'La fecha de inicio debe ser anterior a la fecha de fin.'
            });
            return;
        }

        if (imagen) {
            const validacionImagen = validarImagen(imagen);
            if (!validacionImagen.valido) {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: validacionImagen.mensaje
                });
                return;
            }
        }
        this.submit();
    });

    $('#EditarPromocion').on('submit', function (e) {
        e.preventDefault();
        
        const inicio = $('#inicio_promo_edit').val();
        const fin = $('#fin_promo_edit').val();
        const imagen = $('#imagen_promo_edit')[0].files[0];

        if (!validarFechas(inicio, fin)) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'La fecha de inicio debe ser anterior a la fecha de fin.'
            });
            return;
        }

        if (imagen) {
            const validacionImagen = validarImagen(imagen);
            if (!validacionImagen.valido) {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: validacionImagen.mensaje
                });
                return;
            }
        }
        this.submit();
    });

    // Mensaje de error personalizado debajo del input
    window.Parsley.on('field:error', function () {
        this.$element.addClass('is-invalid');
        this.$element.removeClass('is-valid');
        this.$element.next('.invalid-feedback').show();
    });

    window.Parsley.on('field:success', function () {
        this.$element.removeClass('is-invalid');
        this.$element.addClass('is-valid');
        this.$element.next('.invalid-feedback').hide();
    });

    // Inicializar tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl, {
            template: '<div class="tooltip" role="tooltip" style="background-color: white; color: black; border: 1px solid black;"><div class="tooltip-arrow"></div><div class="tooltip-inner"></div></div>'
        });
    });

    // Manejo de modales para editar, eliminar y ver promociones
    $('#modalEditarPromocion').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var cod_promo = button.data('cod_promo');
        var nombre_promo = button.data('nombre_promo');
        var descripcion_promo = button.data('descripcion_promo');
        var imagen_promo = button.data('imagen_promo');
        var descuento = button.data('descuento');
        var inicio_promo = button.data('inicio_promo');
        var fin_promo = button.data('fin_promo');
        var status = button.data('status');

        var modal = $(this);
        modal.find('input[name="cod_promo"]').val(cod_promo);
        modal.find('#nombre_promo_edit').val(nombre_promo);
        modal.find('#descripcion_promo_edit').val(descripcion_promo);
        modal.find('#descuento_edit').val(descuento);
        modal.find('#inicio_promo_edit').val(inicio_promo);
        modal.find('#fin_promo_edit').val(fin_promo);
        modal.find('#status_edit').val(status);
    });

    $('#modalVerPromocion').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var nombre = button.data('nombre');
        var descripcion = button.data('descripcion');
        var imagen = button.data('imagen');

        var modal = $(this);
        modal.find('#nombre_promocion').text(nombre);
        modal.find('#descripcion_promocion').text(descripcion);
        modal.find('#imagen_promocion').attr('src', imagen);
    });

    $('#modalEliminarPromocion').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var cod_promo = button.data('cod_promo');

        var modal = $(this);
        modal.find('#cod_promo_eliminar').val(cod_promo);
    });
});
