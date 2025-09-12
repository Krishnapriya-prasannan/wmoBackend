from flask import Blueprint, request, jsonify
from db import get_db, close_db

picker_bp = Blueprint('picker', __name__, url_prefix='/picker')

# -------------------------------
# View orders assigned to this picker
# -------------------------------
@picker_bp.route('/orders/<int:picker_id>', methods=['GET'])
def view_assigned_orders(picker_id):
    """
    Fetch all orders assigned to a specific picker.
    """
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
        SELECT o.order_id, o.order_ref, o.status, o.created_at, oi.item_id, oi.quantity
        FROM orders o
        LEFT JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.assigned_to = %s
        """
        cursor.execute(query, (picker_id,))
        results = cursor.fetchall()

        # Format orders by order_id
        orders = {}
        for row in results:
            oid = row['order_id']
            if oid not in orders:
                orders[oid] = {
                    'order_id': oid,
                    'order_ref': row['order_ref'],
                    'status': row['status'],
                    'created_at': str(row['created_at']),
                    'items': []
                }
            if row['item_id']:
                orders[oid]['items'].append({'item_id': row['item_id'], 'quantity': row['quantity']})

        return jsonify(list(orders.values()))
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        close_db(conn)

# -------------------------------
# Start an assigned order
# -------------------------------
@picker_bp.route('/orders/<int:order_id>/start', methods=['PUT'])
def start_order(order_id):
    """
    Mark an assigned order as in_progress.
    """
    conn = get_db()
    cursor = conn.cursor()
    try:
        query = "UPDATE orders SET status = 'in_progress' WHERE order_id = %s"
        cursor.execute(query, (order_id,))
        conn.commit()
        return jsonify({'message': f'Order {order_id} started'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        close_db(conn)

# Add other picker APIs here
