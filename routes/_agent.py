
#from app.models import Task
#from app.models import AgentTask

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
#from app.extensions import db, login_manager
from models import db, UnitTasks

#from app.models import UnitTask

#agent_bp = Blueprint('agent_bp', __name__, template_folder='templates')
agent_bp = Blueprint(
    "agent",
    __name__,
    url_prefix="/agent",
    template_folder="../templates/agent"
)
@agent_bp.route('/agent', methods=["GET", "POST"])
@login_required
def dashboard():
    if current_user.role != 'agent':
        return render_template('403.html'), 403

    tasks = current_user.tasks
    #.all()  # tâches assignées à l'agent
    grouped = {
        'À faire': [t for t in tasks if t.status == 'À faire'],
        'En cours': [t for t in tasks if t.status == 'En cours'],
        'Terminé': [t for t in tasks if t.status == 'Terminé'],
    }
    return render_template('agent/dashboard.html', agent=current_user, grouped=grouped)

@agent_bp.route('/task/<int:task_id>/move/<string:direction>')
@login_required
def move_task(task_id, direction):
    task = UnitTask.query.get_or_404(task_id)

    if current_user not in task.agents:
        return render_template('403.html'), 403

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
    else:
        return "Bad request", 400

    db.session.commit()
    return redirect(url_for('agent_bp.dashboard'))
