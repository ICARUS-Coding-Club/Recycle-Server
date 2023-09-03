import csv
import json

def csv_to_json(csv_filename, json_filename):
    # CSV 파일을 읽기 위한 딕셔너리를 생성
    data = []

    with open(csv_filename, 'r', encoding='cp949') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            data.append(row)

    # JSON 파일로 저장
    with open(json_filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

# 사용 예시
csv_to_json(r'C:\Users\kmg00\Desktop\데이터 변\분리수거쓰레기.csv', r'C:\Users\kmg00\Desktop\데이터\data.json')

