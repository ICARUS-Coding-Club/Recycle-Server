from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# 웹드라이버로 크롬 브라우저를 실행합니다.
driver = webdriver.Chrome()
# blisgo.com 웹사이트를 엽니다.
driver.get("https://blisgo.com/")

# 검색창에 "우산"을 입력하기 위한 CSS 선택자를 정의합니다.
selector = "#ajaxsearchlite2 > div > div.proinput > form > input.orig"
# 위의 선택자를 사용하여 검색창 요소를 찾습니다.
elem = driver.find_element(By.CSS_SELECTOR,selector)
# 검색창에 "우산"을 입력합니다.
elem.send_keys("우산")

# 검색 결과가 로드될 때까지 대기합니다.
time.sleep(10)

# 검색 결과 중 첫 번째 결과에 대한 CSS 선택자를 정의합니다.
css_selector="#ajaxsearchliteres2 > div > div > div > div.asl_content > h3 > a > span"
# 첫 번째 검색 결과 요소를 찾습니다.
element = driver.find_element(By.CSS_SELECTOR,css_selector)
# 검색 결과를 클릭합니다.
element.click()

# 추가적인 로딩 시간을 위해 100초 동안 대기합니다.
time.sleep(100)
# 브라우저를 종료합니다.
driver.quit()
