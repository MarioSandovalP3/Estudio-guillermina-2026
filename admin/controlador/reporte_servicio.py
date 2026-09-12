from admin.modelo.reservas import ReservasModelo
from admin.modelo.empresa import EmpresaModelo
from admin.modelo.inicio import InicioModelo
from flask import request, send_file

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Table,
    TableStyle,
    Spacer,
    Image,
    KeepTogether
)

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import mm
from reportlab.graphics.shapes import Drawing, Line

from datetime import datetime
import tempfile
import os


# =====================================================
# FOOTER PREMIUM
# =====================================================
def footer(canvas, doc):
    canvas.saveState()

    canvas.setTitle("Reporte de Reservas")  # 👈 ESTO ES LO IMPORTANTE

    canvas.setStrokeColor(colors.HexColor("#D4AF37"))
    canvas.setLineWidth(0.8)
    canvas.line(15 * mm, 18 * mm, 195 * mm, 18 * mm)

    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#777777"))

    canvas.drawString(18 * mm, 11 * mm, "Sistema Administrativo ")
    canvas.drawRightString(195 * mm, 11 * mm, datetime.now().strftime("%d/%m/%Y %H:%M"))
    canvas.drawCentredString(105 * mm, 6 * mm, f"Página {doc.page}")

    canvas.restoreState()

# =====================================================
# BORDE EMPRESARIAL
# =====================================================
def borde(canvas, doc):
    canvas.saveState()

    canvas.setStrokeColor(colors.HexColor("#D4AF37"))
    canvas.setLineWidth(1.2)

    canvas.rect(
        10 * mm,
        10 * mm,
        LETTER[0] - 20 * mm,
        LETTER[1] - 20 * mm
    )

    canvas.restoreState()


