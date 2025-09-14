# user_routes.py
from flask import Blueprint, request, jsonify
from models.user_model import authenticate_user
from models.dashboard_model import get_dashboard_stats
from models.demand_model import get_demand_history

user_bp = Blueprint('user', __name__)

# -------------------------------
# 1️⃣ User Login / Auth
# -------------------------------
@user_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('login_type')  # manager/picker

    result = authenticate_user(username, password, role)

    if result.get("success"):
        return jsonify({
            "success": True,           # <-- add this
            "message": "Login successful",
            "user_id": result.get("user_id"),
            "role": result.get("role")
        })
    else:
        return jsonify({
            "success": False,          # <-- add this
            "error": result.get("error")
        }), 401


# -------------------------------
# 2️⃣ Get Dashboard Stats
# -------------------------------
@user_bp.route('/dashboard', methods=['GET'])
def dashboard():
    result = get_dashboard_stats()
    return jsonify(result)


# -------------------------------
# 3️⃣ View Demand History
# -------------------------------
@user_bp.route('/demand-history', methods=['GET'])
def demand_history():
    # Optional query parameters: ?item_id=ITEM001&start_date=2025-01-01&end_date=2025-09-01
    item_id = request.args.get('item_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    result = get_demand_history(item_id=item_id, start_date=start_date, end_date=end_date)
    return jsonify(result)
