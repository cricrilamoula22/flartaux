
from flask_login import login_required, current_user
#from app.models import Unit, UnitTask, AgentTask, User
#from app.models import Unit, Task, User
from flask import Blueprint, render_template, redirect, url_for, request, abort, flash
from app.extensions import db, login_manager

from app.models import UnitTask, Unit, User

unit_bp = Blueprint('unit_bp', __name__, template_folder='templates')


@unit_bp.route('/dashboard')
@login_required
def unit_dashboard():
    if current_user.role != 'manager':
        return render_template('403.html'), 403

    unit = current_user.unit
    tasks = UnitTask.query.filter_by(unit_id=unit.id).all()

    grouped = {
        'À faire': [t for t in tasks if t.status == 'À faire'],
        'En cours': [t for t in tasks if t.status == 'En cours'],
        'Terminé': [t for t in tasks if t.status == 'Terminé'],
    }

    return render_template('unit/dashboard.html', unit=unit, grouped=grouped)

# 🟢 Nouvelle route pour déplacer les tâches dans le dashboard manager
@unit_bp.route('/task/<int:task_id>/move/<string:direction>', methods=['POST', 'GET'])
@login_required
def move_task(task_id, direction):
    if current_user.role != 'manager':
        abort(403)

    task = UnitTask.query.get_or_404(task_id)

    if task.unit_id != current_user.unit_id:
        abort(403)

    if direction == 'forward':
        if task.status == 'À faire':
            task.status = 'En cours'
        elif task.status == 'En cours':
            task.status = 'Terminé'
    elif direction == 'backward':
        if task.status == 'Terminé':
            task.status = 'En cours'
        elif task.status == 'En cours':
            task.status = 'À faire'

    db.session.commit()
    return redirect(url_for('unit_bp.unit_dashboard'))
