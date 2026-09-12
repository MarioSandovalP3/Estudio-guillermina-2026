from flask import send_from_directory, current_app
from flask import Blueprint

mantenimiento_bp = Blueprint('mantenimiento', __name__)

@admin.route('/admin/descargar-backup/<path:filename>')
def descargar_backup(filename):
    return send_from_directory('static/backups', filename, as_attachment=True)
