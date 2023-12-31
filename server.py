# -*- coding: utf-8 -*-
from flask import Flask, json, jsonify, request, render_template, send_from_directory
import pymysql
from PIL import Image
from datetime import datetime, date
import os
import queue
import threading
import random

from util import detectTrash
from modules.OnImageListener import OnImageListener

# template_folder daum.html 경로
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
UPLOAD_IMAGE=r'C:\Users\kmg00\PycharmProjects\Recycle-Server\server_image'

# 작업 대기열 선언
task_queue = queue.Queue()


result_queue = queue.Queue()
task_done_event = threading.Event()


class LocalImageProcessor(OnImageListener):
    def on_detect(self, images):
        print("Images detected: ", images)
        # Process the images or store the results, as per your needs.

        # 결과를 큐에 넣습니다.
        result_queue.put(images)
        # 작업 완료 이벤트를 설정합니다.
        task_done_event.set()


# 클라이언트에서 보낸 바이트배열를 이미지로 변환하고 서버에 저장
# post: 데이터를 받거나 추가하는 요청
# get: 클라이언트가 서버에 데이터를 요청

#숫자받은만큼 랜덤으로 쓰레기 보내기
@app.route('/random_trash_send', methods=['GET'])
def ramdom_trash_send():
    trash_data = request.args.get('random_id')
    int_data=int(trash_data)


    with conn.cursor() as curs:

        curs.execute(f"""SELECT id FROM trashform WHERE type IN('분류: 비닐류', '분류: 유리', '분류: 캔류', '분류: 플라스틱', '분류: 페트', '분류: 종이');""")
        id=curs.fetchall()

        id_list = [id_tuple[0] for id_tuple in id]


        number = random.sample(id_list, int_data)



        placeholders = ', '.join(['%s'] * len(number))
        sql = f"""SELECT * FROM trashform WHERE id IN ({placeholders});"""
        curs.execute(sql, tuple(number))

        rows = curs.fetchall()

        columns = [desc[0] for desc in curs.description]

        result = []
        # 각 행을 순회하면서 딕셔너리 형태로 변환하여 결과 리스트에 추가합니다.
        for row in rows:
            row_dict = dict(zip(columns, row))
            result.append(row_dict)

    return jsonify(result)

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


    onImageListener = LocalImageProcessor()
    add_task(uid_data, onImageListener)

    # 작업 완료 이벤트를 기다립니다.
    task_done_event.wait()

    # 결과 큐에서 값을 가져옵니다.
    images_detected = result_queue.get()

    # 작업 완료 이벤트를 초기화합니다.
    task_done_event.clear()

    if len(images_detected) == 0:
        images_detected.append("감지된 것이 없음")

    for image_name in images_detected:
        with conn.cursor() as curs:
            sql = f"""
                   SELECT * 
                   FROM trashform
                   WHERE name LIKE '%{image_name}%' OR tags LIKE '%{image_name}%';
                   """
            curs.execute(sql)  # SQL 쿼리를 실행합니다.

            rows = curs.fetchall()

            columns = [desc[0] for desc in curs.description]

            result = []
            # 각 행을 순회하면서 딕셔너리 형태로 변환하여 결과 리스트에 추가합니다.
            for row in rows:
                row_dict = dict(zip(columns, row))
                result.append(row_dict)

    return jsonify(result)


#요청받은쓰레기 보내기
@app.route('/multiTrashes', methods=['GET'])
def trashes_send():
    trash_data = request.args.get('idList')
    trash_data = trash_data.replace('"', '')
    if trash_data is None:
        return jsonify({"error": "idList 매개변수를 제공하세요."}), 400

    trash_list = trash_data.split()  # 공백을 기준으로 id 값을 분리합니다.

    result = []
    with conn.cursor() as curs:
        for trash_id in trash_list:
            try:
                trash_id = int(trash_id)
                curs.execute("SELECT * FROM trashform WHERE id=%s", (trash_id,))
                row = curs.fetchone()

                # 커서의 description 속성을 사용하여 테이블의 컬럼 이름들을 가져옵니다.
                columns = [desc[0] for desc in curs.description]
                if row:
                    row_dict = dict(zip(columns, row))
                    # datetime.date 객체를 문자열로 변환
                    if isinstance(row_dict['date'], date):  # datetime.date 대신 date만 사용합니다.
                        row_dict['date'] = row_dict['date'].strftime('%Y-%m-%d')
                    result.append(row_dict)
            except ValueError:
                pass  # 숫자로 변환할 수 없는 값은 무시합니다.
        return jsonify(result)
