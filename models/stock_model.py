from db import get_db, close_db

def upload_stock(item_id, current_stock, location_id, status='new'):
    conn = get_db()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO stock (item_id, current_stock, location_id, status)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (item_id, current_stock, location_id, status))
        conn.commit()
        return True
    except Exception as e:
        return str(e)
    finally:
        cursor.close()
        close_db(conn)
