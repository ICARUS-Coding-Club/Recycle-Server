from flask import Flask, json, jsonify, request,Response,send_from_directory
import pymysql
from PIL import Image
import io
import os
from datetime import datetime,timedelta,date
from werkzeug.utils import secure_filename

app = Flask(__name__)

# MySQL 연결 설정
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='1234',
    db='recycle_db',
    charset='utf8'
)

# MySQL 연결 확인
if conn.open:
    print('connected')
else:
    print('disconnected')
# 저장할 경로
UPLOAD_FOLDER = r'C:\Users\kmg00\Desktop\image'

# 클라이언트에서 보낸 바이트배열를 이미지로 변환하고 서버에 저장
#post: 데이터를 받거나 추가하는 요청
#get: 클라이언트가 서버에 데이터를 요청
#이미지 받기
@app.route('/upload', methods=['POST'])
def upload_image():
    # POST 요청에서 이미지 데이터 추출
    if 'image' not in request.files:
        return jsonify({"error": "이미지가 제공되지 않았습니다."}), 400

    image_file = request.files['image']

    # 만약 'uid'라는 추가 필드가 필요하다면 다음과 같이 추출할 수 있습니다.
    # uid_data = request.form.get('uid')
    # 여기서는 이미지 파일명을 UID로 사용합니다.
    uid_data = secure_filename(image_file.filename)

    # PIL (Python Imaging Library)을 사용하여 이미지 파일을 엽니다.
    image = Image.open(image_file)

    # 지정된 디렉토리가 존재하는지 확인하고, 없으면 생성합니다.
    directory_path = os.path.join(UPLOAD_FOLDER, uid_data)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # 지정된 디렉토리에 이미지 저장
    filename = os.path.join(directory_path, '쓰레기.png')
    image.save(filename)

    # 성공 메시지와 이미지가 저장된 경로로 응답
    return jsonify({"message": "이미지가 성공적으로 저장되었습니다!", "path": filename})

#특정이미지 서빙
@app.route('/image/<filename>')
def serve_image1(filename):
    return send_from_directory(r'C:\\Users\\kmg00\\Desktop\\image\\image.jpg', filename)
#모든이미지 서빙
@app.route('/image')
def serve_image2():
    return send_from_directory(r'C:\\Users\\kmg00\\Desktop\\image\\image.jpg', '쓰레기.png')

# Flask의 route 데코레이터를 사용하여 '/배출정보' 엔드포인트에 대한 처리를 정의합니다.
@app.route('/배출정보')
def dbhw():
    # 커서를 사용하여 데이터베이스 연결을 엽니다..
    with conn.cursor() as curs:
        # household_waste 테이블에서 모든 데이터를 선택하는 SQL 쿼리를 정의합니다.
        sql = "SELECT * FROM household_waste"
        curs.execute(sql)  # SQL 쿼리를 실행합니다.

        rows = curs.fetchall()  # 모든 행을 가져옵니다.

        # 커서의 description 속성을 사용하여 컬럼 이름을 가져옵니다.
        columns = [desc[0] for desc in curs.description]

        result = []
        # 각 행을 순회하면서 딕셔너리 형태로 변환하여 결과 리스트에 추가합니다.
        for row in rows:
            row_dict = dict(zip(columns, row))
            result.append(row_dict)

        # 커스텀 시리얼라이저 함수를 정의합니다.
        # date, datetime 및 timedelta 객체를 처리하기 위한 것입니다.
        def custom_serializer(obj):
            if isinstance(obj, (date, datetime)):
                return obj.strftime('%Y-%m-%d')  # 날짜 및 시간을 문자열로 반환
            elif isinstance(obj, timedelta):
                return obj.total_seconds()  # timedelta 객체를 총 초로 반환
            # 알 수 없는 타입에 대한 처리
            raise TypeError(f"Type {type(obj)} not serializable")

        try:
            # 결과 리스트를 JSON 형식으로 변환합니다.
            response_data = json.dumps(result, ensure_ascii=False, default=custom_serializer)

            # JSON 형식의 응답을 반환합니다.
            return Response(response=response_data, content_type="application/json; charset=utf-8")
        except TypeError:
            # 오류가 발생할 경우 에러 메시지와 함께 응답을 반환합니다.
            return jsonify({"error": "An error occurred while processing the request."})

#Json 데이터 Mysql에 저장
@app.route('/insert', methods=['POST', 'GET'])
def household_waste_send():
    curs = conn.cursor()
    with open('C:/Users/kmg00/Desktop/Rdata/생활쓰레기종합배출정보.json', 'r', encoding='utf-8') as f:
        json_data = json.load(f)
        efile = json_data['household_waste']

        for household_waste in efile:
            sql = "INSERT INTO household_waste (`번호`,`시도명`,`시군구명`,`관리구역명`,`관리구역대상지역명`,`배출장소유형`,`배출장소`,`생활쓰레기배출방법`,`음식물쓰레기배출방법`,`재활용품배출방법`,`생활쓰레기배출요일`,`음식물쓰레기배출요일`,`재활용품배출요일`,`생활쓰레기배출시작시각`,`생활쓰레기배출종료시각`,`음식물쓰레기배출시작시각`,`음식물쓰레기배출종료시각`,`재활용품배출시작시각`,`재활용품배출종료시각`,`미수거일`,`관리부서전화번호`,`데이터기준일자`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (
                household_waste["번호"],
                household_waste["시도명"],
                household_waste["시군구명"],
                household_waste["관리구역명"],
                household_waste["관리구역대상지역명"],
                household_waste["배출장소유형"],
                household_waste["배출장소"],
                household_waste["생활쓰레기배출방법"],
                household_waste["음식물쓰레기배출방법"],
                household_waste["재활용품배출방법"],
                household_waste["생활쓰레기배출요일"],
                household_waste["음식물쓰레기배출요일"],
                household_waste["재활용품배출요일"],
                household_waste["생활쓰레기배출시작시각"],
                household_waste["생활쓰레기배출종료시각"],
                household_waste["음식물쓰레기배출시작시각"],
                household_waste["음식물쓰레기배출종료시각"],
                household_waste["재활용품배출시작시각"],
                household_waste["재활용품배출종료시각"],
                household_waste["미수거일"],
                household_waste["관리부서전화번호"],
                household_waste["데이터기준일자"]
            )
            curs.execute(sql, val)

    conn.commit()
    return "Success"

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8887,debug=True)