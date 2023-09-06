"""
현재 무한 스크롤 형태로 되어있는 사이트를 가장 최하단으로 스크롤하는 모듈
"""

import time


def execute_scrolling(driver):
    """
    크롬 드라이버를 불러와서 가장 최하단으로 스크롤링하는 메소드
    :param driver: 크롬 드라이버
    :return: 없음
    """
    # before_h = driver.execute_script('return window.scrollY')
    before_h = driver.execute_script("return document.body.scrollHeight")
    while True:
        # 스크롤 내림
        # driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.END)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # 새로운 내용 로딩됐는지 확인
        # after_h = driver.execute_script('return window.scrollY')
        after_h = driver.execute_script("return document.body.scrollHeight")

        # 스크롤링 대기시간
        time.sleep(2)

        if after_h == before_h:
            break

        before_h = after_h
