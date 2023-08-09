import requests
from bs4 import BeautifulSoup

#웹페이지 요청
res = requests.get("https://blisgo.com/")
res.raise_for_status() # 문제가 발생했다면 에러를 발생시키고, 문제가 없다면 계속 진행

#웹페이지 파싱
soup = BeautifulSoup(res.text, 'lxml')

#원하는 정보를 선택하여 추출
titles = soup.find_all("div", attrs={"class": "title"})
for t in titles:
    title = t.get_text()
    print(title)