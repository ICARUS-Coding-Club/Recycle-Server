from selenium import webdriver
import csv
import time
from selenium.webdriver.common.by import By
from urllib.parse import quote_plus # URL을 인코딩하기 위한 함수

search=input("쓰레기종류:")
driver = webdriver.Chrome()
driver.get(f'https://blisgo.com/category/{quote_plus(search)}/')

css_selector = "#primary > nav > span"
element = driver.find_element(By.CSS_SELECTOR, css_selector)

for i in range(10):
    time.sleep(3)
    element.click()

totals = driver.find_elements(By.CSS_SELECTOR, ".entry-title")  # Note the use of find_elements
searchList = []

# Iterate through the list of entry titles
for total in totals:
    temp = []
    temp.append(total.text)
    searchList.append(temp)

print(searchList)  # You probably meant to print searchList, not temp

time.sleep(100)
driver.quit()

# CSV 파일을 쓰기 모드로 엽니다.
# 인코딩은 utf-8로 설정하고, newline='' 옵션은 줄 바꿈을 처리하기 위해 사용됩니다.
f = open(f'{search}.csv', 'w', encoding='utf-8', newline='')
csvwriter = csv.writer(f) # csv 작성 객체를 생성합니다.

# searchList를 펼쳐서 CSV 파일에 한 행으로 작성합니다.
csvwriter.writerow(searchList)

f.close() # CSV 파일을 닫습니다.

print('success') # 스크레이핑 및 저장이 성공적으로 완료되었음을 나타내는 메시지를 출력합니다