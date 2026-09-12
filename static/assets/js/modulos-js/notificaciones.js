console.log("Cargo notificaciones");

document.addEventListener("DOMContentLoaded", function () {
    const dropdown = document.getElementById("notificacionesDropdown");
    if (!dropdown) return;

    const contador = dropdown.querySelector(".badge");
    const panel = dropdown.parentElement.querySelector(".dropdown-menu");
    if (!panel) return;

    const STORAGE = "notificaciones_estado";
    let estado = cargarEstado();

    function hoy() {
        const d = new Date();
        return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
    }

    function estadoInicial() {
        return { fecha: hoy(), clientes: 0, reservas: 0, compras: 0, pagos: 0 };
    }

    function cargarEstado() {
        try {
            const datos = JSON.parse(localStorage.getItem(STORAGE) || "null");

            if (!datos || datos.fecha !== hoy()) {
                const nuevo = estadoInicial();
                localStorage.setItem(STORAGE, JSON.stringify(nuevo));
                return nuevo;
            }

            return {
                fecha: datos.fecha,
                clientes: Number(datos.clientes) || 0,
                reservas: Number(datos.reservas) || 0,
                compras: Number(datos.compras) || 0,
                pagos: Number(datos.pagos) || 0
            };
        } catch {
            return estadoInicial();
        }
    }

    function guardarEstado() {
        localStorage.setItem(STORAGE, JSON.stringify(estado));
    }

    function contenedor() {
        return panel.querySelector(".contenedor-notificaciones");
    }

    function crear(titulo, texto, icono, color, id) {
        const elemento = document.createElement("div");

        elemento.className = "dropdown-item px-4 py-3 border-bottom notificacion-item";
        elemento.dataset.id = id;
        elemento.style.whiteSpace = "normal";

        elemento.innerHTML = `
            <div class="d-flex align-items-start">
                <div class="me-3">
                    <div class="rounded-circle ${color}-subtle d-flex align-items-center justify-content-center" style="width:48px;height:48px">
                        <i class="bi ${icono} text-${color} fs-4"></i>
                    </div>
                </div>
                <div class="flex-grow-1">
                    <div class="d-flex justify-content-between align-items-start">
                        <strong class="text-dark">${titulo}</strong>
                        <button type="button" class="btn btn-sm btn-outline-danger border-0 btn-eliminar-notificacion" title="Eliminar notificación">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                    <p class="mb-0 text-muted small">${texto}</p>
                </div>
            </div>
        `;

        elemento.querySelector(".btn-eliminar-notificacion").addEventListener("click", function (e) {
            e.preventDefault();
            e.stopPropagation();
            eliminar(id);
        });

        return elemento;
    }

    function eliminar(id) {
        const elemento = document.querySelector(`[data-id="${id}"]`);
        if (elemento) elemento.remove();

        if (id.startsWith("cliente_"))
            estado.clientes = Number(id.split("_")[1]) * 3;

        if (id.startsWith("reserva_"))
            estado.reservas = Number(id.split("_")[1]) * 3;

        if (id === "compras")
            estado.compras = estado.totalComprasActual;

        if (id === "pagos")
            estado.pagos = estado.totalPagosActual;

        guardarEstado();
        actualizarContador();
    }

    function construir(datos) {
        const cont = contenedor();
        if (!cont) return;

        cont.innerHTML = "";
        let cantidad = 0;

        const clientes = Number(datos.clientes) || 0;
        estado.totalClientesActual = clientes;

        for (
            let i = Math.floor(estado.clientes / 3) + 1;
            i <= Math.floor(clientes / 3);
            i++
        ) {
            cont.appendChild(crear(
                "Nuevos clientes",
                `Se han registrado ${i * 3} clientes hoy.`,
                "bi-person-plus-fill",
                "primary",
                `cliente_${i}`
            ));
            cantidad++;
        }

        const reservas = Number(datos.reservas?.[0]?.total) || 0;
        estado.totalReservasActual = reservas;

        for (
            let i = Math.floor(estado.reservas / 3) + 1;
            i <= Math.floor(reservas / 3);
            i++
        ) {
            cont.appendChild(crear(
                "Nuevas reservas",
                `Se han registrado ${i * 3} reservas hoy.`,
                "bi-calendar-check-fill",
                "success",
                `reserva_${i}`
            ));
            cantidad++;
        }

        const compras = Number(datos.compras) || 0;
        estado.totalComprasActual = compras;

        if (compras > estado.compras) {
            const nuevas = compras - estado.compras;

            cont.appendChild(crear(
                "Nueva compra",
                nuevas === 1
                    ? "Se ha registrado 1 nueva compra hoy."
                    : `Se han registrado ${nuevas} nuevas compras hoy.`,
                "bi-cart-check-fill",
                "danger",
                "compras"
            ));

            cantidad++;
        }

        const pagos = Number(datos.pagos) || 0;
        estado.totalPagosActual = pagos;

        if (pagos > estado.pagos) {
            const nuevos = pagos - estado.pagos;

            cont.appendChild(crear(
                "Nuevo pago",
                nuevos === 1
                    ? "Se ha registrado 1 nuevo pago hoy."
                    : `Se han registrado ${nuevos} nuevos pagos hoy.`,
                "bi-cash-stack",
                "info",
                "pagos"
            ));

            cantidad++;
        }

        guardarEstado();
        actualizarContador(cantidad);
    }

    function actualizarContador(cantidad) {
        if (!contador) return;

        contador.textContent = cantidad || "";
        contador.style.display = cantidad ? "inline-block" : "none";

        const resumen = panel.querySelector(".notificaciones-resumen");
        const total = panel.querySelector(".notificaciones-total");

        if (resumen)
            resumen.textContent = cantidad
                ? `Tienes ${cantidad} notificaciones nuevas`
                : "No tienes notificaciones nuevas";

        if (total)
            total.textContent = cantidad;
    }

    function actualizarContadorDesdeDOM() {
        const cont = contenedor();
        if (!cont) return;

        actualizarContador(
            cont.querySelectorAll(".notificacion-item").length
        );
    }

    function marcarTodas() {
        const datos = window.notificacionesDatos;
        if (!datos) return;

        estado.clientes = Number(datos.clientes) || 0;
        estado.reservas = Number(datos.reservas?.[0]?.total) || 0;
        estado.compras = Number(datos.compras) || 0;
        estado.pagos = Number(datos.pagos) || 0;

        guardarEstado();

        const cont = contenedor();
        if (cont) cont.innerHTML = "";

        actualizarContador(0);
    }

    async function consultar() {
        try {
            const respuesta = await fetch("/notificaciones", {
                method: "GET",
                headers: { "X-Requested-With": "XMLHttpRequest" },
                cache: "no-store"
            });

            if (!respuesta.ok) return;

            const datos = await respuesta.json();
            if (!datos.status) return;

            if (estado.fecha !== datos.fecha) {
                estado = {
                    fecha: datos.fecha,
                    clientes: 0,
                    reservas: 0,
                    compras: 0,
                    pagos: 0
                };
                guardarEstado();
            }

            window.notificacionesDatos = datos;
            construir(datos);
        } catch { }
    }

    panel.querySelectorAll("button").forEach(function (boton) {
        const texto = boton.textContent.trim();

        if (texto.includes("Marcar todas")) {
            boton.addEventListener("click", function (e) {
                e.preventDefault();
                e.stopPropagation();
                marcarTodas();
            });
        }

        if (texto.includes("Eliminar todas")) {
            boton.addEventListener("click", function (e) {
                e.preventDefault();
                e.stopPropagation();
                marcarTodas();
            });
        }
    });

    consultar();
    setInterval(consultar, 5000);
});