# =====================================================
# CONTROLADOR
# =====================================================
def handle_request(ruta):

    modelo = ReservasModelo()

    if request.method == "POST" and request.form.get("pdfr"):

        fecha_inicio = request.form.get("fecha_inicio")
        fecha_fin = request.form.get("fecha_fin")

        empresa_modelo = EmpresaModelo()
        empresa_data = empresa_modelo.mostrar()
        empresa = empresa_data[0] if empresa_data else {}

        reservas = modelo.consultarfiltradofecha(fecha_inicio, fecha_fin)

        archivo = os.path.join(tempfile.gettempdir(), "reporte_reservas.pdf")

        doc = SimpleDocTemplate(
            archivo,
            pagesize=LETTER,
            leftMargin=18 * mm,
            rightMargin=18 * mm,
            topMargin=20 * mm,
            bottomMargin=25 * mm
        )

        estilos = getSampleStyleSheet()

        # =====================================================
        # ESTILOS
        # =====================================================
        titulo_style = ParagraphStyle(
            "titulo",
            parent=estilos["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=18,
            textColor=colors.HexColor("#3A6EAE"),
            alignment=TA_CENTER,
            spaceAfter=8
        )

        subtitulo_style = ParagraphStyle(
            "subtitulo",
            parent=estilos["Normal"],
            fontSize=10,
            textColor=colors.grey,
            alignment=TA_CENTER
        )

        normal = ParagraphStyle(
            "normal",
            parent=estilos["Normal"],
            fontSize=10,
            leading=14
        )

        bold = ParagraphStyle(
            "bold",
            parent=estilos["Normal"],
            fontSize=10,
            fontName="Helvetica-Bold"
        )

        elementos = []

        fecha = datetime.now().strftime("%d/%m/%Y")

        # =====================================================
        # LOGO
        # =====================================================
        logo = ""

        if empresa.get("logo"):

            base_dir = os.path.dirname(
                os.path.abspath(__file__)
            )

            logo_bd = empresa.get("logo", "").lstrip("/")

            logo_path = os.path.abspath(
                os.path.join(
                    base_dir,
                    "..",
                    "..",
                    logo_bd
                )
            )

            print("Ruta PDF:", logo_path)
            print("Existe:", os.path.exists(logo_path))

        

            # =============================

            if os.path.exists(logo_path):

                logo = Image(

                    logo_path,

                    width=42 * mm,

                    height=42 * mm

                )
        # =====================================================
        # EMPRESA (VERTICAL COMO CLIENTES)
        # =====================================================
        empresa_html = f"""
        <font size="18" color="#1B365D">
        <b>{empresa.get("nombre","EMPRESA")}</b>
        </font>
        <br/><br/>
        <font size="10">
        <b>Dirección:</b> {empresa.get("direccion","")}<br/>
        <b>Teléfono:</b> {empresa.get("telefono","")}<br/>
        <b>Correo:</b> {empresa.get("email","")}
        </font>
        """

        header = Table(
            [[logo, Paragraph(empresa_html, normal)]],
            colWidths=[48 * mm, 120 * mm]
        )

        header.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8)
        ]))

        elementos.append(header)

        # =====================================================
        # LINEA DORADA
        # =====================================================
        linea = Drawing(520, 12)
        linea.add(
            Line(
                0, 5, 520, 5,
                strokeColor=colors.HexColor("#D4AF37"),
                strokeWidth=2
            )
        )

        elementos.append(linea)
        elementos.append(Spacer(1, 12))

        # =====================================================
        # TITULO
        # =====================================================
        elementos.append(
            Paragraph("REPORTE GENERAL DE RESERVAS", titulo_style)
        )

        elementos.append(
            Paragraph(
                "Listado completo de reservas por fechas registrados en el sistema administrativo.",
                subtitulo_style
            )
        )

        elementos.append(Spacer(1, 10))

        # =====================================================
        # CAJA RESUMEN (ESTILO CLIENTES)
        # =====================================================
        resumen = [[
            Paragraph("<b>Fecha de emisión</b>", bold),
            Paragraph(fecha, normal),
            Paragraph("<b>Total de reservas</b>", bold),
            Paragraph(
                str(len(reservas)),
                ParagraphStyle(
                    "numero",
                    parent=normal,
                    fontSize=14,
                    fontName="Helvetica-Bold",
                    textColor=colors.HexColor("#1B365D"),
                    alignment=TA_CENTER
                )
            )
        ]]

        tabla_resumen = Table(
            resumen,
            colWidths=[38*mm, 42*mm, 40*mm, 35*mm]
        )

        tabla_resumen.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#F8F9FA")),
            ("BOX", (0,0), (-1,-1), 0.6, colors.HexColor("#D9D9D9")),
            ("INNERGRID", (0,0), (-1,-1), 0.3, colors.HexColor("#DDDDDD")),
            ("TOPPADDING", (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE")
        ]))

        elementos.append(tabla_resumen)
        elementos.append(Spacer(1, 18))

        # =====================================================
        # TABLA RESERVAS
        # =====================================================
        datos = [[
            "FECHA",
            "HORA",
            "CLIENTE",
            "ESPECIALISTA",
            "SERVICIOS",
        
        ]]

        for r in reservas:
            datos.append([
                Paragraph(str(r["fecha_reserva"]), normal),
                Paragraph(str(r["hora_reserva"]), normal),
                Paragraph(f'{r["nombre_cliente"]} {r["apellido_cliente"]}', normal),
                Paragraph(str(r["nombre_especialista"]), normal),
                Paragraph(str(r["servicios"]), normal),
             
            ])

        tabla = Table(
            datos,
            repeatRows=1,
            colWidths=[25*mm, 20*mm, 38*mm, 38*mm, 45*mm]
        )

        tabla.setStyle(TableStyle([

            # HEADER
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1B365D")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (-1,0), 10),
            ("ALIGN", (0,0), (-1,0), "CENTER"),

            # BODY
            ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
            ("FONTSIZE", (0,1), (-1,-1), 9),
            ("ALIGN", (0,1), (-1,-1), "CENTER"),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),

            # GRID + ESTILO
            ("GRID", (0,0), (-1,-1), 0.3, colors.HexColor("#D7D7D7")),
            ("ROWBACKGROUNDS", (0,1), (-1,-1),
             [colors.white, colors.HexColor("#F3F5F7")]),
        ]))

        elementos.append(tabla)

        # =====================================================
        # GENERAR PDF
        # =====================================================
        doc.build(
            elementos,
            onFirstPage=lambda c, d: (borde(c, d), footer(c, d)),
            onLaterPages=lambda c, d: (borde(c, d), footer(c, d))
        )

        return send_file(
            archivo,
            mimetype="application/pdf",
            download_name="reporte_reservas.pdf",
            as_attachment=False
        )

    if request.method == "POST" and request.form.get("pdfe"):

        especialista = request.form.get("especialista")

        empresa_modelo = EmpresaModelo()
        empresa_data = empresa_modelo.mostrar()
        empresa = empresa_data[0] if empresa_data else {}

        # CONSULTAR RESERVAS DEL ESPECIALISTA
        reservas = modelo.consultarEspecialista(especialista)

        archivo = os.path.join(
            tempfile.gettempdir(),
            "reporte_especialista.pdf"
        )

        doc = SimpleDocTemplate(
            archivo,
            pagesize=LETTER,
            leftMargin=18 * mm,
            rightMargin=18 * mm,
            topMargin=20 * mm,
            bottomMargin=25 * mm
        )

        estilos = getSampleStyleSheet()

        titulo_style = ParagraphStyle(
            "titulo_especialista",
            parent=estilos["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=18,
            textColor=colors.HexColor("#3A6EAE"),
            alignment=TA_CENTER
        )

        normal = ParagraphStyle(
            "normal_especialista",
            parent=estilos["Normal"],
            fontSize=10,
            leading=14
        )

        elementos = []

        fecha = datetime.now().strftime("%d/%m/%Y")

        # ==========================
        # ENCABEZADO EMPRESA
        # ==========================

        logo = ""

        if empresa.get("logo"):

            base_dir = os.path.dirname(
                os.path.abspath(__file__)
            )

            logo_bd = empresa.get("logo", "").lstrip("/")

            logo_path = os.path.abspath(
                os.path.join(
                    base_dir,
                    "..",
                    "..",
                    logo_bd
                )
            )

            print("Ruta PDF:", logo_path)
            print("Existe:", os.path.exists(logo_path))

        

            # =============================

            if os.path.exists(logo_path):

                logo = Image(

                    logo_path,

                    width=42 * mm,

                    height=42 * mm

                )

        empresa_html = f"""
        <font size="18" color="#1B365D">
        <b>{empresa.get("nombre","EMPRESA")}</b>
        </font>
        <br/><br/>

        <font size="10">
        <b>Dirección:</b> {empresa.get("direccion","")}<br/>
        <b>Teléfono:</b> {empresa.get("telefono","")}<br/>
        <b>Correo:</b> {empresa.get("email","")}
        </font>
        """

        header = Table(
            [
                [
                    logo,
                    Paragraph(empresa_html, normal)
                ]
            ],
            colWidths=[48*mm,120*mm]
        )


        header.setStyle(TableStyle([
            ("VALIGN",(0,0),(-1,-1),"MIDDLE")
        ]))


        elementos.append(header)

        elementos.append(Spacer(1,15))


        elementos.append(
            Paragraph(
                "REPORTE DE RESERVAS POR ESPECIALISTA",
                titulo_style
            )
        )

        elementos.append(Spacer(1,10))


        # ==========================
        # TABLA
        # ==========================

        datos = [

            [
                "FECHA",
                "HORA",
                "CLIENTE",
                "ESPECIALISTA",
                "SERVICIOS"
            ]

        ]


        for r in reservas:

            datos.append([

                Paragraph(
                    str(r["fecha_reserva"]),
                    normal
                ),

                Paragraph(
                    str(r["hora_reserva"]),
                    normal
                ),

                Paragraph(
                    f'{r["nombre_cliente"]} {r["apellido_cliente"]}',
                    normal
                ),

                Paragraph(
                    str(r["nombre_especialista"]),
                    normal
                ),

                Paragraph(
                    str(r["servicios"]),
                    normal
                )

            ])



        tabla = Table(
            datos,
            repeatRows=1,
            colWidths=[
                25*mm,
                20*mm,
                38*mm,
                38*mm,
                45*mm
            ]
        )


        tabla.setStyle(TableStyle([

            (
                "BACKGROUND",
                (0,0),
                (-1,0),
                colors.HexColor("#1B365D")
            ),

            (
                "TEXTCOLOR",
                (0,0),
                (-1,0),
                colors.white
            ),

            (
                "FONTNAME",
                (0,0),
                (-1,0),
                "Helvetica-Bold"
            ),

            (
                "ALIGN",
                (0,0),
                (-1,-1),
                "CENTER"
            ),

            (
                "GRID",
                (0,0),
                (-1,-1),
                0.3,
                colors.grey
            ),

            (
                "ROWBACKGROUNDS",
                (0,1),
                (-1,-1),
                [
                    colors.white,
                    colors.HexColor("#F3F5F7")
                ]
            )

        ]))


        elementos.append(tabla)


        # ==========================
        # GENERAR PDF
        # ==========================

        doc.build(
            elementos,
            onFirstPage=lambda c,d: (
                borde(c,d),
                footer(c,d)
            ),
            onLaterPages=lambda c,d: (
                borde(c,d),
                footer(c,d)
            )
        )


        return send_file(
            archivo,
            mimetype="application/pdf",
            download_name="reporte_especialista.pdf",
            as_attachment=False
        )
        
