from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from api.routes import api_bp
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Register blueprints
app.register_blueprint(api_bp, url_prefix='/api')

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(debug=True)