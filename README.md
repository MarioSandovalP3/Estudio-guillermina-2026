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

- Python 3.12 recomendado.
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

4. Configura las bases de datos.

   La aplicacion usa dos esquemas en el mismo servidor: `seguridad` y `sac`. El esquema `sac` depende de `seguridad.usuario`.

   ```sql
   CREATE DATABASE seguridad CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish2_ci;
   CREATE DATABASE sac CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish2_ci;
   ```

   Importa los dumps en este orden:

   1. `seguridad hosting.sql` dentro de la base `seguridad`.
   2. `sac hosting.sql` dentro de la base `sac`.

   - Primero `seguridad hosting.sql` dentro de `seguridad`.
   - Despues `sac hosting.sql` dentro de `sac`.

   Los dumps no se incluyen en el repositorio publico porque contienen datos de ejemplo y registros potencialmente sensibles. Conserva copias locales o prepara dumps sanitizados antes de compartirlos.

   `sac` depende de `seguridad.usuario`, por lo que el orden es obligatorio. Los dumps preparados para este proyecto no usan `root@localhost` y utilizan `//` como delimitador para procedimientos y triggers.

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

## Acceso inicial

Para una instalacion de demostracion que use los datos incluidos en el dump de seguridad:

```text
Usuario: 31117996
Contraseña inicial: admin123
Rol: administrador
```

Esta credencial solo sirve para el primer acceso. Cambiala inmediatamente en cualquier entorno publicado y no la reutilices en produccion.

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

La aplicacion lee la conexion desde variables de entorno:

| Variable | Valor local | Valor Aiven/Render |
| --- | --- | --- |
| `DB_HOST` | `localhost` | Host de Aiven |
| `DB_PORT` | `3306` | Puerto de Aiven |
| `DB_USER` | `root` | `avnadmin` u otro usuario |
| `DB_PASS` | Clave local | Variable secreta |
| `DB_NAME` | `sac` | `sac` |
| `DB_SECURITY_NAME` | `seguridad` | `seguridad` |
| `DB_SSL_MODE` | `DISABLED` | `REQUIRED` |

Aunque `DB_SECURITY_NAME` documenta el nombre del segundo esquema, el codigo usa referencias SQL explicitas como `seguridad.usuario`. Ambos esquemas deben existir en la misma instancia MySQL/MariaDB.

## Crear base en Aiven

1. Crea un servicio **MySQL** en [Aiven](https://aiven.io/).
2. Espera a que el servicio este disponible.
3. Copia del panel de Aiven estos datos: host, puerto, usuario, contraseña, nombre de base y modo SSL.
4. Usa una herramienta compatible, como HeidiSQL, MySQL Workbench o el cliente `mysql`.
5. Crea los dos esquemas si el usuario tiene permisos:

    ```sql
    CREATE DATABASE IF NOT EXISTS `seguridad`
       CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish2_ci;
    CREATE DATABASE IF NOT EXISTS `sac`
       CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish2_ci;
    ```

6. Importa `seguridad hosting.sql` y despues `sac hosting.sql`.
7. Verifica que existan las tablas:

    ```sql
    SHOW TABLES FROM seguridad;
    SHOW TABLES FROM sac;
    SELECT cedula FROM seguridad.usuario;
    ```

En Aiven el SSL suele ser obligatorio. Usa `DB_SSL_MODE=REQUIRED`. Si el proveedor entrega un certificado CA y exige validacion estricta, configura tambien el certificado segun la documentacion de Aiven.

### Importacion con cliente mysql

Con las credenciales configuradas y SSL requerido, el procedimiento general es:

```bash
mysql --ssl-mode=REQUIRED -h HOST_AIVEN -P PUERTO -u USUARIO -p seguridad < "seguridad hosting.sql"
mysql --ssl-mode=REQUIRED -h HOST_AIVEN -P PUERTO -u USUARIO -p sac < "sac hosting.sql"
```

El nombre `sac` del segundo comando debe coincidir con `DB_NAME`. No uses `root@localhost` en Aiven.

## Despliegue en Render

### Opcion manual

1. En Render selecciona **New > Web Service** y conecta el repositorio.
2. Usa Python como entorno.
3. Configura:

- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn --bind 0.0.0.0:$PORT app:app`

No uses `gunicorn your_application.wsgi`: ese nombre es un ejemplo. El modulo real del proyecto es `app:app`, porque el archivo es `app.py` y la instancia Flask se llama `app`.

4. En **Environment > Environment Variables** agrega:

   ```text
   DB_HOST=host-de-Aiven
   DB_PORT=puerto-de-Aiven
   DB_USER=avnadmin
   DB_PASS=contraseña-de-Aiven
   DB_NAME=sac
   DB_SECURITY_NAME=seguridad
   DB_SSL_MODE=REQUIRED
   SECRET_KEY=clave-larga-aleatoria
   SESSION_COOKIE_SECURE=1
   FLASK_DEBUG=0
   ```

5. Guarda los cambios y ejecuta **Manual Deploy > Deploy latest commit**.

### Opcion Blueprint

El repositorio incluye `render.yaml`. Puedes crear el servicio desde **New > Blueprint** para que Render lea automaticamente el Build Command, el Start Command y las variables no secretas. Completa manualmente `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASS` y `SECRET_KEY`.

La base de datos debe ser accesible desde Render. Aiven y Render son servicios separados; comprueba que el servicio Aiven este activo y que sus reglas de acceso permitan la conexion.

### Verificacion del despliegue

Cuando Render indique **Live**, abre la URL publica y prueba:

```text
/
/login
```

Si la aplicacion inicia pero no carga datos, revisa primero las variables `DB_HOST`, `DB_PORT`, `DB_PASS`, `DB_NAME` y `DB_SSL_MODE`. Si no inicia y aparece `No module named 'your_application'`, corrige el Start Command a `gunicorn --bind 0.0.0.0:$PORT app:app`.

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
