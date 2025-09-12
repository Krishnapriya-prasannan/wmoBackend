from flask import Blueprint, request, jsonify
from models.order_model import get_orders_for_picker, start_order

picker_bp = Blueprint('picker', __name__, url_prefix='/picker')

@picker_bp.route('/orders/<int:picker_id>', methods=['GET'])
def view_assigned_orders(picker_id):
    try:
        orders = get_orders_for_picker(picker_id)
        return jsonify(orders)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@picker_bp.route('/orders/<int:order_id>/start', methods=['PUT'])
def start_assigned_order(order_id):
    result = start_order(order_id)
    if result is True:
        return jsonify({'message': f'Order {order_id} started'})
    else:
        return jsonify({'error': result}), 500
