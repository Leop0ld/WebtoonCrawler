from crawler.crawler import get_html, search_today_webtoon_list, search_weekday, today as crawl_day, \
                            download_webtoon, BASE_URL, WEBTOON_LIST_URL, download_image

import time


def test_today_is_correct():
    assert crawl_day.tm_wday == time.localtime().tm_wday


def test_correct_get_html():
    html = get_html(WEBTOON_LIST_URL)
    assert html.startswith('<!DOCTYPE html>')
    assert html.endswith('</html>\n')


def test_correct_return_today_webtoon():
    html = get_html(WEBTOON_LIST_URL)
    today_webtoon_list = search_today_webtoon_list(html)
    assert len(today_webtoon_list)


def test_correct_weekday():
    week = ('월', '화', '수', '목', '금', '토', '일')
    html = get_html(WEBTOON_LIST_URL)
    weekday = search_weekday(html)
    assert weekday == week[crawl_day.tm_wday] + '요 웹툰'

"""
def test_download_image():
    download_image('https://avatars0.githubusercontent.com/u/12431127?v=3&s=466', 'test.jpg', '../webtoon/')
    with open('../webtoon/test.jpg', 'rb') as f:
        assert f.name
"""
