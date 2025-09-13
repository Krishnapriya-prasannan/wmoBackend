from db import get_db, close_db

def upload_stock(item_id, current_stock, location_id, status='new', assigned_to=None):
    try:
        db = get_db()
        cursor = db.cursor()

        query = """
            INSERT INTO stock (item_id, current_stock, location_id, status, assigned_to)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            item_id,
            current_stock,
            location_id,
            status,
            assigned_to
        ))

        db.commit()
        return True
    except Exception as e:
        return str(e)
    finally:
        if db:
            close_db(db)


def assign_stock_to_picker(stock_id, picker_id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            UPDATE stock
            SET assigned_to = %s, stock_status = 'in_placement'
            WHERE stock_id = %s
        """, (picker_id, stock_id))
        db.commit()
        return True
    except Exception as e:
        return str(e)
    finally:
        if db:
            close_db(db)


def get_stock_status():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT s.stock_id, i.item_name, s.current_stock, s.stock_status, l.location_id
            FROM stock s
            JOIN items i ON s.stock_item_id = i.item_id
            LEFT JOIN warehouse_locations l ON s.stock_location_id = l.location_id
        """)
        return cursor.fetchall()
    except Exception as e:
        return str(e)
    finally:
        if db:
            close_db(db)


def get_stockout_alerts():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT i.item_id, i.item_name, SUM(s.current_stock) AS total_stock
            FROM items i
            LEFT JOIN stock s ON i.item_id = s.stock_item_id
            GROUP BY i.item_id, i.item_name
            HAVING total_stock < 10   -- threshold for low stock
        """)
        return cursor.fetchall()
    except Exception as e:
        return str(e)
    finally:
        if db:
            close_db(db)
