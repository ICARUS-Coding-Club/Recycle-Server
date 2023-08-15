import csv # CSV 파일 처리를 위한 모듈
from urllib.request import urlopen # 웹사이트를 열고 읽기 위한 모듈
from urllib.parse import quote_plus # URL을 인코딩하기 위한 함수
from bs4 import BeautifulSoup # 웹 스크레이핑을 위한 라이브러리

# 사용자로부터 검색어를 입력받습니다.
#trash=input('무슨 쓰레기인가요')
#search = input('쓰레기 종류를 입력하세요:')
#search1=input('쓰레기 검색:')

# 입력된 검색어로 blisgo.com 웹사이트의 URL을 생성합니다.
# quote_plus를 사용하여 쿼리를 URL로 인코딩합니다.
url = f'https://blisgo.com/%ed%8f%90%ea%b1%b4%ec%a0%84%ec%a7%80-%ec%a0%84%ec%9a%a9-%ec%88%98%ea%b1%b0%ed%95%a8/%eb%85%b8%ed%8a%b8%eb%b6%81-%eb%b0%b0%ed%84%b0%eb%a6%ac-%eb%b2%84%eb%a6%ac%eb%8a%94-%eb%b2%95/'

# 생성된 URL의 웹페이지를 열고 내용을 읽습니다.
html = urlopen(url).read()

# BeautifulSoup 객체를 생성합니다. HTML을 파싱하기 위해.
soup = BeautifulSoup(html, 'html.parser')

# 'entry-title' 클래스를 가진 모든 요소를 가져옵니다.
total1 = soup.select('.elementor-text-editor.elementor-clearfix')

...

# Lists to store extracted data
data_lists = []

for content in total1[:3]:  # Adjust this slice according to the number of lines you're expecting
    text_content = content.text.strip()  # Removes any leading or trailing whitespace

    # If the content starts with "Recycling:" or "Classification:", we'll strip that prefix
    for prefix in ["Recycling:", "Classification:"]:
        if text_content.startswith(prefix):
            text_content = text_content.replace(prefix, "").strip()

    # Append text_content to data_lists
    data_lists.append(text_content)

print(data_lists)  # This will display the content of data_lists after scraping and processing

# If you want to save the data to a CSV file, you can continue with the CSV writing code.
