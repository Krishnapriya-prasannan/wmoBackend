from flask import Blueprint, request, jsonify
import requests
from db import get_db

placement_bp = Blueprint("placement", __name__)

@placement_bp.route("/run_placement", methods=["POST"])
def run_placement():
    data = request.get_json()

    # ✅ Validate input
    required_keys = ["item_id", "demand_frequency", "dimensions", "current_stock", "weight_per_unit"]
    for key in required_keys:
        if key not in data or data[key] in (None, ""):
            return jsonify({"error": f"Missing or null value for key: {key}"}), 400

    print("DEBUG - incoming request data:", data)

    try:
        # ✅ Call placement microservice
        response = requests.post("http://127.0.0.1:6000/place-item", json=data)
        result = response.json()
        print("DEBUG - microservice response:", result)

        if "error" in result:
            return jsonify(result), 400

        # ✅ Extract recommended location
        recommended_location = result.get("recommended_location")
        if not recommended_location:
            msg = result.get("message", "")
            if "placed at location" in msg:
                recommended_location = msg.split("placed at location")[-1].strip()
            else:
                return jsonify({"error": "No suitable location found"}), 400

        # ✅ Clean recommended location (remove epsilon/steps part)
        if recommended_location and " " in recommended_location:
            recommended_location = recommended_location.split(" ")[0]

        # ✅ Ensure run_type is valid enum value
        run_type = data.get("run_type") or "new_stock"
        if run_type not in ["weekly", "new_stock"]:
            run_type = "new_stock"

        # ✅ Force string conversion for safety
        item_id = str(data["item_id"])
        rec_loc = str(recommended_location)
        run_type = str(run_type)

        print("DEBUG - final values for insert:", {
            "item_id": item_id,
            "recommended_location": rec_loc,
            "run_type": run_type
        })

        # ✅ Insert into DB safely
        conn = get_db()
        cursor = conn.cursor(dictionary=True)  # safer type handling
        cursor.execute("""
            INSERT INTO placement_recommendations
            (item_id, recommended_location, run_type)
            VALUES (%s, %s, %s)
        """, (item_id, rec_loc, run_type))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            "message": "Placement stored successfully",
            "item_id": item_id,
            "recommended_location": rec_loc,
            "run_type": run_type
        })

    except Exception as e:
        # ✅ Extra debug for unexpected errors
        import traceback
        print("DEBUG - Unexpected error:", traceback.format_exc())
        return jsonify({"error": str(e)}), 500
