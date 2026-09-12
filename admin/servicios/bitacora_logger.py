from flask import request, session
from admin.modelo.bitacora import BitacoraModelo


def _obtener_modulo(ruta):
    if ruta:
        return str(ruta).lower().split(".")[-1].split("/")[0] or "inicio"

    return (
        request.args.get("ruta", "")
        or request.endpoint
        or request.path.lstrip("/")
        or "inicio"
    )


def _obtener_accion():
    if request.method == "POST":
        if request.form.get("registrar"):
            return "Registrar"
        if request.form.get("actualizar"):
            return "Actualizar"
        if request.form.get("eliminar"):
            return "Eliminar"
        return "Buscar"

    return "Consultar"


def _obtener_entidad_y_campo(modulo):
    mapeo = {
        "producto": ("producto", "nombre_producto"),
        "categoria": ("categoría", "nombre_categoria"),
        "marca": ("marca", "nombre_marca"),
        "usuario": ("usuario", "nombre_usuario"),
        "usuarios": ("usuario", "nombre_usuario"),
        "personal": ("personal", "nombre_personal"),
        "cliente": ("cliente", "nombre_cliente"),
        "proveedor": ("proveedor", "nombre_proveedor"),
        "servicio": ("servicio", "nombre_servicio"),
        "promocion": ("promoción", "nombre_promocion"),
        "presentacion": ("presentación", "nombre_presentacion"),
        "empresa": ("empresa", "nombre_empresa"),
        "moneda": ("moneda", "nombre_moneda"),
        "unidad": ("unidad", "nombre_unidad"),
        "unidadmedida": ("unidad de medida", "nombre_medida"),
        "tipoproducto": ("tipo de producto", "nombre_tipo_producto"),
        "tiposervicios": ("tipo de servicio", "nombre_tipo_servicio"),
        "tipopagos": ("tipo de pago", "nombre_tipopago"),
        "compra": ("compra", "cod_compra"),
        "reservas": ("reserva", "cod_reserva"),
        "disponibilidad": ("disponibilidad", "cod_disponibilidad"),
        "permisos": ("permiso", "cod_permiso"),
        "perfil": ("perfil", "cod_perfil"),
        "rol": ("rol", "cod_rol"),
    }

    return mapeo.get(modulo, (modulo.replace("_", " "), None))


def _obtener_nombre(campo):
    if campo:
        nombre = request.form.get(campo)
        if nombre:
            return nombre

    return (
        request.form.get("nombre")
        or request.form.get("descripcion")
        or request.form.get("titulo")
        or request.form.get("cedula")
        or request.form.get("cod_rol")
        or request.form.get("cod_producto")
        or request.form.get("cod_categoria")
        or request.form.get("cod_marca")
        or request.form.get("cod_cliente")
        or request.form.get("cod_proveedor")
        or request.form.get("cod_compra")
        or request.form.get("cod_reserva")
    )


def _construir_mensaje_bitacora(modulo, accion, nombre=None):
    entidad, campo = _obtener_entidad_y_campo(modulo)
    nombre = nombre or _obtener_nombre(campo)

    verbos = {
        "Registrar": "registró",
        "Actualizar": "actualizó",
        "Eliminar": "eliminó",
        "Buscar": "buscó",
        "Consultar": "consultó",
    }

    if accion in verbos and nombre:
        return f"Se {verbos[accion]} {entidad} {nombre}".strip()

    if accion in verbos:
        return f"Se {verbos[accion]} {entidad}".strip()

    return f"{accion} {entidad}".strip()


def guardar_bitacora(modulo, accion, descripcion=None, cedula=None, ip=None):
    cedula_usuario = cedula if cedula is not None else session.get("cedula") or "anonimo"
    detalle = descripcion or accion or "Bitácora"

    modelo_bitacora = BitacoraModelo()
    return modelo_bitacora.registrar(cedula_usuario, modulo, accion, descripcion=detalle, ip=ip)


def registrar_cierre_sesion():
    cedula_usuario = session.get("cedula")
    if cedula_usuario:
        guardar_bitacora(
            modulo="Login",
            accion="CIERRE_SESION",
            descripcion="Cierre de sesión",
            cedula=cedula_usuario,
            ip=request.remote_addr,
        )
    session.clear()
    return True


def registrar_movimiento_sistema(ruta=None, response=None):
    if request.path.startswith("/static") or request.path.startswith("/favicon"):
        return

    cedula_usuario = session.get("cedula") or request.form.get("cedula") or "anonimo"
    modulo = _obtener_modulo(ruta)
    accion = _obtener_accion()
    if accion not in {"Registrar", "Actualizar", "Eliminar"}:
        return

    nombre = None
    if modulo == "compra" and accion == "Registrar" and response is not None:
        datos_respuesta = response.get_json(silent=True) or {}
        nombre = datos_respuesta.get("cod_compra")

    accion_completa = _construir_mensaje_bitacora(modulo, accion, nombre)

    guardar_bitacora(modulo, accion, accion_completa, cedula=cedula_usuario, ip=request.remote_addr)