#쓰레기정보 주기
@app.route('/trashes', methods=['GET'])
def trashes():
    # 데이터베이스 연결을 커서를 통해 수행합니다.
    with conn.cursor() as curs:

        # 'trashform' 테이블에서 모든 데이터를 가져오는 SQL 쿼리를 작성합니다.
        sql = "SELECT * FROM trashform"

        curs.execute(sql)  # 위에서 정의한 SQL 쿼리를 실행합니다.

        rows = curs.fetchall()  # 쿼리의 결과로 반환된 모든 행을 가져옵니다.

        # 커서의 description 속성을 사용하여 테이블의 컬럼 이름들을 가져옵니다.
        columns = [desc[0] for desc in curs.description]

        result = []
        # 반환된 행들을 순회하며,
        # 각 행의 데이터와 컬럼 이름을 딕셔너리로 매핑하고 이를 결과 리스트에 추가합니다.
        for row in rows:
            row_dict = dict(zip(columns, row))
            # datetime.date 객체를 문자열로 변환
            if isinstance(row_dict['date'], date):  # datetime.date 대신 date만 사용합니다.
                row_dict['date'] = row_dict['date'].strftime('%Y-%m-%d')

            result.append(row_dict)

        # 최종적으로 생성된 딕셔너리 리스트를 JSON 형태로 반환합니다.
        return jsonify(result)
#인공지능 모델 결과에 맞는 데이터 주기
@app.route('/category', methods=['GET'])
def category():
    category_data = request.args.get('name')
    print(category_data)
    with conn.cursor() as curs:
        sql=f"""
            SELECT * FROM trashform
            WHERE 
            `category` = '{category_data}';
            """
        curs.execute(sql)

        rows = curs.fetchall()

        columns = [desc[0] for desc in curs.description]
        result = []

        for row in rows:
            row_dict = dict(zip(columns, row))

            # datetime.date 객체를 문자열로 변환
            if isinstance(row_dict['date'], date):  # datetime.date 대신 date만 사용합니다.
                row_dict['date'] = row_dict['date'].strftime('%Y-%m-%d')
            result.append(row_dict)

        return jsonify(result)
#블로그캠페인
@app.route('/blog_send',methods=['GET'])
def blog():
    with conn.cursor() as curs:
        sql = """
                    SELECT
                        *
                    FROM blog_information
                """
        curs.execute(sql)  # 위에서 정의한 SQL 쿼리를 실행합니다.

        rows = curs.fetchall()  # 쿼리의 결과로 반환된 모든 행을 가져옵니다.

        # 커서의 description 속성을 사용하여 테이블의 컬럼 이름들을 가져옵니다.
        columns = [desc[0] for desc in curs.description]

        result = []
        # 반환된 행들을 순회하며,
        # 각 행의 데이터와 컬럼 이름을 딕셔너리로 매핑하고 이를 결과 리스트에 추가합니다.
        for row in rows:
            row_dict = dict(zip(columns, row))
            # datetime.date 객체를 문자열로 변환
            result.append(row_dict)
        # 최종적으로 생성된 딕셔너리 리스트를 JSON 형태로 반환합니다.
        return jsonify(result)


#네이버뉴스 보내기
@app.route('/news_send',methods=['GET'])
def news():
    with conn.cursor() as curs:

        # 'trashform' 테이블에서 모든 데이터를 가져오는 SQL 쿼리를 작성합니다.
        sql = """
            SELECT
                `id`,
                `title`,
                `time`,
                REPLACE(REPLACE(`body`, '\n', ''), '\t', '') AS `body`,
                `reporter`,
                `image`
            FROM news_information
        """

        curs.execute(sql)  # 위에서 정의한 SQL 쿼리를 실행합니다.

        rows = curs.fetchall()  # 쿼리의 결과로 반환된 모든 행을 가져옵니다.

        # 커서의 description 속성을 사용하여 테이블의 컬럼 이름들을 가져옵니다.
        columns = [desc[0] for desc in curs.description]

        result = []
        # 반환된 행들을 순회하며,
        # 각 행의 데이터와 컬럼 이름을 딕셔너리로 매핑하고 이를 결과 리스트에 추가합니다.
        for row in rows:
            row_dict = dict(zip(columns, row))
            # datetime.date 객체를 문자열로 변환
            result.append(row_dict)
        # 최종적으로 생성된 딕셔너리 리스트를 JSON 형태로 반환합니다.
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

        return jsonify(result)


