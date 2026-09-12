console.log('Abrio componenye intelijente  .js');

document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("btnAsesorIA");
    const chat = document.getElementById("iaChat");
    const close = document.getElementById("cerrarIA");
    const send = document.getElementById("iaSend");
    const input = document.getElementById("iaInput");
    const body = document.getElementById("iaBody");
    const btnSubirImagen = document.getElementById("btnSubirImagen");
    const imagenInput = document.getElementById("iaImagenInput");
    const btnIniciarReserva = document.getElementById("btnIniciarReserva");
    const imagenSimulacion = document.getElementById("imagenSimulacion");
    const efectoSimulacion = document.getElementById("efectoSimulacion");
    const resultadoSimulacion = document.getElementById("resultadoSimulacion");
    const btnUsarSimulacion = document.getElementById("btnUsarSimulacion");
    const modalSimulacion = new bootstrap.Modal(document.getElementById("modalSimulacionIA"));
    const modalReserva = new bootstrap.Modal(document.getElementById("modalReservaIA"));

    btn.addEventListener("click", function () {
        chat.classList.remove("hidden");
        input.focus();
    });

    close.addEventListener("click", function () {
        chat.classList.add("hidden");
    });

    send.addEventListener("click", procesarMensaje);

    input.addEventListener("keypress", function (e) {
        if (e.key === "Enter") {
            procesarMensaje();
        }
    });

    btnSubirImagen.addEventListener("click", function () {
        imagenInput.click();
    });

    imagenInput.addEventListener("change", function () {
        const archivo = this.files[0];

        if (!archivo) {
            return;
        }

        if (!archivo.type.startsWith("image/")) {
            agregarBot("❌ El archivo seleccionado no es una imagen.");
            return;
        }

        const lector = new FileReader();

        lector.onload = function (e) {
            imagenSimulacion.src = e.target.result;

            agregarUsuario("📸 He subido una imagen para analizar.");

            setTimeout(function () {
                agregarBot("🔎 Imagen recibida correctamente.<br><br>Ahora puedes elegir qué deseas simular: cabello, colorimetría o uñas.");

                document.getElementById("opcionesCabello").classList.add("hidden");
                document.getElementById("opcionesColor").classList.add("hidden");
                document.getElementById("opcionesUnas").classList.add("hidden");

                modalSimulacion.show();
            }, 500);
        };

        lector.readAsDataURL(archivo);
    });

    document.querySelectorAll(".btn-simulacion").forEach(function (boton) {
        boton.addEventListener("click", function () {
            const tipo = this.dataset.tipo;

            document.getElementById("opcionesCabello").classList.add("hidden");
            document.getElementById("opcionesColor").classList.add("hidden");
            document.getElementById("opcionesUnas").classList.add("hidden");

            if (tipo === "cabello") {
                document.getElementById("opcionesCabello").classList.remove("hidden");
                resultadoSimulacion.textContent = "💇 Selecciona el estilo de cabello que deseas simular.";
            }

            if (tipo === "color") {
                document.getElementById("opcionesColor").classList.remove("hidden");
                resultadoSimulacion.textContent = "🎨 Selecciona el color que deseas simular.";
            }

            if (tipo === "unas") {
                document.getElementById("opcionesUnas").classList.remove("hidden");
                resultadoSimulacion.textContent = "💅 Selecciona el diseño de uñas que deseas simular.";
            }
        });
    });

    document.querySelectorAll(".opcion-simulacion").forEach(function (boton) {
        boton.addEventListener("click", function () {
            const efecto = this.dataset.efecto;

            imagenSimulacion.className = "ia-preview-image";
            imagenSimulacion.classList.add("efecto-" + efecto);

            document.querySelectorAll(".opcion-simulacion").forEach(function (item) {
                item.classList.remove("active");
            });

            this.classList.add("active");

            let texto = "";

            switch (efecto) {
                case "cabello-corto":
                    texto = "💇 Simulación: cabello corto.";
                    break;
                case "cabello-largo":
                    texto = "💇 Simulación: cabello largo.";
                    break;
                case "rojo":
                    texto = "🎨 Simulación: cabello color rojo.";
                    break;
                case "amarillo":
                    texto = "🎨 Simulación: cabello color amarillo.";
                    break;
                case "rosa":
                    texto = "🎨 Simulación: cabello color rosa.";
                    break;
                case "unas-largas":
                    texto = "💅 Simulación: uñas largas.";
                    break;
                case "unas-cortas":
                    texto = "💅 Simulación: uñas cortas.";
                    break;
                case "unas-rojas":
                    texto = "💅 Simulación: uñas rojas.";
                    break;
                case "unas-rosas":
                    texto = "💅 Simulación: uñas rosas.";
                    break;
                case "unas-cuadradas":
                    texto = "💅 Simulación: uñas con forma cuadrada.";
                    break;
                case "unas-almendra":
                    texto = "💅 Simulación: uñas con forma almendra.";
                    break;
            }

            resultadoSimulacion.textContent = texto;
            document.getElementById("simulacionAcciones").classList.remove("hidden");
        });
    });

    btnUsarSimulacion.addEventListener("click", function () {
        modalSimulacion.hide();

        setTimeout(function () {
            agregarUserReserva();
            modalReserva.show();
        }, 400);
    });

    btnIniciarReserva.addEventListener("click", function () {
        agregarUserReserva();
        modalReserva.show();
    });

    document.getElementById("btnContinuarReserva").addEventListener("click", function () {
        const nombre = document.getElementById("iaNombre").value.trim();
        const apellido = document.getElementById("iaApellido").value.trim();
        const cedula = document.getElementById("iaCedula").value.trim();
        const servicio = document.getElementById("iaServicio").value;
        const fecha = document.getElementById("iaFecha").value;
        const hora = document.getElementById("iaHora").value;
        const especialista = document.getElementById("iaEspecialista").value;

        if (!nombre || !apellido || !cedula || !servicio || !fecha || !hora || !especialista) {
            document.getElementById("mensajeReservaIA").innerHTML = `
                <div class="alert alert-danger py-2">
                    ❌ Debes completar todos los datos de la reserva.
                </div>
            `;
            return;
        }

        document.getElementById("resumenCliente").textContent = nombre + " " + apellido;
        document.getElementById("resumenCedula").textContent = cedula;
        document.getElementById("resumenServicio").textContent = servicio;
        document.getElementById("resumenFecha").textContent = formatearFecha(fecha);
        document.getElementById("resumenHora").textContent = hora;
        document.getElementById("resumenEspecialista").textContent = especialista;

        document.getElementById("reservaPaso1").classList.add("hidden");
        document.getElementById("reservaPaso2").classList.remove("hidden");
    });

    document.getElementById("btnEditarReserva").addEventListener("click", function () {
        document.getElementById("reservaPaso2").classList.add("hidden");
        document.getElementById("reservaPaso1").classList.remove("hidden");
    });

    document.getElementById("btnConfirmarReserva").addEventListener("click", function () {
        document.getElementById("reservaPaso2").classList.add("hidden");
        document.getElementById("reservaPaso3").classList.remove("hidden");

        agregarBot("✅ Reserva simulada confirmada correctamente.");
    });

    document.getElementById("iaCedula").addEventListener("input", function () {
        this.value = this.value.replace(/\D/g, "").slice(0, 8);
    });

    document.getElementById("iaNombre").addEventListener("input", function () {
        this.value = this.value.replace(/[^a-zA-ZÁÉÍÓÚáéíóúÑñ\s]/g, "");
    });

    document.getElementById("iaApellido").addEventListener("input", function () {
        this.value = this.value.replace(/[^a-zA-ZÁÉÍÓÚáéíóúÑñ\s]/g, "");
    });

    function procesarMensaje() {
        const msg = input.value.trim();

        if (!msg) {
            return;
        }

        agregarUsuario(msg);

        input.value = "";

        setTimeout(function () {
            const texto = msg.toLowerCase();

            if (texto.includes("imagen") || texto.includes("foto") || texto.includes("analizar")) {
                agregarBot("📸 Perfecto. Sube una imagen para comenzar el análisis.");
                imagenInput.click();
                return;
            }

            if (texto.includes("reserva") || texto.includes("cita")) {
                agregarBot("📅 Perfecto. Vamos a preparar tu reserva.");
                modalReserva.show();
                return;
            }

            if (texto.includes("cabello") || texto.includes("pelo")) {
                agregarBot("💇 Puedes subir una imagen y luego seleccionar cabello corto o largo.");
                return;
            }

            if (texto.includes("color") || texto.includes("rojo") || texto.includes("rosa") || texto.includes("amarillo")) {
                agregarBot("🎨 Puedes subir una imagen para simular diferentes colores de cabello.");
                return;
            }

            if (texto.includes("uña") || texto.includes("uñas")) {
                agregarBot("💅 Puedes subir una imagen para simular longitud, forma y colores de uñas.");
                return;
            }

            agregarBot("✨ Puedo ayudarte a analizar una imagen, simular cabello, colorimetría, uñas o iniciar una reserva.");
        }, 500);
    }

    function agregarUsuario(texto) {
        body.innerHTML += `<div class="ia-msg user">💬 ${escapeHTML(texto)}</div>`;
        scrollChat();
    }

    function agregarBot(texto) {
        body.innerHTML += `<div class="ia-msg bot">${texto}</div>`;
        scrollChat();
    }

    function agregarUserReserva() {
        agregarBot("📅 Vamos a preparar tu reserva. Completa tus datos para continuar.");
    }

    function scrollChat() {
        body.scrollTop = body.scrollHeight;
    }

    function formatearFecha(fecha) {
        const partes = fecha.split("-");

        if (partes.length !== 3) {
            return fecha;
        }

        return partes[2] + "/" + partes[1] + "/" + partes[0];
    }

    function escapeHTML(texto) {
        return $("<div>").text(texto).html();
    }

    document.getElementById("modalReservaIA").addEventListener("hidden.bs.modal", function () {
        document.getElementById("reservaPaso1").classList.remove("hidden");
        document.getElementById("reservaPaso2").classList.add("hidden");
        document.getElementById("reservaPaso3").classList.add("hidden");
        document.getElementById("mensajeReservaIA").innerHTML = "";
    });
});