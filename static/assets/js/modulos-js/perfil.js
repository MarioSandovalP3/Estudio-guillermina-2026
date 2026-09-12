console.log("Perfil cargado ");

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('formPerfil');
    const inputs = form.querySelectorAll('input:not([readonly])');

    // Reglas de validación
    const regex = {
        nombre_usuario: /^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]{0,50}$/, // solo letras y espacios
        apellido_usuario: /^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]{0,50}$/,
        telefono: /^[0-9]{0,15}$/, // solo números
        direccion: /^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9\s#.,-]{0,100}$/,

    };

    const mensajes = {
        nombre_usuario: 'Solo se permiten letras .',
        apellido_usuario: 'Solo se permiten letras .',
        telefono: 'Solo se permiten números .',
        direccion: 'Solo letras, números y signos .',

    };

    // 🔹 Validación y bloqueo en tiempo real
    inputs.forEach(input => {
        input.addEventListener('input', function (e) {
            const name = this.name;
            const valor = this.value;
            const feedback = this.nextElementSibling;
            const reg = regex[name];

            if (!reg) return;

            if (!reg.test(valor)) {
                // bloquear  incorrecto
                this.value = valor.slice(0, -1);
                this.classList.add('is-invalid');
                feedback.textContent = mensajes[name];
                feedback.style.display = 'block';
            } else {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
                feedback.textContent = '';
                feedback.style.display = 'none';
            }
        });
    });

    // ✅ Envío por AJAX
    $('#formPerfil').on('submit', function (e) {
        e.preventDefault();

        var $modal = $('#primaryheder');

        $.ajax({
            type: 'POST',
            url: '/admin?ruta=perfil',
            data: $(this).serialize() + '&editar=1',
            dataType: 'json',
            success: function (response) {

                if (response.status === 'success') {

                    Swal.fire({
                        icon: 'success',
                        title: 'Éxito',
                        text: response.mensaje,
                        timer: 1500,
                        showConfirmButton: false
                    });

                    // 🔥 ACTUALIZAR UI SIN RECARGAR
                    $('input[name="nombre_usuario"]').val(response.datos.nombre_usuario);
                    $('input[name="apellido_usuario"]').val(response.datos.apellido_usuario);
                    $('input[name="telefono"]').val(response.datos.telefono);
                    $('input[name="direccion"]').val(response.datos.direccion);
                    $('input[name="correo"]').val(response.datos.correo);

                    $modal.modal('hide');
                }
                else {
                    Swal.fire('Error', response.mensaje, 'error');
                }
            }
        });
    });




    $("#formPerfil input[name='correo']").on("input", function () {
        const correo = this.value.trim();
        const regexCorreo = /^[a-zA-Z0-9._%+-]+@(gmail|outlook|hotmail|yahoo)\.com$/;

        if (correo === "") {
            $(this).removeClass("is-invalid is-valid");
            $(this).next(".invalid-feedback").hide();
            return;
        }

        if (!regexCorreo.test(correo)) {
            let feedback = $(this).next(".invalid-feedback");

            if (!feedback.length) {
                feedback = $('<div class="invalid-feedback"></div>');
                $(this).after(feedback);
            }

            $(this).addClass("is-invalid").removeClass("is-valid");
            feedback.text("Ingrese un correo válido terminado en .com").show();
        } else {
            $(this).removeClass("is-invalid").addClass("is-valid");
            $(this).next(".invalid-feedback").hide();
        }
    });



});