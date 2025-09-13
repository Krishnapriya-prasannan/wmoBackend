from db import get_db, close_db

import uuid  # to generate unique order_ref

def create_order(order_items):
    try:
        db = get_db()
        cursor = db.cursor()

        # Generate a unique order reference (can be UUID or custom format)
        order_ref = str(uuid.uuid4())[:8]  # shorter, like "a1b2c3d4"

        # Insert into orders table (status = 'pending', assigned_to = NULL)
        cursor.execute("""
            INSERT INTO orders (order_ref, status, assigned_to)
            VALUES (%s, 'pending', NULL)
        """, (order_ref,))
        order_id = cursor.lastrowid

        # Insert order items
        for item in order_items:
            cursor.execute("""
                INSERT INTO order_items (order_id, item_id, quantity)
                VALUES (%s, %s, %s)
            """, (order_id, item['item_id'], item['quantity']))

        db.commit()
        return {"success": True, "order_id": order_id, "order_ref": order_ref}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        if db:
            close_db(db)



def assign_order_to_picker(order_id, picker_id):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        # Check if order exists
        cursor.execute("SELECT status FROM orders WHERE order_id = %s", (order_id,))
        order = cursor.fetchone()
        if not order:
            return f"Order {order_id} does not exist"

        # Check if picker exists and has role 'picker'
        cursor.execute("SELECT user_id FROM users WHERE user_id = %s AND role = 'picker'", (picker_id,))
        picker = cursor.fetchone()
        if not picker:
            return f"Picker with ID {picker_id} does not exist or is not a picker"

        # Update order assignment
        cursor.execute("""
            UPDATE orders
            SET assigned_to = %s, status = 'in_progress'
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
            SELECT o.order_id, o.status, u.username AS assigned_picker
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