let alertaUltima = null;
let alertaHoy = null;
let temporizadorUltima = null;

const STORAGE_ULTIMA = "ultima_cancelacion_mostrada";
const STORAGE_HOY = "cancelaciones_hoy_estado";

function fechaHoy() {
    const d = new Date();
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

function fechaMostrar(fecha) {
    if (!fecha) return "";
    const p = fecha.split("-");
    return p.length === 3 ? `${p[2]}/${p[1]}/${p[0]}` : fecha;
}

function estadoHoy() {
    const hoy = fechaHoy();

    try {
        const datos = JSON.parse(localStorage.getItem(STORAGE_HOY) || "null");

        if (!datos || datos.fecha !== hoy) {
            const nuevo = { fecha: hoy, eliminada: false };
            localStorage.setItem(STORAGE_HOY, JSON.stringify(nuevo));
            return nuevo;
        }

        return datos;
    } catch {
        return { fecha: hoy, eliminada: false };
    }
}

function guardarEstadoHoy(estado) {
    localStorage.setItem(STORAGE_HOY, JSON.stringify(estado));
}

function mostrarUltima(datos) {
    const contenedor = document.getElementById("contenedorAlertaCancelacion");
    if (!contenedor) return;

    if (alertaUltima) alertaUltima.remove();
    if (temporizadorUltima) clearTimeout(temporizadorUltima);

    alertaUltima = document.createElement("div");
    alertaUltima.className = "alerta-cancelacion-reserva";

    alertaUltima.innerHTML = `
        <div class="alerta-cancelacion-icono">
            <i class="bi bi-calendar-x-fill"></i>
        </div>
        <div class="alerta-cancelacion-contenido">
            <strong>Reserva cancelada</strong>
            <span>
                La reserva de <b>${datos.cliente}</b>
                del <b>${fechaMostrar(datos.fecha)}</b>
                a las <b>${datos.hora}</b> fue cancelada.
            </span>
        </div>
    `;

    contenedor.appendChild(alertaUltima);

    requestAnimationFrame(() => {
        alertaUltima?.classList.add("mostrar-alerta-cancelacion");
    });

    temporizadorUltima = setTimeout(() => {
        if (!alertaUltima) return;

        alertaUltima.classList.remove("mostrar-alerta-cancelacion");
        alertaUltima.classList.add("ocultar-alerta-cancelacion");

        setTimeout(() => {
            alertaUltima?.remove();
            alertaUltima = null;
        }, 400);
    }, 5000);
}

function mostrarCancelacionesHoy(cancelaciones) {
    const contenedor = document.getElementById("contenedorCancelacionesHoy");
    if (!contenedor) return;

    const estado = estadoHoy();

    if (estado.eliminada) {
        alertaHoy?.remove();
        alertaHoy = null;
        return;
    }

    const hoy = fechaHoy();
    const lista = cancelaciones.filter(c => c.fecha === hoy);

    if (!lista.length || alertaHoy) return;

    alertaHoy = document.createElement("div");
    alertaHoy.className = "alerta-cancelaciones-hoy";

    if (lista.length === 1) {
        const c = lista[0];

        alertaHoy.innerHTML = `
            <div class="cancelaciones-hoy-icono">
                <i class="bi bi-calendar-x-fill"></i>
            </div>
            <div class="cancelaciones-hoy-contenido">
                <strong>Reserva cancelada</strong>
                <span>
                    La reserva de <b>${c.cliente}</b>
                    del <b>${fechaMostrar(c.fecha)}</b>
                    a las <b>${c.hora}</b>
                    fue cancelada para el día de hoy.
                </span>
            </div>
            <button type="button"
                class="btn-eliminar-cancelaciones-hoy"
                title="Eliminar">
                <i class="bi bi-trash3-fill"></i>
            </button>
        `;
    } else {
        alertaHoy.innerHTML = `
            <div class="cancelaciones-hoy-icono">
                <i class="bi bi-calendar-x-fill"></i>
            </div>
            <div class="cancelaciones-hoy-contenido">
                <strong>Reservas canceladas</strong>
                <span>
                    <b>${lista.length}</b>
                    reservas fueron canceladas para el día de hoy.
                </span>
            </div>
            <button type="button"
                class="btn-eliminar-cancelaciones-hoy"
                title="Eliminar">
                <i class="bi bi-trash3-fill"></i>
            </button>
        `;
    }

    contenedor.appendChild(alertaHoy);

    alertaHoy.querySelector(".btn-eliminar-cancelaciones-hoy")
        ?.addEventListener("click", () => {
            const estado = estadoHoy();
            estado.eliminada = true;
            guardarEstadoHoy(estado);

            alertaHoy?.remove();
            alertaHoy = null;
        });
}

async function consultarCancelaciones() {
    try {
        const respuesta = await fetch(
            "/notificaciones?cancelacion=1&_=" + Date.now(),
            {
                method: "GET",
                headers: { "X-Requested-With": "XMLHttpRequest" },
                cache: "no-store"
            }
        );

        if (!respuesta.ok) return;

        const datos = await respuesta.json();
        if (!datos.status) return;

        if (datos.ultima) {
            const actual = Number(datos.ultima.cod_servicio);
            const anterior = Number(localStorage.getItem(STORAGE_ULTIMA) || 0);

            if (actual > anterior) {
                localStorage.setItem(STORAGE_ULTIMA, actual);
                mostrarUltima(datos.ultima);
            }
        }

        if (Array.isArray(datos.cancelaciones)) {
            mostrarCancelacionesHoy(datos.cancelaciones);
        }

    } catch (error) {
        console.error("Error consultando cancelaciones:", error);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    consultarCancelaciones();
    setInterval(consultarCancelaciones, 2000);
});



document.addEventListener("DOMContentLoaded", function () {

    const contenedor = document.getElementById("contenedordevolcionstok");
    if (!contenedor) return;

    let alertaMostrada = false;
    let procesoEjecutado = false;
    const MODO_PRUEBA = false;
    const CLAVE_NOTIFICACION = "reservas_devolucion_stock_pendiente";

    function obtenerNotificacionGuardada() {
        const datos = localStorage.getItem(CLAVE_NOTIFICACION);
        if (!datos) return null;

        try {
            return JSON.parse(datos);
        } catch (error) {
            localStorage.removeItem(CLAVE_NOTIFICACION);
            return null;
        }
    }

    function guardarNotificacion(devoluciones) {
        localStorage.setItem(
            CLAVE_NOTIFICACION,
            JSON.stringify({
                devoluciones: devoluciones,
                fecha_guardado: new Date().toISOString()
            })
        );
    }

    function eliminarNotificacion() {
        localStorage.removeItem(CLAVE_NOTIFICACION);
    }

    function mostrarNotificacionGuardada() {
        const notificacion = obtenerNotificacionGuardada();
        if (!notificacion) return false;

        const devoluciones = notificacion.devoluciones || [];

        if (devoluciones.length === 0) {
            eliminarNotificacion();
            return false;
        }

        mostrarAlerta(devoluciones);
        return true;
    }

    function consultarDevoluciones() {
        if (procesoEjecutado) return;

        procesoEjecutado = true;

        fetch(
            "/notificaciones?devolucion_stock=1&_=" + Date.now(),
            {
                method: "GET",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                },
                cache: "no-store"
            }
        )
        .then(function (response) {
            if (!response.ok) {
                throw new Error("Error HTTP: " + response.status);
            }

            return response.json();
        })
        .then(function (data) {
            if (!data.status) return;

            const devoluciones = data.devoluciones || [];
            if (devoluciones.length === 0) return;

            guardarNotificacion(devoluciones);
            mostrarAlerta(devoluciones);
        })
        .catch(function () {
            procesoEjecutado = false;
        });
    }

    function mostrarAlerta(devoluciones) {
        if (alertaMostrada) return;

        alertaMostrada = true;

        const cantidad = devoluciones.length;

        let clientes = "";

        devoluciones.forEach(function (reserva) {
            clientes += `
                <div style="
                    display:flex;
                    align-items:center;
                    gap:7px;
                    margin-bottom:5px;
                    font-size:11px;
                    color:#444;
                ">
                    <div style="
                        width:21px;
                        height:21px;
                        min-width:21px;
                        border-radius:50%;
                        background:#f8e7f0;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                    ">
                        <i class="bi bi-person-fill"
                            style="
                                color:#a7657c;
                                font-size:10px;
                            "
                        ></i>
                    </div>
                    <span>${reserva.cliente || "Cliente"}</span>
                </div>
            `;
        });

        Swal.fire({
            html: `
                <div style="
                    display:flex;
                    align-items:center;
                    gap:14px;
                    width:100%;
                    text-align:left;
                ">
                    <div style="
                        flex:1;
                        min-width:0;
                    ">
                        <div style="
                            display:flex;
                            align-items:center;
                            gap:8px;
                            margin-bottom:7px;
                        ">
                            <div style="
                                width:31px;
                                height:31px;
                                min-width:31px;
                                border-radius:50%;
                                background:#f8e7f0;
                                display:flex;
                                align-items:center;
                                justify-content:center;
                            ">
                                <i class="bi bi-bell-fill"
                                    style="
                                        color:#a7657c;
                                        font-size:15px;
                                    "
                                ></i>
                            </div>

                            <div>
                                <div style="
                                    font-size:13px;
                                    font-weight:700;
                                    color:#333;
                                ">
                                    Reservas no realizadas
                                </div>

                                <div style="
                                    font-size:9px;
                                    color:#999;
                                    margin-top:2px;
                                ">
                                    Al llegar las 08:00 PM
                                </div>
                            </div>
                        </div>

                        <div style="
                            font-size:10px;
                            color:#777;
                            margin-bottom:7px;
                        ">
                            ${cantidad}
                            reserva${cantidad !== 1 ? "s" : ""}
                            de hoy
                        </div>

                        <div>
                            ${clientes}
                        </div>

                        <div style="
                            margin-top:7px;
                            padding-top:7px;
                            border-top:1px solid #eeeeee;
                            font-size:9px;
                            color:#777;
                            line-height:1.4;
                        ">
                            Los productos seleccionados en la reserva
                            fueron devueltos al stock correctamente.
                        </div>
                    </div>

                    <div style="
                        width:1px;
                        height:85px;
                        background:#eeeeee;
                        flex-shrink:0;
                    "></div>

                    <button
                        type="button"
                        id="btnEliminarNotificacionStock"
                        title="Eliminar notificación"
                        style="
                            width:42px;
                            height:42px;
                            min-width:42px;
                            border:0;
                            border-radius:50%;
                            background:#fde8e8;
                            display:flex;
                            align-items:center;
                            justify-content:center;
                            cursor:pointer;
                            transition:all .2s ease;
                        "
                    >
                        <i class="bi bi-trash3-fill"
                            style="
                                color:#dc3545;
                                font-size:17px;
                                pointer-events:none;
                            "
                        ></i>
                    </button>
                </div>
            `,
            width: "480px",
            padding: "12px 15px",
            position: "top-end",
            toast: true,
            showConfirmButton: false,
            showCloseButton: false,
            allowOutsideClick: false,
            allowEscapeKey: false,
            backdrop: false,
            timer: undefined,

            didOpen: function () {
                const boton = document.getElementById(
                    "btnEliminarNotificacionStock"
                );

                if (!boton) return;

                boton.addEventListener("mouseenter", function () {
                    boton.style.background = "#dc3545";

                    const icono = boton.querySelector("i");
                    if (icono) icono.style.color = "#ffffff";
                });

                boton.addEventListener("mouseleave", function () {
                    boton.style.background = "#fde8e8";

                    const icono = boton.querySelector("i");
                    if (icono) icono.style.color = "#dc3545";
                });

                boton.addEventListener("click", function () {
                    eliminarNotificacion();
                    alertaMostrada = false;
                    Swal.close();
                });
            },

            willClose: function () {
                alertaMostrada = false;
            }
        });
    }

    function programarLas8PM() {
        if (MODO_PRUEBA) {
            consultarDevoluciones();
            return;
        }

        const ahora = new Date();
        const ochoPM = new Date();

        ochoPM.setHours(20, 0, 0, 0);

        const diferencia =
            ochoPM.getTime() - ahora.getTime();

        if (diferencia > 0) {
            setTimeout(function () {
                consultarDevoluciones();
            }, diferencia);

            return;
        }

        consultarDevoluciones();
    }

    if (!mostrarNotificacionGuardada()) {
        programarLas8PM();
    }

});



