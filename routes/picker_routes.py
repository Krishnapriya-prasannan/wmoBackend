from flask import Blueprint, request, jsonify
from models.order_model import get_available_orders, assign_order_to_picker, complete_order
from models.stock_model import get_available_stocks, assign_stock_to_picker, complete_stock_placement


picker_bp = Blueprint('picker', __name__, url_prefix='/picker')
stock_bp = Blueprint('stock', __name__, url_prefix='/stock')



# ✅ Get all available (pending) orders
@picker_bp.route('/orders/available', methods=['GET'])
def available_orders():
    result = get_available_orders()
    if isinstance(result, str):  # error case
        return jsonify({'error': result}), 500
    return jsonify({'orders': result})


# ✅ Picker takes an order
@picker_bp.route('/orders/<int:order_id>/take', methods=['PUT'])
def take_order(order_id):
    data = request.get_json()
    picker_id = data.get('picker_id')

    if not picker_id:
        return jsonify({'error': 'picker_id is required'}), 400

    result = assign_order_to_picker(order_id, picker_id)
    if result is True:
        return jsonify({'message': f"Order {order_id} assigned to picker {picker_id}"}), 200
    elif result is False:
        return jsonify({'error': f"Order {order_id} is not pending or already taken"}), 400
    else:
        return jsonify({'error': result}), 500


# ✅ Picker completes an order
@picker_bp.route('/orders/<int:order_id>/complete', methods=['PUT'])
def complete_order_route(order_id):
    data = request.get_json()
    picker_id = data.get('picker_id')

    if not picker_id:
        return jsonify({'error': 'picker_id is required'}), 400

    result = complete_order(order_id, picker_id)
    if result is True:
        return jsonify({'message': f"Order {order_id} completed by picker {picker_id}"}), 200
    elif result is False:
        return jsonify({'error': f"Order {order_id} not found or not assigned to picker {picker_id}"}), 400
    else:
        return jsonify({'error': result}), 500


# ✅ Get all available (new) stocks
@stock_bp.route('/stocks/available', methods=['GET'])
def available_stocks():
    result = get_available_stocks()
    if isinstance(result, str):  # error case
        return jsonify({'error': result}), 500
    return jsonify({'stocks': result})


# ✅ Picker takes a stock (moves from 'new' → 'in_placement')
@stock_bp.route('/stocks/<int:stock_id>/take', methods=['PUT'])
def take_stock(stock_id):
    data = request.get_json()
    picker_id = data.get('picker_id')

    if not picker_id:
        return jsonify({'error': 'picker_id is required'}), 400

    result = assign_stock_to_picker(stock_id, picker_id)
    if result is True:
        return jsonify({'message': f"Stock {stock_id} assigned to picker {picker_id}"}), 200
    elif result is False:
        return jsonify({'error': f"Stock {stock_id} is not new or already taken"}), 400
    else:
        return jsonify({'error': result}), 500


# ✅ Picker completes a stock placement (moves from 'in_placement' → 'placed')
@stock_bp.route('/stocks/<int:stock_id>/complete', methods=['PUT'])
def complete_stock_route(stock_id):
    data = request.get_json()
    picker_id = data.get('picker_id')

    if not picker_id:
        return jsonify({'error': 'picker_id is required'}), 400

    result = complete_stock_placement(stock_id, picker_id)
    if result is True:
        return jsonify({'message': f"Stock {stock_id} placed by picker {picker_id}"}), 200
    elif result is False:
        return jsonify({'error': f"Stock {stock_id} not found or not assigned to picker {picker_id}"}), 400
    else:
        return jsonify({'error': result}), 500