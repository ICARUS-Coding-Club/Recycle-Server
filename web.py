#필요한 모듈과 라이브러리들을 가져옴
import csv                       # CSV 파일을 처리하기 위한 모듈
from urllib.request import urlopen  # 웹 사이트를 열고 읽기 위한 모듈
from urllib.parse import quote_plus  # URL 인코딩을 위한 함수
from bs4 import BeautifulSoup     # 웹 스크래핑을 위한 라이브러리

# 사용자로부터 검색어를 입력받음
search = input('검색어를 입력:')

# 입력받은 검색어로 blisgo.com 웹사이트의 URL을 생성
# quote_plus를 사용하여 검색어를 URL 인코딩하여 검색이 가능한 형태로 변환
url = f'https://blisgo.com/{quote_plus(search)}/'

# 생성된 URL의 웹페이지를 열고 그 내용을 읽어옴
html = urlopen(url).read()

# BeautifulSoup 객체 생성. HTML을 파싱하기 위함
soup = BeautifulSoup(html, 'html.parser')

# 'entry-title'이라는 클래스를 가진 모든 요소를 가져옴
total = soup.select(".entry-title")
searchList = []

# total에 담긴 각 요소에 대해
for i in total:
    print(i.text)