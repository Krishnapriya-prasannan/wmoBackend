from db import get_db, close_db

def get_dashboard_stats():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        # Orders summary
        cursor.execute("SELECT status, COUNT(*) AS count FROM orders GROUP BY status")
        orders_summary = cursor.fetchall()
        
        # Stock summary
        cursor.execute("SELECT COUNT(*) AS total_items, SUM(current_stock) AS total_stock FROM stock")
        stock_summary = cursor.fetchone()
        
        # Picker availability
        cursor.execute("SELECT COUNT(*) AS available_pickers FROM users WHERE role='picker' AND status='in_work'")
        picker_summary = cursor.fetchone()
        
        return {
            "orders": orders_summary,
            "stock": stock_summary,
            "pickers": picker_summary
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        if db:
            close_db(db)
