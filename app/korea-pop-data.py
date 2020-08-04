import django
django.setup()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

import os
import json
import urllib
from urllib.parse import unquote

from tours.models import *


def kpop_crawler_url(kpop_url_list=dict()):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    driver = webdriver.chrome.webdriver.WebDriver(executable_path='../chromedriver', chrome_options=options)
    for num in range(1, 6):

        url = f'https://korean.visitseoul.net/hallyu?curPage={num}&srchType=&srchOptnCode=&srchCtgry=29&sortOrder=&srchWord='
        driver.get(url)
        print(url)

        try:
            article_list = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'article-list-slide'))
            )
            articles = article_list.find_elements_by_tag_name("li")
            for article in articles:
                a_tag = article.find_element_by_tag_name("a")

                title = a_tag.get_attribute('title')
                href = a_tag.get_attribute('href')
                href = urllib.parse.unquote(href)
                thumb = a_tag.find_element_by_class_name('thumb').get_attribute('style')

                kpop_url_list[title] = {
                    'href': href,
                    'thumb': 'https://korean.visitseoul.net/' + thumb.replace('background-image: url("', '').replace(
                        '");', ''),
                }
                print(title)
                print(href)
                print(thumb)

        except Exception as ex:  # 에러 종류
            print('에러가 발생 했습니다', ex)  #
            driver.quit()

    driver.quit()
    return kpop_url_list


def korea_pop_detail_page(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    driver = webdriver.chrome.webdriver.WebDriver(executable_path='../chromedriver', chrome_options=options)
    # url = 'https://korean.visitseoul.net/hallyu/근대역사-골목산책-우리슈퍼-코스_/34204'
    driver.get(url)
    try:
        info_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'infor-element'))
        )
        category_title_selenium = info_element.find_element_by_class_name('h3')
        category_title = category_title_selenium.text
        print(category_title)

        text_area = info_element.find_element_by_class_name('text-area')
        tourist_spots = text_area.find_elements_by_class_name('cnt-blockquote')
        for spot in tourist_spots:
            spot_name = spot.find_element_by_class_name('fc-blue').text
            spot_info = spot.find_elements_by_tag_name('p')
            if '탐방코스' == spot_name:
                continue
            else:
                try:
                    description = '없음'
                    address = '없음'
                    open_hour = '없음'
                    tel = '없음'
                    website = '없음'
                    trans = '없음'
                    for infomation in spot_info:

                        if '주소' in infomation.text:
                            try:
                                address = infomation.text.strip().replace("주소: ", "")
                            except Exception as ex:
                                print('address error', ex)
                        elif '운영시간' in infomation.text:
                            try:
                                open_raw = infomation.text.strip()
                                open_hour = infomation.text.strip().replace("운영시간 :", "").replace("운영시간:", "").replace(
                                    "운영시간", "")
                            except Exception as ex:
                                print('open_hour error', ex)


                        elif '전화번호' in infomation.text or '문의' in infomation.text:

                            try:
                                tel = infomation.text.strip().replace("문의 :", "").replace("문의:", "").replace("전화번호:",
                                                                                                             "").replace(
                                    "전화번호 :", "")
                                tel = re.search('\d{2,3}-\d{3,4}-\d{3,4}', tel)
                                if tel == None:
                                    tel = re.search(' \d{4}-\d{4}', tel)
                                tel = tel.group()
                            except Exception as ex:
                                print('tel error', ex)

                        elif '홈페이지' in infomation.text or '웹사이트' in infomation.text or '웹페이지' in infomation.text:
                            if '웹페이지' in infomation.text:
                                try:
                                    a_tag = infomation.find_element_by_tag_name('a')
                                    href = a_tag.get_attribute('href')
                                    href = urllib.parse.unquote(href)
                                    website = href
                                except Exception as ex:
                                    print('a tag href ::::::', ex)
                            else:
                                try:
                                    website = infomation.text.strip().replace("홈페이지: ", "").replace("웹사이트: ", "")
                                except Exception as ex:
                                    print('website error', ex)

                        elif '교통편' in infomation.text:
                            try:
                                trans = infomation.text.strip().split(':')[1]
                            except Exception as ex:
                                print('trans error', ex)
                        elif len(infomation.text) > 150:
                            try:
                                description = infomation.text
                            except Exception as ex:
                                print('description error', ex)
                        else:
                            text = ''

                except Exception as ex:
                    print('not iteral', ex)
            if '-' in spot_name:
                try:
                    spot_name = spot_name.split('-')[1].replace(" ", '')
                except Exception as ex:
                    print('여기서 나는 건가?', ex)
            print('placename : ', spot_name)
            print('description : ', description)
            print('place address : ', address)
            print('place telphone : ', tel)
            print('place open_hour : ', open_hour)
            print('place website : ', website)
            print('place transportation : ', trans)
            place, _ = Place.objects.get_or_create(
                name=spot_name,
                content=description,
                address=address,
                phone_number=tel,
                open_time=open_hour,
                url=website,
                trans=trans,

            )
            print('models make:::::::::::::::::::: ', place)
            kpopcontent, _ = KPopContent.objects.get_or_create(
                place=place,
                content_type='mu',
                title=category_title,
            )
            print('kpopcontent:::::::::::::::::::: ', kpopcontent)
            print('=========================================================')

    except Exception as ex:  # 에러 종류
        print('에러가 발생 했습니다', ex)  #
        driver.quit()
    driver.quit()


kpop_url_list = kpop_crawler_url()
# print(kpop_url_list)
with open('./k_pop_url_page_fron_1_to_6_0801.json', 'w', encoding='UTF-8') as outfile:
    json.dump(kpop_url_list, outfile, ensure_ascii=False)

# k_pop_url_page_fron_1_to_6
with open('./k_pop_url_page_fron_1_to_6_0801.json', 'r') as file:
    json_data = json.load(file)
for title in json_data:
    url = json_data[title]['href']
    print(url)
    try:
        data = korea_pop_detail_page(url)

    except:
        print('다른 페이지 오류를 어떻게 잡지')


celeb_list = ['강다니엘', '세븐틴', '엑소', '몬스타엑스', '방탄소년단','아미','오마이걸', '규현', '아이즈원', '뉴이스트', 'TXT', '갓세븐', 'NCT', 'BTS', '블랙핑크', '위너', '유노윤호', '산다라박', '이하이', '이수현','워너원','동할배', '빅뱅', '소년24']

profession = 'SINGER'
for name in celeb_list:
    celeb, _ = Celebrity.objects.get_or_create(
        name = name,
        profession = profession,
    )
    
    kpopcontent_list = KPopContent.objects.filter(title__contains=celeb.name)
    for content in kpopcontent_list:
        content.celebrity = celeb
        content.save()
