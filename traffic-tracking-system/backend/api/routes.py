from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from models.detector import VehicleDetector
from utils.file_handler import allowed_file, save_file

api_bp = Blueprint('api', __name__)
detector = VehicleDetector()

@api_bp.route('/process', methods=['POST'])
def process_media():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = save_file(file, filename)
        
        try:
            # Process the file
            result = detector.process(filepath)
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400