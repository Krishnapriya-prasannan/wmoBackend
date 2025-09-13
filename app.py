from flask import Flask, jsonify
from flask_cors import CORS
from routes.manager_routes import manager_bp
#from routes.picker_routes import picker_bp

app = Flask(__name__)
CORS(app)  # allow cross-origin requests

# Register blueprints
app.register_blueprint(manager_bp)
#app.register_blueprint(picker_bp)

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