let alertaEmpresa = null;

async function consultarEmpresaNoRegistrada() {
    try {
        const respuesta = await fetch(
            "/notificaciones?empresa=1&_=" + Date.now(),
            {
                method: "GET",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                },
                cache: "no-store"
            }
        );

        if (!respuesta.ok) {
            throw new Error("Error HTTP: " + respuesta.status);
        }

        const data = await respuesta.json();

        console.log("Respuesta empresa:", data);

        if (data.status === true) {
            mostrarEmpresaNoRegistrada(data.empresa_registrada);
        }

    } catch (error) {
        console.error("Error verificando empresa:", error);
    }
}


function mostrarEmpresaNoRegistrada(empresaRegistrada) {
    const contenedor = document.getElementById("contenedorEmpresaNoRegistrada");

    if (!contenedor) {
        console.error("No existe #contenedorEmpresaNoRegistrada");
        return;
    }

    const registrada =
        empresaRegistrada === true ||
        empresaRegistrada === 1 ||
        empresaRegistrada === "1" ||
        empresaRegistrada === "true";

    if (registrada) {
        if (alertaEmpresa) {
            alertaEmpresa.remove();
            alertaEmpresa = null;
        }

        habilitarModulosEmpresa();
        return;
    }

    if (alertaEmpresa) {
        return;
    }

    alertaEmpresa = document.createElement("div");

    contenedor.style.textAlign = "right";

    alertaEmpresa.style.cssText =
        "display:inline-flex;" +
        "align-items:center;" +
        "gap:12px;" +
        "padding:11px 14px;" +
        "margin-bottom:15px;" +
        "background:#fff8e1;" +
        "border:1px solid #f1d27a;" +
        "border-left:4px solid #e0a800;" +
        "border-radius:10px;" +
        "box-shadow:0 3px 10px rgba(0,0,0,.08);" +
        "width:fit-content;" +
        "max-width:520px;" +
        "text-align:left;";

    alertaEmpresa.innerHTML = `
        <div style="
            width:40px;
            height:40px;
            min-width:40px;
            display:flex;
            align-items:center;
            justify-content:center;
            background:#fff0b3;
            color:#d39e00;
            border-radius:50%;
            font-size:19px;
        ">
            <i class="bi bi-building-exclamation"></i>
        </div>

        <div style="
            display:flex;
            flex-direction:column;
            gap:2px;
        ">
            <strong style="
                color:#856404;
                font-size:14px;
            ">
                Empresa no registrada
            </strong>

            <span style="
                color:#6c5a20;
                font-size:12px;
                line-height:1.4;
            ">
                Registre los datos de la empresa para habilitar los demás módulos.
            </span>
        </div>

        <button
            type="button"
            title="Cerrar"
            style="
                border:0;
                background:transparent;
                color:#856404;
                font-size:14px;
                cursor:pointer;
                padding:4px 6px;
                margin-left:5px;
            "
        >
            <i class="bi bi-x-lg"></i>
        </button>
    `;

    contenedor.appendChild(alertaEmpresa);

    alertaEmpresa.querySelector("button")?.addEventListener("click", function () {
        if (alertaEmpresa) {
            alertaEmpresa.remove();
            alertaEmpresa = null;
        }
    });
}

