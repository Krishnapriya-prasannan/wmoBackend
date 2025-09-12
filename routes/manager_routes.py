from flask import Blueprint, request, jsonify
from models.warehouse_model import add_warehouse_location
from models.stock_model import upload_stock

manager_bp = Blueprint('manager', __name__, url_prefix='/manager')

@manager_bp.route('/warehouse_locations', methods=['POST'])
def create_location():
    data = request.get_json()
    result = add_warehouse_location(
        data.get('location_id'),
        data.get('x_coord'),
        data.get('y_coord'),
        data.get('max_size'),
        data.get('max_weight')
    )
    if result is True:
        return jsonify({'message': f"Location {data.get('location_id')} added successfully"})
    else:
        return jsonify({'error': result}), 500

@manager_bp.route('/stock', methods=['POST'])
def add_stock():
    data = request.get_json()
    result = upload_stock(
        data.get('item_id'),
        data.get('current_stock'),
        data.get('location_id'),
        data.get('status', 'new')
    )
    if result is True:
        return jsonify({'message': f"Stock for item {data.get('item_id')} uploaded successfully"})
    else:
        return jsonify({'error': result}), 500
