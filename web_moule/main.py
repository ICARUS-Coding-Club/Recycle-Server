from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

from web_moule.create_driver import create_driver


def get_naver_news_titles_and_contents(driver, url):
    driver.get(url)

    news_links = []

    # "네이버뉴스"로 표시된 뉴스 링크를 모두 수집
    all_links = driver.find_elements(By.CSS_SELECTOR, '.news .type01 li .info_group a.info')
    for link in all_links:
        if '네이버뉴스' in link.text:
            news_links.append(link.get_attribute('href'))

    news_data = []

    for link in news_links:
        driver.get(link)
        time.sleep(2)  # 페이지 로딩 대기

        try:
            # 본문 제목과 내용을 크롤링
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            title = soup.select_one('#articleTitle').text
            content = soup.select_one('#articleBodyContents').text
            news_data.append((title, content))
        except:
            pass

    return news_data


def main():
    # 본인의 환경에 맞게 경로 수정
    driver = create_driver()
    browser = webdriver.Chrome(driver)

    url = "https://search.naver.com/search.naver?where=news&sm=tab_jum&query=재활용+환경"

    news_list = get_naver_news_titles_and_contents(browser, url)
    for title, content in news_list:
        print("Title:", title)
        print("Content:", content)
        print("=" * 50)

    browser.quit()


if __name__ == "__main__":
    main()