function habilitarModulosEmpresa() {
    document
        .querySelectorAll('[data-empresa-bloqueado="true"]')
        .forEach(enlace => {

            if (enlace.dataset.href) {
                enlace.setAttribute("href", enlace.dataset.href);
            }

            enlace.style.removeProperty("pointer-events");
            enlace.style.removeProperty("cursor");
            enlace.style.removeProperty("background");
            enlace.style.removeProperty("color");

            if (enlace.classList.contains("sidebar-link")) {

                enlace.style.setProperty("background", "#1f5ceb", "important");
                enlace.style.setProperty("color", "#fff", "important");

                const icono = enlace.querySelector("i");

                if (icono) {
                    icono.style.removeProperty("color");
                    icono.style.setProperty("color", "#fff", "important");
                }

                const texto = enlace.querySelector("span");

                if (texto) {
                    texto.style.removeProperty("color");
                    texto.style.setProperty("color", "#fff", "important");
                }

            } else if (enlace.classList.contains("submenu-link")) {

                enlace.style.removeProperty("color");

                const icono = enlace.querySelector("i");

                if (icono) {
                    icono.style.removeProperty("color");
                }
            }
        });
}

document.addEventListener("DOMContentLoaded", function () {
    consultarEmpresaNoRegistrada();
});

