"""
크롬 드라이버 생성 및 설정 모듈
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# 크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager


def create_driver() -> webdriver.Chrome:
    # 크롬 브라우저 꺼짐 방지
    chrome_options = Options()
    chrome_options.add_experimental_option('detach', True)

    # 불필요한 에러 메시지 없애기
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # 디버거 크롬 옵션 추가
    chrome_options.add_argument("remote-debugging-port=9222")
    chrome_options.add_argument("user-data-dir=C:\\selenium\\ChromeProfile")
    extensions_path = [
        r'C:\Users\Juyoung_Laptop\AppData\Local\Google\Chrome\User Data\Default\Extensions\cfhdojbkjhnklbpkdaibdccddilifddb\3.19_0',
        r'C:\Users\Juyoung_Laptop\AppData\Local\Google\Chrome\User Data\Default\Extensions\hapgiopokcmcnjmakciaeaocceodcjdn\6.4_0'
    ]

    chrome_options.add_argument(f'load-extension={",".join(extensions_path)}')

    # 크롬 드라이버 최신 버전 설치
    service = Service(executable_path=ChromeDriverManager().install())

    # 드라이버 객체 생성
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.service = service
    driver.implicitly_wait(10)
    driver.maximize_window()

    return driver

