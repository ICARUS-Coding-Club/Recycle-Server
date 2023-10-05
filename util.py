import os

def detectTrash(id):
    # 쓰레기 클래스
    trash_dict = {
        0: "유리",
        1: "페트",
        2: "스티로품",
        3: "캔",
        4: "우유팩",
        5: "종이컵",
        6: "종이",
        7: "박스",
        8: "플라스틱",
        9: "배터리",
        10: "고무장갑",
        11: "전구",
        12: "치약",
        13: "세제",
        14: "과일포장망"
    }

    # user id 받기
    user_id = id

    # 텍스트 파일 초기화
    file_path = rf"yolov5-master\runs\detect\trash\labels\{user_id}.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("")

    # 이미지 판별
    command = rf"python ./yolov5-master/detect.py --weights ./yolov5-master/runs/train/yolov5_trash_final/weights/best.pt --img 640 --conf 0.5 --source ./images/{user_id}.png --save-txt --name trash --exist-ok"
    os.system(command)

    result = []
    # 파일을 읽기 모드로 엽니다
    with open(file_path, "r", encoding="utf-8") as file:
        # 파일의 각 줄을 순회하면서 데이터를 처리합니다.
        for line in file:
            # 각 줄을 공백을 기준으로 분리합니다.
            parts = line.split()
            
            # 첫 번째 숫자를 추출합니다.
            first_number = int(parts[0])
            
            result.append(trash_dict[first_number])

    return result