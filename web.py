# 필요한 모듈과 라이브러리들을 가져옴
import csv                       # CSV 파일을 처리하기 위한 모듈
from urllib.request import urlopen  # 웹 사이트를 열고 읽기 위한 모듈
from urllib.parse import quote_plus  # URL 인코딩을 위한 함수
from bs4 import BeautifulSoup     # 웹 스크래핑을 위한 라이브러리
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from urllib.parse import quote_plus

driver = webdriver.Chrome()
driver.get("https://blisgo.com/category/%ec%9d%bc%eb%b0%98%ec%93%b0%eb%a0%88%ea%b8%b0/")

css_selector="#primary > nav > span"
element = driver.find_element(By.CSS_SELECTOR,css_selector)
for i in range(10):
    time.sleep(3)
    element.click()
# 사용자로부터 검색어를 입력받음
search = input('검색어를 입력:')

# 입력받은 검색어로 blisgo.com 웹사이트의 URL을 생성
# quote_plus를 사용하여 검색어를 URL 인코딩하여 검색이 가능한 형태로 변환
url = f'https://blisgo.com/category/{quote_plus(search)}/'

# 생성된 URL의 웹페이지를 열고 그 내용을 읽어옴
html = urlopen(url).read()

# BeautifulSoup 객체 생성. HTML을 파싱하기 위함
soup = BeautifulSoup(html, 'html.parser')

# 'entry-title'이라는 클래스를 가진 모든 요소를 가져옴
total = soup.select(".entry-title")
searchList = []

# total 리스트 내의 각 요소에 대해
for i in total:
    temp = []               # 임시 리스트 생성
    temp.append(i.text)     # 해당 요소의 텍스트(내용)를 임시 리스트에 추가
    searchList.append(temp) # 임시 리스트를 searchList에 추가

# CSV 파일을 쓰기 모드로 열기 (파일명은 사용자가 입력한 검색어로 지정)
# 인코딩은 utf-8로 설정하며, newline='' 옵션은 줄바꿈 처리를 위해 사용
f = open(f'{search}.csv', 'w', encoding='utf-8', newline='')
csvwriter = csv.writer(f)  # csv writer 객체 생성

# searchList의 각 요소(리스트)를 CSV 파일에 한 줄씩 쓰기
for i in searchList:
    csvwriter.writerow(i)

f.close()  # CSV 파일 닫기ㅋ

print('성공')  # 스크래핑 및 저장이 성공적으로 완료되었음을 알리는 메시지 출력

time.sleep(100)  # waits for 10 seconds
driver.quit()
