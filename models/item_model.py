from db import get_db, close_db

# ✅ Add a new item
def create_item(item_id, category, subcategory, size, color, material, unit_price, shelf_life, dimensions):
    """
    dimensions: a dict, e.g., {"height": 10, "width": 20, "depth": 30}
    """
    try:
        db = get_db()
        cursor = db.cursor()
        query = """
            INSERT INTO items (item_id, category, subcategory, size, color, material, unit_price, shelf_life, dimensions)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            item_id,
            category,
            subcategory,
            size,
            color,
            material,
            unit_price,
            shelf_life,
            str(dimensions)  # store as JSON string
        ))
        db.commit()
        return True
    except Exception as e:
        return str(e)
    finally:
        if db:
            close_db(db)

# ✅ Optional: Fetch all items
def get_all_items():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM items")
        return cursor.fetchall()
    except Exception as e:
        return str(e)
    finally:
        if db:
            close_db(db)
# ✅ Optional: Fetch item by ID
def get_item_by_id(item_id):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM items WHERE item_id = %s", (item_id,))
        return cursor.fetchone()
    except Exception as e:
        return str(e)
    finally:
        if db:
            close_db(db)