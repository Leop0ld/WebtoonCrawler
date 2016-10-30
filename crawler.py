from bs4 import BeautifulSoup
import requests
import re
import sys
import time
from lxml import html

BASE_URL = 'http://comic.naver.com'
WEBTOON_LIST_URL = 'http://comic.naver.com/webtoon/weekday.nhn'
DETAIL_WEBTOON_URL = 'http://comic.naver.com/webtoon/list.nhn?titleId='

today = time.localtime()

header = {
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    'Accept': 'image/webp,image/*,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4,zh-CN;q=0.2,zh;q=0.2',
}


def get_html(url, headers=None):
    """
    :param url: get 요청을 보낼 url
    :param headers: get 요청에 사용될 header
    :return html: BeautifulSoup으로 get 요청에 대한 html 값을 파싱해서 반환한다
    """
    response = requests.get(url, headers=headers)
    decode_text = response.text.encode(response.encoding)
    html = BeautifulSoup(decode_text, "lxml")
    return str(html)


def search_weekday(html_str):
    """
    :param html_str: bs4로 파싱된 html의 string을 받는다
    :return result: 무슨 요일 웹툰인지 확인하기 위해 요일을 반환한다(e.g. 월요 웹툰)
    """
    tree = html.fromstring(html_str)
    result = tree.xpath('//*[@id="content"]/div[3]/div[@class="col col_selected"]/div/h4/span/text()')[0]
    return result


def search_today_webtoon_list(html_str):
    """
    :param html_str: bs4로 파싱된 html의 string을 받는다
    :return result: 오늘의 웹툰 리스트를 result에 담아서 list 형태로 반환한다
    """
    tree = html.fromstring(html_str)
    result = tree.xpath('//*[@id="content"]/div[3]/div[@class="col col_selected"]/div/ul/li/a')
    return result


def download_webtoon(webtoon_id):
    """
    :param webtoon_id: webtoon의 id를 받는다
    :return 은 하지 않고 webtoon의 최신 날짜의 것을 다운로드한다
    """
    url = DETAIL_WEBTOON_URL + webtoon_id
    response = get_html(url)
    tree = html.fromstring(response)
    a_list = tree.xpath('//*[@id="content"]/table/tr')
    detail_url = a_list[2][1][0].attrib['href']

    detail_webtoon_html = get_html(BASE_URL+detail_url)
    image_tree = html.fromstring(detail_webtoon_html)

    # Webtoon Image list
    image_list = image_tree.xpath('//*[@alt="comic content"]')
    index = 1
    for image in image_list:
        # download_image(image.attrib['src'], str(index)+'.jpg', 'webtoon/')
        index += 1

    pass


def download_image(img_url, file_name, file_path=''):
    """
    :param img_url: img를 가져올 url을 지정한다
    :param file_name: file을 어떤 이름으로 저장할 것인지 지정한다
    :param file_path: default 값은 python 파일이 위치한 곳이지만 다른 곳에 다운받고 싶을 경우 지정하면 된다
    :return 하지 않고 요청한 url에 있는 image를 다운받는다
    """
    with open(file_path+file_name, "wb") as f:
        print("Downloading %s" % file_name)
        response = requests.get(img_url, headers=header, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None:  # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("[%s%s]\n" % ('=' * done, ' ' * (50 - done)))
                time.sleep(0.5)
                sys.stdout.flush()


html_content = get_html(WEBTOON_LIST_URL)
today_webtoon_list = search_today_webtoon_list(html_content)
weekday = search_weekday(html_content)

# download_webtoon('675823')
