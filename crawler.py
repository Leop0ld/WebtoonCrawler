from bs4 import BeautifulSoup
import requests
import lxml


BASE_URL = 'http://comic.naver.com/webtoon/weekday.nhn'


def get_html(url, headers=None):
    response = requests.get(url, headers=headers)
    html_content = response.text.encode(response.encoding)
    html = BeautifulSoup(html_content, "lxml")
    return html

print(get_html(BASE_URL))
