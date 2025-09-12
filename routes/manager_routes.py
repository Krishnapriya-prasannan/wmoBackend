from flask import Blueprint, request, jsonify
from db import get_db, close_db

manager_bp = Blueprint('manager', __name__, url_prefix='/manager')

# -------------------------------
# Add new warehouse location
# -------------------------------
@manager_bp.route('/warehouse_locations', methods=['POST'])
def add_warehouse_location():
    data = request.get_json()
    location_id = data.get('location_id')
    x_coord = data.get('x_coord')
    y_coord = data.get('y_coord')
    max_size = data.get('max_size')
    max_weight = data.get('max_weight')

    if not location_id or x_coord is None or y_coord is None:
        return jsonify({'error': 'Missing required fields'}), 400

    conn = get_db()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO warehouse_locations (location_id, x_coord, y_coord, max_size, max_weight)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (location_id, x_coord, y_coord, max_size, max_weight))
        conn.commit()
        return jsonify({'message': f'Location {location_id} added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        close_db(conn)

# -------------------------------
# Upload new stock
# -------------------------------
@manager_bp.route('/stock', methods=['POST'])
def upload_stock():
    data = request.get_json()
    item_id = data.get('item_id')
    current_stock = data.get('current_stock')
    location_id = data.get('location_id')
    status = data.get('status', 'new')

    if not item_id or current_stock is None:
        return jsonify({'error': 'Missing required fields'}), 400

    conn = get_db()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO stock (item_id, current_stock, location_id, status)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (item_id, current_stock, location_id, status))
        conn.commit()
        return jsonify({'message': f'Stock for item {item_id} uploaded successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        close_db(conn)
