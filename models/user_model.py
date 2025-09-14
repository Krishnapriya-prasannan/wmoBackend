from db import get_db, close_db

# ✅ Create new user (Manager or Picker)
def create_user(username, password, role, status=None):
    conn = get_db()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO users (username, password, role, status)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (username, password, role, status))
        conn.commit()
        return True
    except Exception as e:
        return str(e)
    finally:
        cursor.close()
        close_db(conn)



def authenticate_user(username, password, role):
    db = None
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT user_id, username, password, role FROM users WHERE username=%s AND role=%s", 
                       (username, role))
        user = cursor.fetchone()
        
        if not user:
            return {"success": False, "error": "User not found or role mismatch"}

        if password == user['password']:
            return {
                "success": True,
                "user_id": user['user_id'],
                "role": user['role']
            }
        else:
            return {"success": False, "error": "Invalid password"}

    except Exception as e:
        return {"success": False, "error": str(e)}

    finally:
        if db:
            close_db(db)

# ✅ Update picker status (in_work / rest)
def update_picker_status(user_id, status):
    conn = get_db()
    cursor = conn.cursor()
    try:
        query = "UPDATE users SET status=%s WHERE user_id=%s AND role='picker'"
        cursor.execute(query, (status, user_id))
        conn.commit()
        return True
    except Exception as e:
        return str(e)
    finally:
        cursor.close()
        close_db(conn)

# ✅ Get all pickers and their status (for manager)
def get_all_pickers():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT user_id, username, status FROM users WHERE role='picker'"
        cursor.execute(query)
        pickers = cursor.fetchall()
        return pickers
    finally:
        cursor.close()
        close_db(conn)
