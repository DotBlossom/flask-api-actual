from flask import Blueprint, request, jsonify
from google.cloud import storage
from urllib.parse import quote
from dotenv import load_dotenv
import os


load_dotenv()  # .env 파일 로드
bucket_name = "pj3-payday"

upload_bp = Blueprint('upload', __name__)
download_bp = Blueprint('download', __name__)

send_predict_request_bp = Blueprint('predict', __name__)

import urllib.request
import requests
@download_bp.route('/flaskapi/download')
def download_image():
    #image_url = request.args.get('image_url')
    image_url = "https://storage.googleapis.com/pj3-payday/%EB%B2%8C.png"
    
    response = requests.get(image_url)
    response.raise_for_status() 
    
    img = response.content
    
    return jsonify({'message': 'Image downloaded successfully'}), 200
    
    
    

# upload는 그냥 뭐 통채로 .. 해도 .. 일단은 단일 코드
@upload_bp.route('/flaskapi/upload/<int:roomId>', methods=['POST'])
def upload_image(roomId):
    if 'image' not in request.files:
        return jsonify({'description': 'No image file provided'}), 400

    # bucket Connections
    KEY_PATH = os.environ.get('GOOGLE_APPLICATION_PATH')
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = KEY_PATH
    
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    
    

    #Type: blob(form_data)
    images = request.files.getlist('image')
    uploaded_image_urls = []
    
    for image in images:
        # try 구현 할수도 있음
        content_type = image.content_type
        blob = bucket.blob(image.filename)
        blob.upload_from_file(image, content_type=content_type)
    
        uploaded_image_urls.append(blob.public_url);


   
    return jsonify({'imageUrl': uploaded_image_urls}), 200


# 버튼 하나 더 만들자.. 최종 보내기 .. 재 업로드 or 나머지만 보내기 .. 
# 된다면 로딩 ㄱㄱ 







'''
original_filename = image.filename_, 
            file_extension = os.path.splitext(original_filename)
            new_filename = f"{uuid.uuid4()}{file_extension}"

'''

'''
# signal 처리, 복잡도 감소
image_uploaded = signal('image-uploaded')

@image_uploaded.connect
def send_predict_request(sender, **kwargs):
    receiptId = kwargs['receiptId']
    image_url = kwargs['imageUrl']
    order = kwargs['order']  # 필요에 따라 order 값 설정

    # 다른 Flask 서버로 요청 보내기
    response = requests.post(f'http://localhost:5333/gpu/predict/{receiptId}/{order}', json={'imageUrl': image_url})


    return response.json(), response.status_code
'''