from crawler import get_html


def test_correct_get_html():
    html = get_html('http://comic.naver.com/webtoon/weekday.nhn')
    assert str(html).startswith('<!DOCTYPE html>')
    assert str(html).endswith('</html>\n')
