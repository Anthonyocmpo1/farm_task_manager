from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Worker

worker_bp = Blueprint('worker_bp', __name__)

@worker_bp.route('/workers', methods=['GET'])
@jwt_required()
def get_workers():
    workers = Worker.query.all()
    return jsonify([worker.to_dict() for worker in workers]), 200

@worker_bp.route('/workers', methods=['POST'])
@jwt_required()
def add_worker():
    data = request.get_json()
    new_worker = Worker(name=data['name'], role=data.get('role'))
    db.session.add(new_worker)
    db.session.commit()
    return jsonify(new_worker.to_dict()), 201

@worker_bp.route('/workers/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_worker(id):
    worker = Worker.query.get_or_404(id)
    db.session.delete(worker)
    db.session.commit()
    return jsonify({'message': 'Worker deleted successfully'}), 204
