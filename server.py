# -*- coding: utf-8 -*-
from flask import Flask, json, jsonify, request, Response, send_from_directory, render_template
import pymysql
from PIL import Image

from datetime import datetime, timedelta, date
from werkzeug.utils import secure_filename

import os

import queue
import threading

# template_folder daum.html경로
app = Flask(__name__, template_folder=r'C:\Users\kmg00\PycharmProjects\Recycle-Server')

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
UPLOAD_FOLDER = r'C:\Users\kmg00\PycharmProjects\Recycle-Server\images'

# 작업 대기열 선언
task_queue = queue.Queue()


# 클라이언트에서 보낸 바이트배열를 이미지로 변환하고 서버에 저장
# post: 데이터를 받거나 추가하는 요청
# get: 클라이언트가 서버에 데이터를 요청


# 이미지 받기
@app.route('/upload', methods=['POST'])
# image folder에 uid FOLDER 만들고 그 안에 안드로이드에서 준 이미지.PNG를 저장
def upload_image():
    # POST 요청에서 이미지 데이터 추출
    if 'image' not in request.files:
        return jsonify({"error": "이미지가 제공되지 않았습니다."}), 400

    image_file = request.files['image']

    # 만약 'uid'라는 추가 필드가 필요하다면 다음과 같이 추출할 수 있습니다
    uid_data = request.form.get('uid')
    # 여기서는 이미지 파일명을 UID로 사용합니다.
    # uid_data = secure_filename(image_file.filename)

    # PIL (Python Imaging Library)을 사용하여 이미지 파일을 엽니다.
    image = Image.open(image_file)

    # 지정된 디렉토리가 존재하는지 확인하고, 없으면 생성합니다.
    # directory_path = os.path.join(UPLOAD_FOLDER, uid_data)
    # if not os.path.exists(directory_path):
    #    os.makedirs(directory_path)

    # 지정된 디렉토리에 이미지 저장
    filename = os.path.join(UPLOAD_FOLDER, f'{uid_data}.png')
    image.save(filename)

    add_task(uid_data)
    # 성공 메시지와 이미지가 저장된 경로로 응답
    return jsonify({"message": "이미지가 성공적으로 저장되었습니다!", "path": filename})


# 폴더에 있는 모든 이미지 서빙
@app.route('/image/<uid>')
def serve_image1(uid):
    return send_from_directory(r'C:\\Users\\kmg00\\Desktop\\image', uid)


# 특정이미지 서빙^^
@app.route('/image/<uid>/<image_name>')
def serve_image2(uid, image_name):
    return send_from_directory(r'C:\\Users\\kmg00\\Desktop\\image', uid, image_name.png)


@app.route('/trashes', methods=['GET'])
def trashes():
    with conn.cursor() as curs:
        # household_waste 테이블에서 모든 데이터를 선택하는 SQL 쿼리를 정의합니다.
        sql = "SELECT * FROM trashform"
        curs.execute(sql)  # SQL 쿼리를 실행합니다.

        rows = curs.fetchall()  # 모든 행을 가져옵니다.

        # 커서의 description 속성을 사용하여 컬럼 이름을 가져옵니다.
        columns = [desc[0] for desc in curs.description]

        result = []
        # 각 행을 순회하면서 딕셔너리 형태로 변환하여 결과 리스트에 추가합니다.
        for row in rows:
            row_dict = dict(zip(columns, row))
            result.append(row_dict)

        return jsonify(result)


