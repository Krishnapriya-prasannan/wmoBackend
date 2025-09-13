from db import get_db, close_db

def run_inventory_placement_optimization():
    """
    Simple version: recommend first available location for each stock with 'new' status.
    Later you can replace this with AI/ML optimization logic.
    """
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        # Get unplaced stock
        cursor.execute("""
            SELECT s.stock_id, i.item_name
            FROM stock s
            JOIN items i ON s.stock_item_id = i.item_id
            WHERE s.stock_status = 'new'
        """)
        new_stock = cursor.fetchall()

        # Get available locations
        cursor.execute("SELECT location_id FROM warehouse_locations")
        locations = cursor.fetchall()
        loc_ids = [l['location_id'] for l in locations]

        recommendations = []
        for idx, stock in enumerate(new_stock):
            recommended_loc = loc_ids[idx % len(loc_ids)] if loc_ids else None
            recommendations.append({
                "stock_id": stock['stock_id'],
                "item_name": stock['item_name'],
                "recommended_location": recommended_loc
            })

        return recommendations
    except Exception as e:
        return str(e)
    finally:
        if db:
            close_db(db)
