import csv # CSV 파일 처리를 위한 모듈
from urllib.request import urlopen # 웹사이트를 열고 읽기 위한 모듈
from urllib.parse import quote_plus # URL을 인코딩하기 위한 함수
from bs4 import BeautifulSoup # 웹 스크레이핑을 위한 라이브러리

# 사용자로부터 검색어를 입력받습니다.
trash=input('무슨 쓰레기인가요')
search = input('쓰레기 종류를 입력하세요:')
search1=input('쓰레기 검색:')

# 입력된 검색어로 blisgo.com 웹사이트의 URL을 생성합니다.
# quote_plus를 사용하여 쿼리를 URL로 인코딩합니다.
url = f'https://blisgo.com/{quote_plus(search)}/{quote_plus(search1)}/'

# 생성된 URL의 웹페이지를 열고 내용을 읽습니다.
html = urlopen(url).read()

# BeautifulSoup 객체를 생성합니다. HTML을 파싱하기 위해.
soup = BeautifulSoup(html, 'html.parser')

# 'entry-title' 클래스를 가진 모든 요소를 가져옵니다.
total1 = soup.select('.elementor-text-editor.elementor-clearfix')

searchList = []

searchList.append(trash)

for i in total1[:4]:
    searchList.append(i.text)

# CSV 파일을 쓰기 모드로 엽니다.
# 인코딩은 utf-8로 설정하고, newline='' 옵션은 줄 바꿈을 처리하기 위해 사용됩니다.
f = open(f'{trash}.csv', 'w', encoding='utf-8', newline='')
csvwriter = csv.writer(f) # csv 작성 객체를 생성합니다.

# searchList를 펼쳐서 CSV 파일에 한 행으로 작성합니다.
csvwriter.writerow(searchList)

f.close() # CSV 파일을 닫습니다.

print('success') # 스크레이핑 및 저장이 성공적으로 완료되었음을 나타내는 메시지를 출력합니다
