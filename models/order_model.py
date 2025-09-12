from db import get_db, close_db

def get_orders_for_picker(picker_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT o.order_id, o.order_ref, o.status, o.created_at, oi.item_id, oi.quantity
        FROM orders o
        LEFT JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.assigned_to = %s
    """, (picker_id,))
    results = cursor.fetchall()
    cursor.close()
    close_db(conn)

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

    return list(orders.values())

def start_order(order_id):
    conn = get_db()
    cursor = conn.cursor()
    try:
        query = "UPDATE orders SET status='in_progress' WHERE order_id=%s"
        cursor.execute(query, (order_id,))
        conn.commit()
        return True
    except Exception as e:
        return str(e)
    finally:
        cursor.close()
        close_db(conn)
