from db import get_db, close_db

def add_warehouse_location(location_id, x_coord, y_coord, max_size=None, max_weight=None):
    conn = get_db()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO warehouse_locations (location_id, x_coord, y_coord, max_size, max_weight)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (location_id, x_coord, y_coord, max_size, max_weight))
        conn.commit()
        return True
    except Exception as e:
        return str(e)
    finally:
        cursor.close()
        close_db(conn)
