from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from urllib.parse import quote_plus
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import base64

# Base64를 사용하여 URL을 인코딩하는 함수
def cloak_url(url):
    """URL을 Base64로 인코딩합니다."""
    return base64.b64encode(url.encode()).decode()

# 사용자로부터 휴지 유형과 이미지 번호를 입력받습니다.
search = input("쓰레기 유형: ")
img_num = input('쓰레기 번호: ')

# 크롬 웹드라이버를 초기화하고 지정된 URL로 이동합니다.
driver = webdriver.Chrome()
driver.get(f'https://blisgo.com/category/{quote_plus(search)}/')

# 페이지의 '더 보기' 버튼을 위한 CSS 선택자
css_selector = "#primary > nav > span"
element = driver.find_element(By.CSS_SELECTOR, css_selector)

# '더 보기' 버튼을 최대 10번 클릭하여 콘텐츠를 더 로드합니다
for i in range(10):
    try:
        # '더 보기' 버튼이 클릭 가능해질 때까지 기다린 후 클릭합니다.
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
        )
        element.click()
        time.sleep(3)  # 각 클릭 후 콘텐츠가 로드되기를 기다립니다.
    except TimeoutException:
        # '더 보기' 버튼이 지정된 시간 내에 클릭 가능하지 않으면 반복을 중단합니다.
        break

# 모든 콘텐츠가 로드될 때까지 기다립니다.
time.sleep(10)

# 제공된 이미지 번호를 기반으로 특정 이미지로 이동합니다.
selector = "#post-"+(img_num)+" > div > div > div.ast-blog-featured-section.post-thumb.ast-col-md-12 > div > a > img"
element = driver.find_element(By.CSS_SELECTOR, selector)
element.click()

# 이미지 페이지가 로드될 때까지 기다립니다.
time.sleep(5)

# 특정 이미지의 원본 URL을 추출합니다.
image_element = driver.find_element(By.CSS_SELECTOR, ".elementor-image img")
image_url = image_element.get_attribute('src')

# 이미지 URL을 Base64로 인코딩한 후 디코딩합니다.
cloaked_url = cloak_url(image_url)
cloaked_url = base64.b64decode(cloaked_url).decode('utf-8')

# 페이지의 특정 섹션에서 텍스트 콘텐츠를 추출합니다.
totals = driver.find_elements(By.CSS_SELECTOR, ".elementor-text-editor.elementor-clearfix")
searchList = []
for i in totals[:4]:
    searchList.append(i.text)

# 디코딩된 이미지 URL을 목록에 추가합니다.
searchList.append(cloaked_url)
print(searchList)

# 지연 후 브라우저를 닫습니다.
time.sleep(10)
driver.quit()

# 수집된 데이터를 DataFrame으로 변환합니다.
df = pd.DataFrame({search: searchList})

# 데이터가 제대로 입력되었는지 DataFrame을 출력하여 확인합니다.
print(df)

# 원하는 구조를 위해 DataFrame을 전치합니다.
transposed_df = df.transpose()

# DataFrame을 엑셀 파일로 저장합니다.
filename = f"{img_num}.xlsx"
transposed_df.to_excel(filename, index=True, header=False, engine='xlsxwriter')

# 엑셀 파일이 저장되었음을 사용자에게 알립니다.
print(f'{filename} 저장되었습니다!')
