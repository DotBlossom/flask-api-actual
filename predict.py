from flask import Blueprint, request

import requests

predict_bp = Blueprint('predict', __name__)

#ㄴㄴ
@predict_bp.route('/flaskTest/<int:order>', methods=['GET'])
def response_predict_request(order):
    data = []
    # result return -> loading -> img + text 
    return data;
    