# 시도명 시군구명 관리구역대상지역 관리구역명
@app.route('/dbwt', methods=['POST', 'GET'])
def dbwt():
    road_data = request.args.get('roadAdd')
    road_array = road_data.split() if road_data else []
    s = road_array[1]
    if road_array:
        if road_array[0] == '경남':
            r = road_array[0] = '경상남도'
        elif road_array[0] == '충남':
            r = road_array[0] = '충청남도'
        elif road_array[0] == '경북':
            r = road_array[0] = '경상북도'
        elif road_array[0] == '충북':
            r = road_array[0] = '충청북도'
        elif road_array[0] == '전남':
            r = road_array[0] = '전라남도'
        elif road_array[0] == '전북':
            r = road_array[0] = '전라북도'
        elif road_array[0] == '강원':
            r = road_array[0] = '강원도'
        elif road_array[0] == '경기':
            r = road_array[0] = '경기도'
        elif road_array[0] == '제주':
            r = road_array[0] = '제주특별자치도'
        elif road_array[0] == '서울':
            r = road_array[0] = '서울특별시'
        elif road_array[0] == '부산':
            r = road_array[0] = '부산광역시'
        elif road_array[0] == '대구':
            r = road_array[0] = '대구광역시'
        elif road_array[0] == '인천':
            r = road_array[0] = '인천광역시'
        elif road_array[0] == '광주':
            r = road_array[0] = '광주광역시'
        elif road_array[0] == '대전':
            r = road_array[0] = '대전광역시'
        elif road_array[0] == '울산':
            r = road_array[0] = '울산광역시'

        # 커서를 사용하여 데이터베이스 연결을 엽니다.
        with conn.cursor() as curs:
            sql = """SELECT 번호,시도명,시군구명,관리구역대상지역명,관리구역명
                     FROM household_waste
                     WHERE `시도명`=%s AND `시군구명`=%s"""

            curs.execute(sql, (r, s))  # SQL 쿼리를 실행합니다.

            rows = curs.fetchall()

            columns = [desc[0] for desc in curs.description]

            result = []
            # 각 행을 순회하면서 딕셔너리 형태로 변환하여 결과 리스트에 추가합니다.
            for row in rows:
                row_dict = dict(zip(columns, row))
                result.append(row_dict)

        print(result)
        return jsonify(result)


# flask의 route 데코레이터를 사용하여 '/배출정보' 엔드포인트에 대한 처리를 정의합니다.
@app.route('/dbhw', methods=['GET'])
def dbhw():
    road_data = request.args.get('roadAdd')
    num = road_data

    with conn.cursor() as curs:
        sql = f"""SELECT * FROM household_waste WHERE `번호` = {num}"""
        curs.execute(sql)

        rows = curs.fetchall()

        columns = [desc[0] for desc in curs.description]
        result = []

        for row in rows:
            row_dict = dict(zip(columns, row))

            # timedelta 객체를 HH:MM 형식으로 변환
            for key in ['생활쓰레기배출시작시각', '생활쓰레기배출종료시각', '음식물쓰레기배출시작시각', '음식물쓰레기배출종료시각', '재활용품배출시작시각', '재활용품배출종료시각']:
                if isinstance(row_dict[key], timedelta):
                    total_seconds = row_dict[key].total_seconds()
                    hours = int(total_seconds // 3600)
                    minutes = int((total_seconds % 3600) // 60)
                    row_dict[key] = f"{hours:02}:{minutes:02}"

            # datetime.date 객체를 문자열로 변환
            if isinstance(row_dict['데이터기준일자'], date):  # datetime.date 대신 date만 사용합니다.
                row_dict['데이터기준일자'] = row_dict['데이터기준일자'].strftime('%Y-%m-%d')

            result.append(row_dict)

    print(result[0])
    return jsonify(result[0])


# Daum우편번호 html
@app.route('/daum', methods=['GET'])
def Zip_code():
    return render_template('daum.html')


# Json 생활쓰레기종합배출정보 데이터 Mysql에 저장
@app.route('/insert/household_waste', methods=['POST', 'GET'])
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


# Json 쓰레기정보 데이터 Mysql에 저장
@app.route('/insert/trashform', methods=['POST', 'GET'])
def trashform_send():
    curs = conn.cursor()
    current_date = datetime.now().strftime('%Y-%m-%d')
    with open('C:/Users/kmg00/Desktop/Rdata/2128.json', 'r', encoding='utf-8') as f:
        json_data = json.load(f)
        efile = json_data['trashform']

        for trashform in efile:
            sql = "INSERT INTO trashform (`id`,`name`,`type`,`method`,`etc`,`views`,`image`,`date`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (
                trashform["id"],
                trashform["name"],
                trashform["type"],
                trashform["method"],
                trashform["etc"],
                trashform["views"],
                trashform["image"],
                current_date,
            )
            curs.execute(sql, val)

    conn.commit()
    return "Success"


def add_task(uid):
    # 요청을 대기열에 추가
    task_queue.put(uid)

    return jsonify({'status': 'task added'}), 200


def process_tasks():
    while True:
        # 대기열에서 요청을 가져옴
        task = task_queue.get()

        # 실제 작업 처리 로직 (예: 5초 지연)
        os.system(
            '  python ./yolov5-master/detect.py --weights ./yolov5-master/runs/train/model01/weights/best.pt'
            f' --img 640 --conf 0.5 --source ./images/{task}.png')

        print("작업완료")

        # 작업이 끝나면 다음 작업 처리를 위해 큐에서 삭제
        task_queue.task_done()


# 백그라운드 스레드에서 작업 처리
worker = threading.Thread(target=process_tasks)
worker.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8887, debug=True, threaded=True)
