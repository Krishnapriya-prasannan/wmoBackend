from flask import Blueprint, request, jsonify
from models.warehouse_model import add_warehouse_location, get_all_locations
from models.stock_model import upload_stock, assign_stock_to_picker, get_stock_status, get_stockout_alerts
from models.order_model import create_order, assign_order_to_picker, get_order_progress
from models.optimization_model import run_inventory_placement_optimization

manager_bp = Blueprint('manager', __name__, url_prefix='/manager')


# ✅ Upload warehouse layout
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


# ✅ View all warehouse locations
@manager_bp.route('/warehouse_locations', methods=['GET'])
def view_locations():
    result = get_all_locations()
    return jsonify({'locations': result})


# ✅ Upload / Restock stock
@manager_bp.route('/stock', methods=['POST'])
def add_stock():
    data = request.get_json()
    result = upload_stock(
        data.get('item_id'),
        data.get('current_stock'),
        data.get('location_id'),
        data.get('status', 'new'),
        data.get('assigned_to')
    )
    if result is True:
        return jsonify({'message': f"Stock for item {data.get('item_id')} uploaded successfully"})
    else:
        return jsonify({'error': result}), 500


# ✅ Assign stock placement to picker
@manager_bp.route('/stock/assign', methods=['PUT'])
def assign_stock():
    data = request.get_json()
    result = assign_stock_to_picker(
        data.get('stock_id'),
        data.get('picker_id')
    )
    if result is True:
        return jsonify({'message': f"Stock {data.get('stock_id')} assigned to picker {data.get('picker_id')}"})
    else:
        return jsonify({'error': result}), 500


# ✅ View stock status
@manager_bp.route('/stock/status', methods=['GET'])
def stock_status():
    result = get_stock_status()
    return jsonify({'stock_status': result})


# ✅ View stockout alerts
@manager_bp.route('/stock/alerts', methods=['GET'])
def stockout_alerts():
    result = get_stockout_alerts()
    return jsonify({'alerts': result})


# ✅ Create orders
@manager_bp.route('/orders', methods=['POST'])
def create_new_order():
    data = request.get_json()
    result = create_order(
        data.get('order_items'),  # expects list of {item_id, quantity}
        data.get('created_by')
    )
    if result is True:
        return jsonify({'message': 'Order created successfully'})
    else:
        return jsonify({'error': result}), 500


# ✅ Assign pickers to orders
@manager_bp.route('/orders/assign', methods=['PUT'])
def assign_order():
    data = request.get_json()
    result = assign_order_to_picker(
        data.get('order_id'),
        data.get('picker_id')
    )
    if result is True:
        return jsonify({'message': f"Order {data.get('order_id')} assigned to picker {data.get('picker_id')}"})
    else:
        return jsonify({'error': result}), 500


# ✅ View order progress
@manager_bp.route('/orders/progress', methods=['GET'])
def order_progress():
    result = get_order_progress()
    return jsonify({'order_progress': result})


# ✅ Run inventory placement optimization
@manager_bp.route('/optimization/run', methods=['POST'])
def run_optimization():
    result = run_inventory_placement_optimization()
    return jsonify({'recommendations': result})
