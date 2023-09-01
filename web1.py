import urllib.request
from bs4 import BeautifulSoup
import json


def get_article(links):
    req = urllib.request.Request(links, headers={'User-Agent': 'Mozilla/5.0'})
    sourcecode = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(sourcecode, "html.parser")

    title = soup.select_one(".media_end_head_headline")
    time_data = soup.select_one(".media_end_head_info_datestamp_time._ARTICLE_DATE_TIME")
    body = soup.select_one(".go_trans._article_content")
    image = soup.select_one("img[src^='https://imgnews.pstatic.net/image/']")

    article_data = {}



    if title:
        article_data['제목'] = title.text
    if time_data:
        article_data['시간'] = time_data.text
    if body:
        article_data['본문'] = body.text
    if image:
        article_data['이미지'] = image['src']

    image_element = soup.find("img", class_="._LAZY_LOADING")
    if image_element and 'src' in image_element.attrs:
        image_src = image_element["src"]
        print(image_src)
    else:
        print("No src found or no matching img element found.")

    #print(article_data)

    return article_data



url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EC%9E%AC%ED%99%9C%EC%9A%A9%20%ED%99%98%EA%B2%BD&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=516&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:all,a:all&start=1"
req = urllib.request.Request(url)
sourcecode = urllib.request.urlopen(req).read()
soup = BeautifulSoup(sourcecode, "html.parser")

articles_list = []

for li in soup.find_all("li", class_="bx"):
    info_group = li.find("div", class_="info_group")
    if info_group:
        navernews_link = info_group.find("a", string="네이버뉴스")
        if navernews_link:
            article_data = get_article(navernews_link["href"])
            if article_data:
                articles_list.append(article_data)

# 리스트를 JSON 형태로 파일에 저장
with open('환경정보.json', 'w', encoding='utf-8') as f:
    json.dump(articles_list, f, ensure_ascii=False, indent=4)
