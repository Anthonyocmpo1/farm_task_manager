from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Task

task_bp = Blueprint('task_bp', __name__)

@task_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks]), 200

@task_bp.route('/tasks', methods=['POST'])
@jwt_required()
def add_task():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    new_task = Task(
        title=data['title'], description=data.get('description'),
        due_date=data['due_date'], status=data.get('status', 'To-Do'),
        user_id=current_user_id, farm_id=data['farm_id']
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201

@task_bp.route('/tasks/<int:id>', methods=['PUT'])
@jwt_required()
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.due_date = data.get('due_date', task.due_date)
    task.status = data.get('status', task.status)
    db.session.commit()
    return jsonify(task.to_dict()), 200

@task_bp.route('/tasks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'}), 204
