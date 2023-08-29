from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from urllib.parse import quote_plus
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import base64

def cloak_url(url):
    """Encode the URL using Base64."""
    return base64.b64encode(url.encode()).decode()

# 사용자로부터 쓰레기 종류를 입력받습니다

# 크롬 웹드라이버를 실행하여 blisgo.com 웹사이트에 접속합니다.
driver = webdriver.Chrome()
driver.get(f'https://blisgo.com/category/음식물쓰레기/')

# 페이지 내의 '더 보기' 버튼의 CSS 선택자를 정의합니다.
css_selector = "#primary > nav > span"
element = driver.find_element(By.CSS_SELECTOR, css_selector)
#post-7658
#post-6360
#post-5945
#post-2128
# '더 보기' 버튼을 10번 클릭합니다.
for i in range(3):
    try:
        # 더 보기 버튼이 10초 내에 클릭 가능한 상태가 되면 클릭
        element = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
        )
        element.click()
        time.sleep(3)  # 페이지 로드를 위한 대기
    except TimeoutException:
        # 10초 동안 더 보기 버튼이 클릭 가능하지 않으면 반복 중단
        break

#요소가 완전히 보이게 하기: 요소가 화면에 완전히 보이도록 스크롤하십시오.
#driver.execute_script("arguments[0].scrollIntoView(true);", element)

# ... [previous code]

time.sleep(10)

selector = "#post-2128 > div > div > div.ast-blog-featured-section.post-thumb.ast-col-md-12 > div > a > img"
element = driver.find_element(By.CSS_SELECTOR, selector)
element.click()

time.sleep(5)  # Add a delay after the click to ensure the page loads properly

# After clicking, fetch the specific image using its CSS selector
image_element = driver.find_element(By.CSS_SELECTOR, ".elementor-image img")
image_url = image_element.get_attribute('src')



# If you want to cloak the URL, you can do so:
cloaked_url = cloak_url(image_url)
cloaked_url = base64.b64decode(cloaked_url).decode('utf-8')
print(cloaked_url)

# Close webdriver after a certain amount of time when crawling is finished.
time.sleep(100)
driver.quit()



