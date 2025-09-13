from db import get_db, close_db

def add_warehouse_location(location_id, x_coord, y_coord, max_size, max_weight):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO warehouse_locations (location_id, x_coord, y_coord, max_size, max_weight)
            VALUES (%s, %s, %s, %s, %s)
        """, (location_id, x_coord, y_coord, max_size, max_weight))
        db.commit()
        return True
    except Exception as e:
        return str(e)
    finally:
        if db:
            close_db(db)
def get_all_locations():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM warehouse_locations")
        return cursor.fetchall()
    except Exception as e:
        return str(e)
    finally:
        if db:  
            close_db(db)
