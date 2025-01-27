from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Farm

farm_bp = Blueprint('farm_bp', __name__)

@farm_bp.route('/farms', methods=['GET'])
@jwt_required()
def get_farms():
    farms = Farm.query.all()
    return jsonify([farm.to_dict() for farm in farms]), 200

@farm_bp.route('/farms', methods=['POST'])
@jwt_required()
def add_farm():
    data = request.get_json()
    new_farm = Farm(name=data['name'], location=data.get('location'), size=data.get('size'))
    db.session.add(new_farm)
    db.session.commit()
    return jsonify(new_farm.to_dict()), 201

@farm_bp.route('/farms/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_farm(id):
    farm = Farm.query.get_or_404(id)
    db.session.delete(farm)
    db.session.commit()
    return jsonify({'message': 'Farm deleted successfully'}), 204
