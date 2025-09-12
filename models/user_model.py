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

# ✅ Fetch user by username (for login)
def get_user_by_username(username):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM users WHERE username=%s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        return user
    finally:
        cursor.close()
        close_db(conn)

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
