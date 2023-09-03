import time
import csv
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from modules.create_driver import create_driver
from modules.url_ascii_helper import PercentStrHelper
from modules.execute_infinite_scrolling import execute_scrolling
from Trash import Trash

news_url = r'https://search.naver.com/search.naver?where=news&sm=tab_jum&query=/'

category_list = ["일반쓰레기",
                 "대형생활폐기물",
                 "음식물쓰레기",
                 "의류수거함",
                 "플라스틱",
                 "유리",
                 "형광등-전용-수거함",
                 "불연성쓰레기",
                 "캔류",
                 "비닐류"]

test_category_list = ["일반쓰레기"]


def main():
    driver = create_driver()

    for category in category_list:
        detail_items = []

        try:
            # 카테고리별 쓰레기 백과사전 링크 접속
            driver.get(news_url + PercentStrHelper.percent_decode(category) + '/')


            # rel 의 book mark 속성을 가진 a 태그를 전부 저장
            a_tags = driver.find_elements(By.CSS_SELECTOR, 'a[rel="bookmark"]')

            # 각각의 쓰레기의 자세히 보기 링크를 set에 저장
            for tag in a_tags:
                item_name = tag.text
                item_url = tag.get_attribute('href')
                detail_items.append({'name': item_name, 'url': item_url})

            # 개별 쓰레기 정보 파싱
            for item in detail_items:
                # 개별 쓰레기 정보를 request
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                                  "Chrome/91.0.4472.124 Safari/537.36"
                }
                response = requests.get(item['url'], headers=headers)
                soup = BeautifulSoup(response.content, 'html.parser')

                time.sleep(1)

                # 두 번째 'elementor-text-editor elementor-clearfix' 클래스를 가진 div를 찾습니다.
                elementor_clearfix_tag = soup.select('.elementor-text-editor.elementor-clearfix')[1]

                # h6 태그가 존재하는지 확인합니다.
                if elementor_clearfix_tag.find('h6'):
                    item_tag = elementor_clearfix_tag.find('h6').text
                # strong 태그가 존재하는지 확인합니다.
                elif elementor_clearfix_tag.find('strong'):
                    item_tag = elementor_clearfix_tag.find('strong').text
                else:
                    item_tag = "태그 정보 없음"

                # 모든 p 태그의 텍스트를 찾습니다.
                p_tags = elementor_clearfix_tag.find_all('p')

                # 첫 번째 p 태그는 재활용 가능 여부에 대한 정보를 가집니다.
                item_recyclable = p_tags[0].text if p_tags else "재활용 정보 없음"
                if "재활용" not in item_recyclable:
                    item_recyclable = "데이터 수정 필요"

                # 두 번째 p 태그는 분류에 대한 정보를 가집니다.
                item_category = p_tags[1].text if len(p_tags) > 1 else "분류 정보 없음"

                if "재활용: 불가능" in item_category:
                    print(f"분류: {category}")
                elif "재활용: 가능" in item_category:
                    print(f"분류: {category}")

                # 세 번째 'elementor-text-editor elementor-clearfix' 클래스를 가진 div를 찾습니다.
                elementor_clearfix_tag = soup.select('.elementor-text-editor.elementor-clearfix')[2]

                # 버리는 방법
                p_tags = elementor_clearfix_tag.find_all('p')

                item_disposal_method = []

                for p in p_tags:
                    item_disposal_method.append(p.text)

                # 네 번째 'elementor-text-editor elementor-clearfix' 클래스를 가진 div를 찾습니다.
                elementor_clearfix_tag = soup.select('.elementor-text-editor.elementor-clearfix')[3]
                p_tags = elementor_clearfix_tag.find_all('p')

                item_additional_info = []
                if len(p_tags) >= 1:
                    for p in p_tags:
                        item_additional_info.append(p.text)
                else:
                    item_additional_info.append(elementor_clearfix_tag.text)

                image_div_tag = soup.select('.elementor-image')[0]
                img_tag = image_div_tag.find('img')
                item_url = img_tag['src']

                trash_item = Trash(item['name'],
                                   item_tag,
                                   item_recyclable,
                                   item_category,
                                   item_disposal_method,
                                   item_additional_info,
                                   item_url)

                print(f"Item name: {item['name']}")
                print(f"Item Tag: {item_tag}")
                print(f"Item Recyclable: {item_recyclable}")
                print(f"Item Category: {item_category}")
                print(f"Item disposal method: {item_disposal_method}")
                print(f"Item additional info: {item_additional_info}")
                print(f"Item Image Url: {item_url}")

                detail_items.append(trash_item)
                time.sleep(1)

        except Exception as e:
            print(e, end='\n')
            print("자동으로 다음 카테고리로 넘어갑니다.")

        with open(f'{category}_trash_data.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['name', 'tags', 'recyclable', 'categories', 'disposal_method', 'additional_info', 'image_url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()  # 헤더 작성
            for trash_item in detail_items:
                if isinstance(trash_item, Trash):
                    writer.writerow({
                        'name': trash_item.name,
                        'tags': trash_item.tags,
                        'recyclable': trash_item.recyclable,
                        'categories': trash_item.categories,
                        'disposal_method': '|'.join(trash_item.disposal_method),
                        'additional_info': '|'.join(trash_item.additional_info),
                        'image_url': trash_item.image_url
                    })


if __name__ == "__main__":
    main()
