# AI 쓰레기 이미지 인식 앱

🏛 경상국립대학교 코딩 동아리 이카루스  
💻 공개SW 개발자 대회 출품작  
</br>

## 프로젝트 소개  

```bash
• 현재 우리나라의 저조한 재활용률로인한 환경 문제가 발생하고 있습니다.
• 간단한 스마트폰 촬영과 사진 속 쓰레기를 인식하는 인공지능 모델을 통해 올바른 재활용 방법을 제공하고자합니다.
• YOLOV5 이미지 인식 모델을 학습 및 개발하고 플라스크 자체 구축 서버를 통해 안드로이드 앱과 통신하여 동작합니다.
```

</br>
  
## 아키텍쳐
![이미지 설명](https://github.com/ICARUS-Coding-Club/Recycle-App/blob/master/image_view/%EC%95%84%ED%82%A4%ED%85%8D%EC%B3%90.png)

</br>

## 모델 학습 실행 명령어
    python train.py --img 640 --batch 16 --epochs 20 --data ~/dataset/data.yaml --cfg ./models/yolov5s.yaml --weights yolov5s.pt --name yolov5_coco

</br>

## 이미지 판별 실행 명령어
모델 이름 설정 [model_name]: ex) exp   
판별할 이미지 이름 [image_name]: ex) test_image

    python ./yolov5-master/detect.py --weights ./yolov5-master/runs/train/[model_name]/weights/best.pt --img 640 --conf 0.5 --source ./images/[image_name].jpg

</br>

## detect.py 인자값 설명
--weights: 사용할 모델 가중치 파일 경로  
--source: 판별할 이미지 파일 경로  
--data: (선택 사항) 데이터셋 구성 파일의 경로 지정 (기본값 'data/coco128.yaml')  
--imgsz: 이미지 detect시 입력 이미지 크기 (기본값 640)  
--conf-thres: 신뢰 임계값 지정 (기본값 0.25), 해당 임계값 이상의 객체 감지만 유효  
--iou-thres: IoU 임계값 지정 (기본값 0.45)  
--max-det: 이미지 당 최대 검출 개수 (기본값 1000)  
--device: 모델을 실행할 디바이스를 지정 (기본값 ""), CUDA 디바이스 "0", "0,1,2,3" 등으로 지정, 또는 CPU 지정 가능  
--view-img: 결과를 시각화 하여 표시 (바로 화면에 띄워줌, 안해도 저장은 됨), (인자값 없음)  
--save-txt: 결과를 텍스트 파일로 저장 (인자값 없음)  
--save-conf: 결과에 대한 확률을 --save-txt 레이블에 저장 (잘 모르겠음)  
--save-crop: 잘린 객체 감지 상자 저장 (인자값 없음), 클래스 별로 저장됨  
--nosave: 이미지 또는 비디오 저장 안함 (인자값 없음), 결과 저장 안됨  
--classes: 특정 클래스만 인식 ex) --classes 0  
--agnostic-nms: 클래스에 독립적인 NMS를 사용 (인자값 없음), (잘 모르겠음)  
--augment: 증강된 추론을 사용 (인자값 없음), 인식이 안됬던 이미지가 인식될 때가 있지만, 항상 옳은 판단을 내렸다고 할 수는 없고 오히려 잘못된 인식을 할 때도 있음  
--visualize: 특성을 시각화 (인자값 없음), 이미지 인식에 사용되는 다양한 특성을 이미지로 저장  
--update: 모든 모델을 업데이트 (인자값 없음), (잘 모르겠음)  
--project: 결과를 저장할 프로젝트 경로 지정 ex) --project [저장할 폴더 경로]  
--name: 결과를 저장할 프로젝트 이름 지정 ex) --name [저장할 프로젝트 이름]  
--exist-ok: 기존 프로젝트/이름이 있는 경우 추가하지 않음 (인자값 없음) ex) --name [저장할 프로젝트 이름] --exist-ok 해당 프로젝트 이름에 그대로 저장  
--line-thickness: 바운딩 박스의 두께를 지정 ex) --line-thickness 1  
--hide-labels: 라벨을 숨김 (인자값 없음), 바운딩 박스만 남고 라벨이 사라짐  
--hide-conf: 신뢰 점수 숨김 (인자값 없음)  
--half: FP16 하프 프리시전 추론 사용 (인자값 없음), (잘 모르겠음)  
--dnn: ONNX 추론을 위해 OpenCV DNN을 사용 (인자값 없음), (잘 모르겠음)  
--vid-stride: 비디오 프레임 속도 간격 지정 ex) --vid-stride 1 (비디오 인식을 하지 않아서 잘 모르겠음)  

</br>

## 참고 사이트
https://minding-deep-learning.tistory.com/19

</br>

## 개발 환경

```bash
1. Visual Studio Code (Python 3.8.17)
2. Anaconda
3. CUDA 11.8
4. Pytorch 11.8
5. GPU: RTX 3070, RAM: 32GB
```

</br>

## 애플리케이션 Git Hub  

```bash
https://github.com/ICARUS-Coding-Club/Recycle-App
```

</br>

## 인공지능 Git Hub  

```bash
https://github.com/ICARUS-Coding-Club/Recycle-Server
```

</br>