# flask의 route 데코레이터를 사용하여 '/배출정보' 엔드포인트에 대한 처리를 정의합니다.
@app.route('/dbhw', methods=['GET'])
def dbhw():
    road_data = request.args.get('roadAdd')
    num = road_data

    with conn.cursor() as curs:
        sql = f"""
        SELECT
        `번호`,
        `시도명`,
        `시군구명`,
        `관리구역명`,
        `관리구역대상지역명`,
        `배출장소유형`,
        `배출장소`,
        `생활쓰레기배출방법`,
        `음식물쓰레기배출방법`,
        `재활용품배출방법`,
        REPLACE(`생활쓰레기배출요일`, '+', ',') AS `생활쓰레기배출요일`,
        REPLACE(`음식물쓰레기배출요일`, '+', ',') AS `음식물쓰레기배출요일`,
        REPLACE(`재활용품배출요일`, '+', ',') AS `재활용품배출요일`,
        `생활쓰레기배출시작시각`,
        `생활쓰레기배출종료시각`,
        `음식물쓰레기배출시작시각`,
        `음식물쓰레기배출종료시각`,
        `재활용품배출시작시각`,
        `재활용품배출종료시각`,
        `미수거일`,
        `관리부서전화번호`,
        `데이터기준일자`
        FROM 
            household_waste
        WHERE 
            `번호` = {num};
        """

        curs.execute(sql)

        rows = curs.fetchall()

        columns = [desc[0] for desc in curs.description]
        result = []

        for row in rows:
            row_dict = dict(zip(columns, row))

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

# 이미지 서버 생성
@app.route('/image_server/<filename>')
def image_server(filename):
    # 지정된 파일명의 이미지를 반환합니다.
    return send_from_directory(UPLOAD_IMAGE,filename)

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
    with open('C:/Users/kmg00/Desktop/data.json', 'r', encoding='utf-8') as f:
        json_data = json.load(f)
        efile = json_data['trashform']

        for trashform in efile:
            sql = "INSERT INTO trashform (`id`,`name`,`tags`,`recycle_able`,`type`,`method`,`etc`,`image`,`date`,`category`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (
                trashform["id"],
                trashform["name"],
                trashform["tags"],
                trashform["recycle_able"],
                trashform["type"],
                trashform["method"],
                trashform["etc"],
                trashform["image"],
                current_date,
                trashform["category"]

            )
            curs.execute(sql, val)

    conn.commit()
    return "Success"
#블로그 캠페인 데이터 MySQL 저장
@app.route('/insert/blog', methods=['POST', 'GET'])
def blog_send():
    curs = conn.cursor()
    with open('C:/Users/kmg00/Desktop/out.json', 'r', encoding='utf-8') as f:
        json_data = json.load(f)
        # "blog_information" 키 아래에 있는 리스트를 순회
        for blog in json_data["blog_information"]:
            sql = """INSERT INTO blog_information(`id`,`blog_title`,`blog_time`,`blog_body`,`blog_reporter`,`blog_image`) 
                     VALUES (%s,%s,%s,%s,%s,%s)"""
            val = (
                blog.get("id"),
                blog.get("blog_title"),
                blog.get("blog_time"),
                blog.get("blog_body"),
                blog.get("blog_reporter"),
                blog.get("blog_image"),
            )
            curs.execute(sql, val)

    conn.commit()
    return "Success"

#Json 네이버뉴스 데이터 MySQL 저장
@app.route('/insert/news', methods=['POST', 'GET'])
def news_send():
    curs = conn.cursor()
    with open('C:/Users/kmg00/Desktop/데이터/분리수거.json', 'r', encoding='utf-8') as f:

        json_data = json.load(f)

        for news in json_data:
            sql = "INSERT INTO news_information(`id`,`title`,`time`,`body`,`reporter`,`image`) VALUES (%s,%s,%s,%s,%s,%s)"
            val = (
                news["id"],
                news["title"],
                news["time"],
                news["body"],
                news["reporter"],
                news["image"],
            )
            curs.execute(sql, val)

    conn.commit()
    return "Success"
def add_task(uid, listener: OnImageListener):
    # 요청을 대기열에 추가
    task_queue.put([uid, listener])


def process_tasks():
    while True:
        # 대기열에서 요청을 가져옴
        item = task_queue.get()
        task = item[0]
        listener = item[1]


        trash_list = detectTrash(task)

        print("작업완료")
        print(trash_list)

        # 작업이 끝나면 다음 작업 처리를 위해 큐에서 삭제
        task_queue.task_done()

        listener.on_detect(trash_list)



# 백그라운드 스레드에서 작업 처리
worker = threading.Thread(target=process_tasks)
worker.start()

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=8887, debug=False, threaded=True)
    except Exception as e:
        print(f"Flask 앱 실행 중 오류: {e}")
