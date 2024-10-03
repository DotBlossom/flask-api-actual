from flask import Blueprint, request

import requests

predict_bp = Blueprint('predict', __name__)

#ㄴㄴ
@predict_bp.route('/flaskTest/<int:order>', methods=['GET'])
def response_predict_request(order):
    
    data = [
    {
        "id": 1,
        "ResultimgURL": "https://dummyimage.com/600x400/000/fff&text=Processed+Image+1",
        "imgURL": "https://dummyimage.com/600x400/000/fff&text=Original+Image+1",
        "answer_text": {
            "title": "롯데리아 이대점",
            "date": "2024/09/28 (토) 18:50",
            "address": "서울특별시 서대문구 이화여대길 59",
            "items": [
                {"name": "우이락+실비김치", "price": 3400, "quantity": 1},
                {"name": "내츄치즈스틱", "price": 2600, "quantity": 1},
                {"name": "L포테이토", "price": 2400, "quantity": 6},
                {"name": "어니언시즈닝", "price": 200, "quantity": 1},
                {"name": "치즈시즈닝", "price": 200, "quantity": 1},
                {"name": "칠리시즈닝", "price": 200, "quantity": 1},
                {"name": "실비김치맛시즈닝", "price": 200, "quantity": 1},
                {"name": "제로콜라 (L)", "price": 2200, "quantity": 1},
                {"name": "[아이스]", "price": 0, "quantity": 2},
            ],
        },
        "order": 1,
    },
    {
        "id": 2,
        "ResultimgURL": "https://dummyimage.com/600x400/000/fff&text=Processed+Image+1",
        "imgURL": "https://dummyimage.com/600x400/000/fff&text=Original+Image+1",
        "answer_text": {
            "title": "롯데리아 이대점",
            "date": "2024/09/28 (토) 18:50",
            "address": "서울특별시 서대문구 이화여대길 59",
            "items": [
                {"name": "우이락+실비김치", "price": 3400, "quantity": 1},
                {"name": "내츄치즈스틱", "price": 2600, "quantity": 1},
                {"name": "L포테이토", "price": 2400, "quantity": 6},
                {"name": "어니언시즈닝", "price": 200, "quantity": 1},
                {"name": "치즈시즈닝", "price": 200, "quantity": 1},
                {"name": "칠리시즈닝", "price": 200, "quantity": 1},
                {"name": "실비김치맛시즈닝", "price": 200, "quantity": 1},
                {"name": "제로콜라 (L)", "price": 2200, "quantity": 1},
                {"name": "[아이스]", "price": 0, "quantity": 2},
            ],
        },
        "order": 1,
    },
    
    ]
    
    
    # result return -> loading -> img + text 
    return data;
    
