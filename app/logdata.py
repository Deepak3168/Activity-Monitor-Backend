from flask import Blueprint, jsonify
from .models import LogData

logdata_blueprint = Blueprint('logdata', __name__)

@logdata_blueprint.route('/logdata', methods=['GET'])
def get_logdata():
    log_data = LogData.query.order_by(LogData.timestamp.desc()).all()
    log_entries = [
        {
            'username': log.username,
            'timestamp': log.timestamp,
            'logtype': log.logtype
        } for log in log_data
    ]
    return jsonify(log_entries)
