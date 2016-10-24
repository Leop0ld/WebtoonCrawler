from bs4 import BeautifulSoup
import requests
import re
from lxml import html


BASE_URL = 'http://comic.naver.com/webtoon/weekday.nhn'


def get_html(url, headers=None):
    """
    :param url: get 요청을 보낼 url
    :param headers: get 요청에 사용될 header
    :return html: BeautifulSoup으로 get 요청에 대한 html 값을 파싱해서 반환한다
    """
    response = requests.get(url, headers=headers)
    decode_text = response.text.encode(response.encoding)
    html = BeautifulSoup(decode_text, "lxml")
    return html


def search_weekday(html_str):
    """
    :param html_str: bs4로 파싱된 html의 string을 받는다
    :return result: 무슨 요일 웹툰인지 확인하기 위해 요일을 반환한다(e.g. 월요 웹툰)
    """
    tree = html.fromstring(html_str)
    result = tree.xpath('//*[@id="content"]/div[3]/div[1]/div/h4/span/text()')[0]
    return result


def search_today_webtoon_list(html_str):
    """
    :param html_str: bs4로 파싱된 html의 string을 받는다
    :return result: 오늘의 웹툰 리스트를 result에 담아서 list 형태로 반환한다
    """
    tree = html.fromstring(html_str)
    result = tree.xpath('//*[@id="content"]/div[3]/div[1]/div/ul/li/a/text()')
    return result

html_content = str(get_html(BASE_URL))
today_webtoon_list = search_today_webtoon_list(html_content)
weekday = search_weekday(html_content)
