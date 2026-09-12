console.log("abrio");

const togglePassword = document.getElementById('toggle-password');
const passwordInput = document.getElementById('password');
const eyeIcon = document.getElementById('eye-icon');

togglePassword.addEventListener('click', function () {
    // Alternar el tipo de input entre 'password' y 'text'
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type);
    // Alternar el icono del ojo
    eyeIcon.classList.toggle('fa-eye-slash');
});

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('formRegistrarCliente');

    // Función para validar letras (sin espacios)
    function validarLetras(event) {
        const input = event.target;
        const valor = input.value;
        const regex = /^[a-zA-ZñÑáéíóúÁÉÍÓÚ]*$/; // Permitir solo letras sin espacios

        if (!regex.test(valor)) {
            input.value = valor.replace(/[^a-zA-ZñÑáéíóúÁÉÍÓÚ]/g, ''); // Eliminar caracteres no permitidos
            mostrarError(input, 'Solo se permiten letras .');
        } else {
            ocultarError(input);
        }
    }

    // Función para validar números
    function validarNumeros(event) {
        const input = event.target;
        const valor = input.value;
        const regex = /^[0-9]*$/; // Permitir solo dígitos

        if (!regex.test(valor)) {
            input.value = valor.replace(/[^0-9]/g, ''); // Eliminar caracteres no permitidos
            mostrarError(input, 'Solo se permiten números.');
        } else {
            ocultarError(input);
        }
    }

    // Función para validar el correo electrónico (permitir "ñ")
    function validarCorreo(event) {
        const input = event.target;
        const valor = input.value;
        const regex = /^[a-zA-ZñÑ0-9._%+-]+@[a-zA-ZñÑ0-9.-]+\.[a-zA-Z]{2,}$/; // Formato de correo que permite "ñ"

        if (!regex.test(valor) && valor !== '') {
            mostrarError(input, 'Formato de correo no válido.');
        } else {
            ocultarError(input);
        }
    }

    // Función para validar la contraseña
    function validarContraseña(event) {
        const input = event.target;
        const valor = input.value;

        if (valor.length < 6) {
            mostrarError(input, 'La contraseña debe tener al menos 6 caracteres.');
        } else {
            ocultarError(input);
        }
    }

    // Función para mostrar el mensaje de error
    function mostrarError(input, mensaje) {
        ocultarError(input); // Asegurarse de que no haya mensajes previos
        const error = document.createElement('div');
        error.className = 'error-message';
        error.style.color = 'red';
        error.innerText = mensaje;
        input.parentNode.insertBefore(error, input.nextSibling);
        input.classList.remove('is-valid');
        input.classList.add('is-invalid');
    }

    // Función para ocultar el mensaje de error
    function ocultarError(input) {
        const error = input.parentNode.querySelector('.error-message');
        if (error) {
            error.remove();
        }
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
    }

    // Función para validar campos obligatorios
    function validarObligatorios() {
        const inputs = form.querySelectorAll('input[required]');
        let esValido = true;

        inputs.forEach(input => {
            if (!input.value) {
                mostrarError(input, 'Este campo es obligatorio.');
                esValido = false;
            } else {
                ocultarError(input);
            }
        });

        return esValido;
    }

    // Agregar eventos a los campos
    document.getElementById('cedula_reg').addEventListener('input', validarNumeros);
    document.getElementById('correo_reg').addEventListener('input', validarCorreo);
    document.getElementById('telefono_reg').addEventListener('input', validarNumeros);
    document.getElementById('nombre_usuario_reg').addEventListener('input', validarLetras);
    document.getElementById('password').addEventListener('input', validarContraseña); // Validar contraseña

 
});