## 서버 목적
image upload 후, background 형식의 작업요청을 통해, 딥러닝 서버에 보내는 http 요청을 대신 flask api에 개별적으로 연결함

### 만약 여러개의 이미지 자체를 요청과 함께 바로 dl 서버로 보내고 dl 서버에서 모든 cv 분석결과를 도출해서 보내주면

    1. 사용자는 모든 이미지 분석이 완료될 때 까지 빈화면
    2. 서버-클라이언트에서 할당한 쓰레드와, 그 사이 네트워크 오버헤드가 지속
    3. 이미지까지 같이보내고, 같이 받는 동기구조면 네트워크가 박살남

### 이러한 이유로 이미지를 여러개 올려도, flaskapi-bufferServer를 통해

  1. image bucket upload, k8s persist ssd 저장
  2. img 업로드 확정 및 dl 서버 요청을 분리하여 코드 제공
  3. dl 서버에 persist ssd route 제공하여, dl 서버는 이미지를 처리하지도,
  큰 오버헤드 network연결도 모두 안함
  4. 사용자 관점에서도, 이미지가 개별적으로 오니, 하나라도 오면 서비스를 사용하는동안
  나머지 이미지분석 결과가 도출되는 구조
  5. 각자 k8s 서비스를 loadbalancer로 서버를 구성하여, 트래픽에 따라
  유동적으로 deployment-> pod replication

이런 근거로 api-buffer server를 앞에 두고, 유사 proxy 하는 구조


### 만약 kafka를 도입하여, front 요청을 msg/pubsub로 대체한다면
    1. 더 세부적인 dataflow 컨트롤이 가능하고
    2. msg의 특징을 이용하여 secondary caching or non perisist db로 이용가능
    3. 그리고 msq의 header를 인식하여 데이터 간접 수집도 가능하고 언제든지 elastic search 3신기 도입가능
