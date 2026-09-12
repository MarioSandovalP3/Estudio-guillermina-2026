from flask import request, send_file
from admin.modelo.clientes import ClientesModelo
from admin.modelo.empresa import EmpresaModelo

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
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)

from reportlab.lib.enums import (
    TA_CENTER,
    TA_LEFT,
    TA_RIGHT
)

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

    canvas.setStrokeColor(colors.HexColor("#D4AF37"))
    canvas.setLineWidth(0.8)

    canvas.line(
        15 * mm,
        18 * mm,
        195 * mm,
        18 * mm
    )

    canvas.setFont(
        "Helvetica",
        8
    )

    canvas.setFillColor(colors.HexColor("#777777"))

    canvas.drawString(
        18 * mm,
        11 * mm,
        "Sistema Administrativo • Peluquería"
    )

    canvas.drawRightString(
        195 * mm,
        11 * mm,
        datetime.now().strftime("%d/%m/%Y %H:%M")
    )

    canvas.drawCentredString(
        105 * mm,
        6 * mm,
        f"Página {doc.page}"
    )

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

    modelo = ClientesModelo()

    if request.method == "POST" and request.form.get("pdf"):

        empresa_modelo = EmpresaModelo()

        empresa_data = empresa_modelo.mostrar()

        empresa = empresa_data[0] if empresa_data else {}

        clientes = modelo.consultar()

        archivo = os.path.join(
            tempfile.gettempdir(),
            "reporte_clientes.pdf"
        )

        doc = SimpleDocTemplate(
            archivo,
            pagesize=LETTER,
            leftMargin=18 * mm,
            rightMargin=18 * mm,
            topMargin=20 * mm,
            bottomMargin=25 * mm
        )

        doc.title = "Reporte General de Clientes"

        estilos = getSampleStyleSheet()

        # =====================================================
        # ESTILOS
        # =====================================================

        empresa_style = ParagraphStyle(

            "empresa",

            parent=estilos["Heading1"],

            fontName="Helvetica-Bold",

            fontSize=23,

            textColor=colors.HexColor("#1B365D"),

            leading=24,

            alignment=TA_LEFT

        )

        titulo_style = ParagraphStyle(

            "titulo",

            parent=estilos["Heading1"],

            fontName="Helvetica-Bold",

            fontSize=18,

            textColor=colors.HexColor("#B8860B"),

            alignment=TA_CENTER,

            spaceAfter=4

        )

        subtitulo_style = ParagraphStyle(

            "subtitulo",

            parent=estilos["Normal"],

            fontName="Helvetica",

            fontSize=10,

            textColor=colors.grey,

            alignment=TA_CENTER

        )

        normal = ParagraphStyle(

            "normal",

            parent=estilos["Normal"],

            fontName="Helvetica",

            fontSize=10,

            leading=15

        )

        bold = ParagraphStyle(

            "bold",

            parent=estilos["Normal"],

            fontName="Helvetica-Bold",

            fontSize=10

        )

        info = ParagraphStyle(

            "info",

            parent=estilos["Normal"],

            fontName="Helvetica",

            fontSize=9,

            textColor=colors.HexColor("#444444"),

            leading=14

        )

        elementos = []

        fecha = datetime.now().strftime("%d/%m/%Y")

        # =====================================================
        # LOGO
        # =====================================================

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
        # DATOS EMPRESA
        # =====================================================

        empresa_html = f"""

        <font size="18" color="#1B365D">

        <b>{empresa.get("nombre","EMPRESA")}</b>

        </font>

        <br/><br/>

        <font size="10">

        <b>Dirección:</b> {empresa.get("direccion","")}

        <br/>

        <b>Teléfono:</b> {empresa.get("telefono","")}

        <br/>

        <b>Correo:</b> {empresa.get("email","")}

        </font>

        """

        datos_empresa = Paragraph(
            empresa_html,
            normal
        )

        header = Table(

            [

                [

                    logo,

                    datos_empresa

                ]

            ],

            colWidths=[48 * mm, 120 * mm]

        )

        header.setStyle(TableStyle([

            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

            ('BOTTOMPADDING', (0, 0), (-1, -1), 8)

        ]))

        elementos.append(header)

        # =====================================================
        # LINEA DORADA
        # =====================================================

        linea = Drawing(
            520,
            12
        )

        linea.add(

            Line(

                0,

                5,

                520,

                5,

                strokeColor=colors.HexColor("#D4AF37"),

                strokeWidth=2

            )

        )

        elementos.append(linea)

        elementos.append(
            Spacer(1, 12)
        )
        # =====================================================
        # TITULO DEL REPORTE
        # =====================================================

        elementos.append(
            Paragraph(
                "REPORTE GENERAL DE CLIENTES",
                titulo_style
            )
        )

        elementos.append(
            Paragraph(
                "Listado completo de clientes registrados en el sistema administrativo.",
                subtitulo_style
            )
        )

        elementos.append(
            Spacer(1, 10)
        )

        # =====================================================
        # CAJA RESUMEN
        # =====================================================

        resumen = [

            [

                Paragraph("<b>Fecha de emisión</b>", bold),

                Paragraph(fecha, normal),

                Paragraph("<b>Total de clientes</b>", bold),

                Paragraph(
                    str(len(clientes)),
                    ParagraphStyle(
                        "numero",
                        parent=normal,
                        alignment=TA_CENTER,
                        textColor=colors.HexColor("#1B365D"),
                        fontSize=14,
                        fontName="Helvetica-Bold"
                    )
                )

            ]

        ]

        tabla_resumen = Table(

            resumen,

            colWidths=[
                38 * mm,
                42 * mm,
                40 * mm,
                35 * mm
            ]

        )

        tabla_resumen.setStyle(TableStyle([

            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8F9FA")),

            ('BOX', (0,0), (-1,-1), 0.6, colors.HexColor("#D9D9D9")),

            ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor("#DDDDDD")),

            ('TOPPADDING', (0,0), (-1,-1), 8),

            ('BOTTOMPADDING', (0,0), (-1,-1), 8),

            ('VALIGN', (0,0), (-1,-1), 'MIDDLE')

        ]))

        elementos.append(tabla_resumen)

        elementos.append(
            Spacer(1, 18)
        )

        # =====================================================
        # TABLA
        # =====================================================

        datos = [[

            "CÉDULA",

            "NOMBRE",

            "APELLIDO",

            "TELÉFONO",

            "DIRECCIÓN",

            "CORREO"

        ]]

        for cliente in clientes:

            datos.append([

                Paragraph(
                    cliente["cedula"],
                    normal
                ),

                Paragraph(
                    cliente["nombre_usuario"],
                    normal
                ),

                Paragraph(
                    cliente["apellido_usuario"],
                    normal
                ),

                Paragraph(
                    cliente["telefono"] or "",
                    normal
                ),

                Paragraph(
                    cliente["direccion"] or "No disponible",
                    normal
                ),

                Paragraph(
                    cliente["correo"] or "No disponible",
                    normal
                )

            ])

        tabla = Table(

            datos,

            repeatRows=1,

            colWidths=[

                25 * mm,

                25 * mm,

                25 * mm,

                25 * mm,

                42 * mm,

                45 * mm

            ]

        )

        tabla.setStyle(TableStyle([

            # Encabezado

            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1B365D")),

            ('TEXTCOLOR', (0,0), (-1,0), colors.white),

            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),

            ('FONTSIZE', (0,0), (-1,0), 10),

            ('ALIGN', (0,0), (-1,0), 'CENTER'),

            ('BOTTOMPADDING', (0,0), (-1,0), 10),

            ('TOPPADDING', (0,0), (-1,0), 10),

            # Cuerpo

            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),

            ('FONTSIZE', (0,1), (-1,-1), 9),

            ('ALIGN', (0,1), (-1,-1), 'CENTER'),

            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),

            ('TOPPADDING', (0,1), (-1,-1), 7),

            ('BOTTOMPADDING', (0,1), (-1,-1), 7),

            # Colores alternos

            ('ROWBACKGROUNDS',

                (0,1),

                (-1,-1),

                [

                    colors.white,

                    colors.HexColor("#F3F5F7")

                ]

            ),

            # Bordes

            ('GRID',

                (0,0),

                (-1,-1),

                0.25,

                colors.HexColor("#D7D7D7")

            ),

            ('LINEBELOW',

                (0,0),

                (-1,0),

                1,

                colors.HexColor("#D4AF37")

            ),

            ('BOX',

                (0,0),

                (-1,-1),

                0.5,

                colors.HexColor("#BEBEBE")

            )

        ]))

        elementos.append(
            KeepTogether(tabla)
        )

        elementos.append(
            Spacer(1, 18)
        )

   
      


        # =====================================================
        # GENERAR PDF
        # =====================================================

        doc.build(

            elementos,

            onFirstPage=lambda canvas, documento: (
                borde(canvas, documento),
                footer(canvas, documento)
            ),

            onLaterPages=lambda canvas, documento: (
                borde(canvas, documento),
                footer(canvas, documento)
            )

        )

        # =====================================================
        # ENVIAR ARCHIVO
        # =====================================================

        return send_file(

            archivo,

            mimetype="application/pdf",

            download_name="reporte_clientes.pdf",

            as_attachment=False

        )

    # =====================================================
    # CONSULTA NORMAL
    # =====================================================

    registro = modelo.consultar()

    return {

        "registro": registro

    }        
