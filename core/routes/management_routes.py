"""
Management Routes - Handles all database management and utility endpoints.
"""
from flask import Blueprint, request, jsonify
from core import database

management_bp = Blueprint('management', __name__)

@management_bp.route('/truncate-table', methods=['POST'])
def truncate_table():
    """Truncate the database table - DANGEROUS OPERATION"""
    try:
        result = database.truncate_table()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500 