# Estudio Guillermina

Sistema web para la administracion de un estudio de belleza. Permite gestionar clientes, reservas, especialistas, servicios, productos, compras, pagos, promociones, reportes y permisos de usuarios.

## Caracteristicas

- Sitio publico con informacion del estudio, servicios y promociones.
- Inicio de sesion con roles y permisos por modulo.
- Gestion de clientes, usuarios, especialistas y proveedores.
- Registro y seguimiento de reservas.
- Control de productos, categorias, marcas, unidades y stock.
- Registro de compras y pagos.
- Reportes operativos y estadisticos.
- Copias de seguridad y restauracion de la base de datos.
- Registro de movimientos en bitacora.

## Tecnologias

- Python 3
- Flask
- MariaDB/MySQL
- mysql-connector-python
- bcrypt
- python-dotenv
- HTML, CSS y JavaScript
- Bootstrap y librerias frontend incluidas en `static/assets`

## Estructura del proyecto

```text
.
|-- app.py                         # Punto de entrada Flask
|-- admin/
|   |-- config/                    # Configuracion y conexion a BD
|   |-- controlador/               # Controladores de cada modulo
|   |-- modelo/                    # Acceso a datos y logica de persistencia
|   `-- servicios/                 # Servicios auxiliares
|-- db/                            # Scripts SQL adicionales
|-- reportes/                      # Archivos generados por reportes
|-- static/                        # CSS, JavaScript, imagenes y uploads
|-- templates/                     # Plantillas Jinja2
|-- sac hosting.sql                # Esquema y datos de la base sac
`-- seguridad hosting.sql          # Esquema y datos de la base seguridad
```

## Requisitos

- Python 3.10 o superior.
- MariaDB 10.4+ o MySQL compatible.
- Git.
- En Windows, XAMPP es una opcion practica para MariaDB/MySQL.

## Instalacion

1. Clona el repositorio:

   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd Estudio-guillermina-2026
   ```

2. Crea y activa un entorno virtual.

   En Windows PowerShell:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   En Linux o macOS:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Instala las dependencias:

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Crea la base de datos y selecciona cada una antes de importar su dump:

   ```sql
   CREATE DATABASE seguridad CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish2_ci;
   CREATE DATABASE sac CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish2_ci;
   ```

   Importa en este orden, seleccionando la base correspondiente en phpMyAdmin:

   1. `seguridad hosting.sql` dentro de la base `seguridad`.
   2. `sac hosting.sql` dentro de la base `sac`.

   Estos dumps no se incluyen en el repositorio publico porque contienen datos de ejemplo y registros potencialmente sensibles. Conserva copias locales o prepara dumps sanitizados antes de compartirlos.

   `sac` depende de `seguridad.usuario`, por lo que el orden es importante. Si el servidor rechaza las instrucciones `DEFINER`, elimina `DEFINER=\`root\`@\`localhost\`` de los dumps antes de importarlos.

5. Copia `.env.example` como `.env` y ajusta sus valores:

   ```env
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASS=
   DB_NAME=sac
   DB_SECURITY_NAME=seguridad
   DB_SSL_MODE=DISABLED
   SECRET_KEY=replace-with-a-long-random-secret
   SESSION_COOKIE_SECURE=0
   FLASK_DEBUG=0
   ```

   Ajusta los valores a tu instalacion. No publiques este archivo si contiene credenciales reales.

## Ejecucion

Desde la raiz del proyecto y con el entorno virtual activo:

```bash
python app.py
```

Abre en el navegador:

```text
http://127.0.0.1:5000
```

## Configuracion de base de datos

La aplicacion lee `DB_HOST`, `DB_USER`, `DB_PASS` y `DB_NAME` desde `.env`. La base `seguridad` se consulta mediante nombres de tabla calificados, mientras que `DB_NAME` normalmente debe ser `sac`.

## Despliegue en Render

Configura un Web Service conectado al repositorio y usa:

- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn --bind 0.0.0.0:$PORT app:app`

En Environment Variables define `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASS`, `DB_NAME=sac`, `DB_SECURITY_NAME=seguridad`, `DB_SSL_MODE=REQUIRED`, `SECRET_KEY`, `SESSION_COOKIE_SECURE=1` y `FLASK_DEBUG=0`. La base de datos debe estar disponible desde Render, por ejemplo en Aiven, y los esquemas `sac` y `seguridad` deben existir en ese mismo servidor.

Los archivos SQL contienen procedimientos, funciones, vistas, triggers, datos iniciales y relaciones entre tablas. Se recomienda importar los dumps en bases nuevas para evitar conflictos con tablas u objetos existentes.

## Desarrollo

El panel administrativo utiliza rutas con el formato:

```text
/admin?ruta=<modulo>
```

Algunos modulos disponibles son `inicio`, `cliente`, `reserva`, `producto`, `compra`, `pagos`, `usuarios`, `permisos`, `mantenimiento` y los diferentes reportes.

## Seguridad

Antes de publicar o desplegar el sistema:

- Define `SECRET_KEY` mediante una variable de entorno y no uses una clave fija.
- Desactiva `debug` en produccion.
- No publiques `.env`, backups SQL ni credenciales de prueba.
- Protege las descargas y restauraciones de backups con autenticacion y permisos.
- Importa los dumps solo en bases de datos controladas.
- Usa HTTPS y activa cookies seguras en produccion.
- Implementa proteccion CSRF para formularios que modifican datos.
- Cambia todas las contrasenas iniciales antes de usar el sistema.

## Estado

Proyecto academico en desarrollo. Las instrucciones de despliegue deben adaptarse al servidor y a la configuracion de MariaDB/MySQL utilizada.
