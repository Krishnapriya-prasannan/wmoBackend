from flask import Blueprint, request, jsonify
import requests
from db import get_db
import json

route_bp = Blueprint("route", __name__)

@route_bp.route("/run_route_optimization", methods=["POST"])
def run_route_optimization():
    data = request.get_json()

    # ✅ Validate input
    if "pick_list" not in data or not data["pick_list"]:
        return jsonify({"error": "pick_list is required"}), 400

    try:
        # ✅ Call the microservice
        response = requests.post("http://127.0.0.1:6001/optimize-route", json=data)
        result = response.json()

        if "error" in result:
            return jsonify(result), 400

        optimized_path = result.get("optimized_path", [])
        total_distance = result.get("total_distance", 0)

        # ✅ Insert into DB (routes table)
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            INSERT INTO routes (task_type, reference_id, start_location, end_location, route, total_distance)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            "order_pick",
            None,
            optimized_path[0],
            optimized_path[-1],
            json.dumps(optimized_path),   # ✅ correct JSON format
            total_distance
        ))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            "message": "Route optimization completed",
            "optimized_path": optimized_path,
            "total_distance": total_distance
        })

    except Exception as e:
        import traceback
        print("DEBUG - Error in run_route_optimization:", traceback.format_exc())
        return jsonify({"error": str(e)}), 500
