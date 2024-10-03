
from flask import Blueprint, request, jsonify
import requests
import os


process_bp = Blueprint('process', __name__)



def download_image(image_url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(image_url, headers=headers)
    
    response.raise_for_status() 
    

    img = response.content
    content_type = response.headers['Content-Type'] 
    return img, content_type
    
# URL에서 파일명 추출 함수
def get_filename_from_url(image_url):
    return os.path.basename(image_url)


@process_bp.route('/flaskapi/<int:id>', methods=['POST'])
def send_to_gpu_server(id):
    global address  # 전역 변수 사용
    global title  # 전역 변수 사용
    
    data = request.json  # 요청에서 JSON 데이터 가져오기
    image_url = data.get("imageUrl")
    print(image_url)
    if not image_url:
        return jsonify({"error": "이미지 URL 없음"}), 400

    try:
        image_file, content_type = download_image(image_url)

        # 파일명 자동 추출
        filename = get_filename_from_url(image_url)
        print(filename)
        # 파일 정보 구성
        file_info = {
            "filename": filename,
            "file_content": image_file,  # 파일 내용 일부만 표시
            "content_type": content_type,
        }
    except Exception as e:
        return jsonify({"이미지 전송 오류": str(e)}), 500

    # OCR URL
    path_ocr = os.environ.get('OCR_URL')
    ocr_url = f'http://{path_ocr}/ocr'
    
    # 이미지 파일을 OCR에 맞춰 변환(dict 형식)
    files = {'image': (file_info['filename'], file_info['file_content'], file_info['content_type'])}

    try:
        # OCR POST 요청
        ocr_response = requests.post(ocr_url, files=files)

        # OCR 요청 성공시
        if ocr_response.ok:
            ocr_data = ocr_response.json()

            # OCR 데이터 로그 출력
            # logging.info(f"OCR 데이터: {ocr_data}")

            items = []  # 메뉴 아이템 초기화
            
            # OCR 데이터에서 필요한 정보를 추출
            title = ocr_data.get('매장이름', None)
            date = ocr_data.get('날짜', None)
            address = ocr_data.get('주소', None)
            # 주소에서 후처리
            if address:
                address = address.replace(' 1중', '').replace(' 1층', '').strip()
                
            if '메뉴 및 가격' in ocr_data:
                items = ocr_data['메뉴 및 가격']

            print(items)
            items_objfy = []
            keys = ['name' , 'quantity', 'price']
            for i in range(len(items)):
                item = items[i]
                item[2] = int(item[2].replace(",", ""))
                item_obj = {key: value for key, value in zip(keys, item)}
                items_objfy.append(item_obj)

            # 추가적인 처리 로직
            return jsonify({
                "id" : id,
                "ResultimgURL" : "none",
                "imgURL" : image_url,
                "answer_text" : {
                    "title" : title,
                    "date" : date,
                    "address" : address,
                    "items" : items_objfy
                },
                "order" : id
            }), 200
            
        else:
            return jsonify({"OCR 요청 실패": ocr_response.text}), 500

    except Exception as e:
        return jsonify({"이미지 전송 오류": str(e)}), 500


        

    '''
    # OCR URL
    ocr_url = 'http://ocr-api:5000/ocr'
    
    # 이미지 파일을 OCR에 맞춰 변환(dict 형식)
    files = {'image': (file_info.filename, file_info.file_content, file_info.content_type)}

    try:
        # OCR POST 요청
        ocr_response = requests.post(ocr_url, files=files)

        # OCR 요청 성공시
        if ocr_response.ok:
            ocr_data = ocr_response.json()
            call_menu_item = []  # 메뉴 아이템 초기화
            
            # OCR 데이터에서 필요한 정보를 추출
            if '메뉴 및 가격' in ocr_data:
                call_menu_item = ocr_data['메뉴 및 가격']
                
            # 주소 정보를 저장
            address_box = ocr_data.get('주소', None)
            # 주소에서 후처리
            if address_box:
                address_box = address_box.replace(' 1중', '').replace(' 1층', '').strip()

            # 추가적인 처리 로직
            return jsonify({
                "메뉴 및 가격": call_menu_item,
                "주소": address_box  # 주소도 반환
            }), 200
            
        else:
            return jsonify({"OCR 요청 실패": ocr_response.text}), 500

    except Exception as e:
        return jsonify({"이미지 전송 오류": str(e)}), 500
'''
