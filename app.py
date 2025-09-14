
# app.py
from flask import Flask, jsonify
from flask_cors import CORS

# Import blueprints
from routes.manager_routes import manager_bp
from routes.picker_routes import picker_bp, stock_bp
from routes.placement import placement_bp
from routes.route_optimization import route_bp
from routes.user_routes import user_bp   # ✅ added

app = Flask(__name__)
CORS(app)  # allow cross-origin requests

# -------------------------------
# Register blueprints
# -------------------------------
app.register_blueprint(manager_bp)
app.register_blueprint(picker_bp)
app.register_blueprint(stock_bp)
app.register_blueprint(placement_bp, url_prefix='/placement')
app.register_blueprint(route_bp, url_prefix='/route')
app.register_blueprint(user_bp, url_prefix='/user')  # ✅ added



# Basic home route
@app.route('/')
def home():
    return jsonify({"message": "Warehouse Management Backend running!"})

# Global error handler example
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not Found"}), 404

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
