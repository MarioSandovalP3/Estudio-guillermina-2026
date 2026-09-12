console.log("Abrio cliente");

const reglas = {
    cedula: {
        regex: /[0-9]/,
        mensaje: "Solo se permiten números.",
        max: 10
    },
    telefono: {
        regex: /[0-9]/,
        mensaje: "Solo se permiten números.",
        max: 12
    },
    nombre_usuario: {
        regex: /[a-zA-ZÁÉÍÓÚáéíóúÑñ\s]/,
        mensaje: "Solo se permiten letras, espacios,.",
        max: 12
    },
    apellido_usuario: {
        regex: /[a-zA-ZÁÉÍÓÚáéíóúÑñ\s]/,
        mensaje: "Solo se permiten letras, espacios,.",
        max: 12
    },
    direccion: {
        regex: /[a-zA-Z0-9ÁÉÍÓÚáéíóúÑñ\s.,#\-\/()]/,
        mensaje: "Solo se permiten letras, números y signos básicos.",
        max: 40
    }
};

document.addEventListener("DOMContentLoaded", function () {

    function mostrarError(input, mensaje) {
        let feedback = $(input).next(".invalid-feedback");

        if (!feedback.length) {
            feedback = $('<div class="invalid-feedback"></div>');
            $(input).after(feedback);
        }

        $(input).addClass("is-invalid").removeClass("is-valid");
        feedback.text(mensaje).show();

        clearTimeout(input.errorTimer);
        input.errorTimer = setTimeout(function () {
            feedback.hide();
            $(input).removeClass("is-invalid");
        }, 1800);
    }

    $(document).on("keydown", "#formRegistrarCliente input, #formEditarCliente input", function (e) {
        const r = reglas[this.name];
        if (r && e.key.length === 1 && !r.regex.test(e.key)) {
            e.preventDefault();
            mostrarError(this, r.mensaje);
        }
    });

    $(document).on("paste", "#formRegistrarCliente input, #formEditarCliente input", function (e) {

        const regla = reglas[this.name];

        // El correo no se valida
        if (!regla) return;

        const texto = e.originalEvent.clipboardData.getData("text");

        if (![...texto].every(caracter => regla.regex.test(caracter))) {
            e.preventDefault();
            mostrarError(this, regla.mensaje);
            return;
        }

        const seleccion = this.selectionEnd - this.selectionStart;

        if (
            regla.max &&
            this.value.length - seleccion + texto.length > regla.max
        ) {
            e.preventDefault();
            mostrarError(this, "Límite de " + regla.max + " caracteres alcanzado.");
        }
    });

    $("#formRegistrarCliente, #formEditarCliente, #formPerfil").parsley();

    $("#formRegistrarCliente").on("submit", function (e) {
        e.preventDefault();

        if (!$(this).parsley().validate()) return;

        $.post("/admin?ruta=cliente", $(this).serialize(), function (res) {

            Swal.fire({
                icon: res.icon,
                title: res.title,
                text: res.text,
                confirmButtonText: "Aceptar",
                timer: 2000,
                timerProgressBar: true,
                backdrop: false
            }).then(function () {

                if (res.icon === "success") {
                    $("#formRegistrarCliente")[0].reset();
                    $("#formRegistrarCliente").parsley().reset();
                    $("#formRegistrarCliente").find(".is-invalid, .is-valid").removeClass("is-invalid is-valid");
                    $("#formRegistrarCliente").find(".invalid-feedback").hide();
                    $("#modalRegistrarCliente").modal("hide");
                    $("#table1").load(location.href + " #table1>*", "");
                }

            });

        }, "json");
    });

    $("#formEditarCliente").on("submit", function (e) {
        e.preventDefault();

        if (!$(this).parsley().validate()) return;

        $.post("/admin?ruta=cliente", $(this).serialize(), function (res) {

            Swal.fire({
                icon: res.icon,
                title: res.title,
                text: res.text,
                confirmButtonText: "Aceptar",
                timer: 2000,
                timerProgressBar: true,
                backdrop: false
            }).then(function () {

                if (res.icon === "success") {
                    $("#formEditarCliente")[0].reset();
                    $("#formEditarCliente").parsley().reset();
                    $("#formEditarCliente").find(".is-invalid, .is-valid").removeClass("is-invalid is-valid");
                    $("#formEditarCliente").find(".invalid-feedback").hide();
                    $("#modalEditar").modal("hide");
                    $("#table1").load(location.href + " #table1>*", "");
                }

            });

        }, "json");
    });

    $("#formEliminarCliente").on("submit", function (e) {
        e.preventDefault();

        $.post("/admin?ruta=cliente", $(this).serialize(), function (res) {

            Swal.fire({
                icon: res.icon,
                title: res.title,
                text: res.text,
                confirmButtonText: "Aceptar",
                timer: 2000,
                timerProgressBar: true,
                backdrop: false
            }).then(function () {

                if (res.icon === "success") {
                    $("#formEliminarCliente")[0].reset();
                    $("#modalEliminarCliente").modal("hide");
                    $("#table1").load(location.href + " #table1>*", "");
                }

            });

        }, "json");
    });

    $("#cedula_reg").on("blur", function () {

        const cedula = $(this).val().trim();

        if (!cedula) return;

        $.post(
            "/admin?ruta=cliente",
            { buscar: cedula },
            function (res) {

                if (res.existe === true) {

                    Swal.fire({
                        title: "Advertencia",
                        text: "El cliente ya se encuentra registrado",
                        icon: "warning",
                        confirmButtonText: "Aceptar"
                    });

                    $("#cedula_reg")
                        .val("")
                        .removeClass("is-valid is-invalid")
                        .focus();
                }

            },
            "json"
        );
    });

    const modalEditar = document.getElementById("modalEditar");

    if (modalEditar) {
        modalEditar.addEventListener("show.bs.modal", function (event) {

            const button = event.relatedTarget;
            const fila = button.closest("tr");
            const celdas = fila.querySelectorAll("td");
            const form = modalEditar.querySelector("#formEditarCliente");

            form.querySelector("#cedula_edit").value = celdas[0].innerText.trim();
            form.querySelector("#nombre_usuario_edit").value = celdas[1].innerText.trim();
            form.querySelector("#apellido_usuario_edit").value = celdas[2].innerText.trim();
            form.querySelector("#telefono_edit").value = celdas[3].innerText.trim();
            form.querySelector("#direccion_edit").value = celdas[4].innerText.trim();
            form.querySelector("#correo_edit").value = celdas[5].innerText.trim();
            form.querySelector("#status_edit").value = celdas[6].dataset.status;
            form.querySelector("#cod_rol_edit").value = button.getAttribute("data-rol");
        });
    }

    const modalEliminar = document.getElementById("modalEliminarCliente");

    if (modalEliminar) {
        modalEliminar.addEventListener("show.bs.modal", function (event) {

            const button = event.relatedTarget;
            const form = modalEliminar.querySelector("#formEliminarCliente");

            form.querySelector("#cedula_eliminar").value =
                button.getAttribute("data-cedula");

            document.getElementById("nombre_usuario").innerText =
                button.getAttribute("data-nombre");
        });
    }

    $("#btnCerrarModal").on("click", function () {
        const form = $("#formRegistrarCliente");

        form[0].reset();
        form.parsley().reset();
        form.find(".is-invalid, .is-valid").removeClass("is-invalid is-valid");
        form.find(".invalid-feedback").hide();
    });

    $("#btnCerrar, #btnClose").on("click", function () {
        const form = $("#formEditarCliente");

        form.parsley().reset();
        form.find(".is-invalid, .is-valid").removeClass("is-invalid is-valid");
        form.find(".invalid-feedback").hide();
    });


    $("#correo_reg, #correo_edit").on("input", function () {
        const correo = this.value.trim();
        const regexCorreo = /^[a-zA-Z0-9._%+-]+@(gmail|outlook|hotmail|yahoo).com$/;


        if (correo === "") {
            $(this).removeClass("is-invalid is-valid");
            $(this).next(".invalid-feedback").hide();
            return;
        }

        if (!regexCorreo.test(correo)) {
            mostrarError(this, "Ingrese un correo válido  como gmail.com, outlook.com, hotmail.com o yahoo.com");
        } else {
            $(this).removeClass("is-invalid").addClass("is-valid");
            $(this).next(".invalid-feedback").hide();
        }
        

    });

});