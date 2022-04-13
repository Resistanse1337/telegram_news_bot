import requests
from lxml.html import fromstring


def get_html():
    """Возвращает html главной страницы"""
    data = requests.get("https://vc.ru/").text

    return data


def parse_news(data):
    """Возвращает список всех ссылок на новости, их заголовки и краткое описание"""
    root = fromstring(data)

    urls = root.xpath("//a[@class='content-link']/attribute::href")
    titles = root.xpath("//div[@class='content-title content-title--short l-island-a']/text()")
    descriptions = root.xpath("//div[@class='l-island-a']/p/text()")

    return urls, titles, descriptions


def get_last_news():
    """Возвращает первую по списку новость"""
    urls, titles, descriptions = parse_news(get_html())

    return urls[0], titles[0], descriptions[0]


if __name__ == "__main__":
    data = get_html()
    urls, titles, descriptions = parse_news(data)




