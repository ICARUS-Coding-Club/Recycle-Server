# 리본 : AI 이미지 인식 재활용 안내

🏛 경상국립대학교 코딩 동아리 이카루스  
💻 공개SW 개발자 대회 출품작  
</br>

## 프로젝트 소개  

```bash
• 간단한 스마트폰 촬영과 사진 속 쓰레기를 인식하는 인공지능 모델을 통해 올바른 재활용 방법을 제공하고자합니다.
• YOLOV5 이미지 인식 모델을 학습 및 개발하고 플라스크 자체 구축 서버를 통해 안드로이드 앱과 통신하여 동작합니다.
```

</br>
  
## 아키텍쳐
![이미지 설명](https://github.com/ICARUS-Coding-Club/Recycle-App/blob/master/image_view/%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98_%EC%88%98%EC%A0%95%EB%B3%B8.png)

</br>

## 주요 기능  

**1. 쓰레기 이미지 인식 기능**

  ```bash
  • 스마트폰 앱으로 쓰레기를 촬영하거나 사진을 업로드하여 서버로 전송합니다.
  • 서버로 전송된 사진이 저장되어 이미지 감지 학습 인공지능 모델을 실행합니다.
  • 미리 분류된 16가지 클래스로 쓰레기를 판별하여 어떤 쓰레기인지 판별합니다.
  • 판별된 쓰레기의 카테고리를 검색하여 판별된 쓰레기와 함께 관련된 쓰레기를 정보를 앱으로 반환합니다.
  • 서버로부터 반환된 쓰레기의 정보(설명, 분리수거, 배출 방법 등등)를 사용자가 알기 쉽게 제공합니다.
  ```

</br>

**2. 분리수거, 재활용과 관련된 정보 제공 기능**  

  ```bash
 • 카테고리별 쓰레기 검색을 통해 쓰레기의 배출 방법 및 분리수거 방법을 제공합니다.
 • 일반인에게 익숙하지 않은 재활용 마크에 대한 정보를 제공합니다.
 • 지역 선택을 통해 각 지역의 쓰레기 유형별(생활, 음식물, 재활용) 쓰레기 배출 방법, 장소 및 시간을 안내합니다.
 • 우리나라의 환경, 재활용, 분리수거 관련 기사를 한눈에 보기 쉽도록 안내합니다.
 • 쓰레기 재활용 현황을 한눈에 보기 쉽도록 차트 형태로 안내합니다.
  ```
    
</br>

## 라이선스

[Retrofit : Apache License 2.0](https://square.github.io/retrofit/#license)    
[Flask : BSD 3-Clause](https://flask.palletsprojects.com/en/3.0.x/license/)    
[MySql : GPL 3.0](https://www.gnu.org/licenses/)   

<br/>

## 개발 환경

```bash
1. 안드로이드 스튜디오 2023.1 (Kotlin)
2. Retrofit HTTP API
3. Visual Studio Code (Python 3.8)
4. Anaconda
5. Cuda 11.8 RTX 3070, RAM 32GB
6. Flask
7. MySQL 8.0
```

</br>

## 애플리케이션 Git Hub  

```bash
https://github.com/ICARUS-Coding-Club/Recycle-App
```

</br>

## 인공지능 Git Hub  

```bash
https://github.com/ICARUS-Coding-Club/Recycle-AI
```

</br>
