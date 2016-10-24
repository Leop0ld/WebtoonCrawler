from crawler import get_html, BASE_URL, search_today_webtoon_list, search_weekday

import time


def test_correct_get_html():
    html = get_html(BASE_URL)
    assert str(html).startswith('<!DOCTYPE html>')
    assert str(html).endswith('</html>\n')


def test_correct_return_today_webtoon():
    html = get_html(BASE_URL)
    today_webtoon_list = search_today_webtoon_list(str(html))
    assert len(today_webtoon_list)


def test_correct_weekday():
    today = time.localtime()
    week = ('월', '화', '수', '목', '금', '토', '일')

    html = get_html(BASE_URL)
    weekday = search_weekday(str(html))
    assert weekday == week[today.tm_wday] + '요 웹툰'
