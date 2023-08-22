from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from urllib.parse import quote_plus
import pandas as pd

# 사용자로부터 쓰레기 종류를 입력받습니다
search = input("쓰레기 종류: ")

# 크롬 웹드라이버를 실행하여 blisgo.com 웹사이트에 접속합니다.
driver = webdriver.Chrome()
driver.get(f'https://blisgo.com/category/{quote_plus(search)}/')

# 페이지 내의 '더 보기' 버튼의 CSS 선택자를 정의합니다.
css_selector = "#primary > nav > span"
element = driver.find_element(By.CSS_SELECTOR, css_selector)

# '더 보기' 버튼을 10번 클릭합니다.
for i in range(10):
    time.sleep(3)
    element.click()

# 페이지 내의 모든 항목의 제목을 수집합니다.
totals = driver.find_elements(By.CSS_SELECTOR, ".entry-title")
searchList = []

for total in totals:
    searchList.append(total.text)

print(searchList)

# 크롤링이 끝나면 일정 시간 후에 웹드라이버를 종료합니다.
time.sleep(100)
driver.quit()

# 수집한 데이터를 pandas DataFrame으로 변환합니다.
df = pd.DataFrame({search: searchList})

# DataFrame을 Excel 파일로 저장합니다.
df.to_excel(f'{search}.xlsx', index=False, engine='xlsxwriter')

print('success')
