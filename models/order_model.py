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


# ✅ Get all pending orders
def get_available_orders():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM orders WHERE status = 'pending'")
        orders = cursor.fetchall()
        return orders
    except Exception as e:
        return str(e)
    finally:
        if db:
            close_db(db)

# ✅ Assign order to picker (take order)
def assign_order_to_picker(order_id, picker_id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            UPDATE orders
            SET assigned_to = %s, status = 'in_progress'
            WHERE order_id = %s AND status = 'pending'
        """, (picker_id, order_id))
        db.commit()
        return cursor.rowcount > 0   # True if updated
    except Exception as e:
        db.rollback()
        return str(e)
    finally:
        if db:
            close_db(db)


# ✅ Complete order
def complete_order(order_id, picker_id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            UPDATE orders
            SET status = 'completed'
            WHERE order_id = %s AND assigned_to = %s AND status = 'in_progress'
        """, (order_id, picker_id))
        db.commit()
        return cursor.rowcount > 0
    except Exception as e:
        db.rollback()
        return str(e)
    finally:
        if db:
            close_db(db)
