from db import get_db, close_db

def get_demand_history(item_id=None, start_date=None, end_date=None):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        query = "SELECT item_id, date, sales, demand_frequency FROM demand_history WHERE 1=1"
        params = []

        if item_id:
            query += " AND item_id=%s"
            params.append(item_id)
        if start_date:
            query += " AND date >= %s"
            params.append(start_date)
        if end_date:
            query += " AND date <= %s"
            params.append(end_date)
        
        query += " ORDER BY date DESC"
        cursor.execute(query, tuple(params))
        data = cursor.fetchall()
        return {"demand_history": data}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if db:
            close_db(db)
