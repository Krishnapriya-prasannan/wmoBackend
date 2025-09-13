from db import get_db, close_db

def create_order(order_items, created_by):
    try:
        db = get_db()
        cursor = db.cursor()

        # Insert into orders table
        cursor.execute("""
            INSERT INTO orders (order_status, created_by)
            VALUES ('pending', %s)
        """, (created_by,))
        order_id = cursor.lastrowid

        # Insert order items
        for item in order_items:
            cursor.execute("""
                INSERT INTO order_items (order_id, item_id, quantity)
                VALUES (%s, %s, %s)
            """, (order_id, item['item_id'], item['quantity']))

        db.commit()
        return True
    except Exception as e:
        return str(e)
    finally:
        if db:
            close_db(db)


def assign_order_to_picker(order_id, picker_id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            UPDATE orders
            SET assigned_to = %s, order_status = 'in_progress'
            WHERE order_id = %s
        """, (picker_id, order_id))
        db.commit()
        return True
    except Exception as e:
        return str(e)
    finally:
        if db:
            close_db(db)


def get_order_progress():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT o.order_id, o.order_status, u.username AS assigned_picker
            FROM orders o
            LEFT JOIN users u ON o.assigned_to = u.user_id
        """)
        return cursor.fetchall()
    except Exception as e:
        return str(e)
    finally:
        if db:
            close_db(db)
