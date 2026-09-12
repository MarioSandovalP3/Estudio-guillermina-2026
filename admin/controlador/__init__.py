from admin.controlador import panel
from admin.controlador import cliente
from admin.controlador import rol
from admin.controlador import empresa
from admin.controlador import especialidad
from admin.controlador import usuarios
from admin.controlador import tipopagos
from admin.controlador import mantenimiento
from admin.controlador import pagos
from admin.controlador import pagospersonal
from admin.controlador import permisos
from admin.controlador import personal
from admin.controlador import tiposervicio
from admin.controlador import unidadmedida
from admin.controlador import presentacion 
from admin.controlador import unidad
from admin.controlador import moneda
from admin.controlador import disponibilidad 
from admin.controlador import reserva
from admin.controlador import login
from admin.controlador import inicio
from admin.controlador import perfil
from admin.controlador import marca
from admin.controlador import proveedor
from admin.controlador import tipoproducto
from admin.controlador import categoria
from admin.controlador import promocion
from admin.controlador import producto
from admin.controlador import compra
from admin.controlador import bitacora
from admin.controlador import misreservas
from admin.controlador import reservacliente
from admin.controlador import reporte_cliente
from admin.controlador import reporte_reserva
from admin.controlador import reporte_servicio
from admin.controlador import reporte_pago_estadistico
from admin.controlador import reporte_reserva_estadistico
from admin.controlador import reporte_pago
from admin.controlador import reporte_producto
from admin.controlador import reporte_producto_estadistico

controladores = {
    
    "reporte_cliente": reporte_cliente,
    "reporte_reserva": reporte_reserva,
    "reporte_servicio": reporte_servicio,
    "reporte_pago_estadistico": reporte_pago_estadistico,
    "reporte_reserva_estadistico": reporte_reserva_estadistico,
    "reporte_pago": reporte_pago,
    "reporte_producto": reporte_producto,
    "reporte_producto_estadistico": reporte_producto_estadistico,

    "panel": panel,
    "cliente": cliente,
    "rol": rol,
    "empresa": empresa,
    "especialidad": especialidad,
    "usuarios": usuarios,
    "tipopagos": tipopagos,
    "permisos": permisos,
    "tiposervicio": tiposervicio,
    "personal": personal,
    "mantenimiento": mantenimiento,
   "unidadmedida": unidadmedida, 
    "marca": marca,
    "proveedor": proveedor,
    "tipoproducto": tipoproducto,
    "categoria": categoria,
    "promocion": promocion,

    "producto": producto,
    "compra": compra,
    "unidad": unidad,
    "disponibilidad": disponibilidad,
    "moneda": moneda,
    "reserva": reserva,
    "reservacliente": reservacliente,
   "misreservas": misreservas,
    "login": login,
    "inicio": inicio,
    "perfil": perfil,
    "pagos": pagos,
    "pagospersonal": pagospersonal,
    "bitacora": bitacora,
    "presentacion": presentacion
  
}