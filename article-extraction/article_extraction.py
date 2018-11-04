#!/usr/bin/env python3

# pip3 install newspaper3k --user
import requests
import newspaper
from newspaper import Article


def extract_article(url):

    article = Article(url)

    # 1 . Download the article
    article.download()

    # 2. Parse the article
    article.parse()

    print('Full Text')
    print(article.text)

    # 3. Fetch Author Name(s)
    print(article.authors)

    # 4. Fetch Publication Date
    print('Article Publication Date:')
    print(article.publish_date)

    # 5. The URL of the Major Image
    print('Major Image in the article:')
    print(article.top_image)

    # 6. Natural Language Processing on Article to fetch Keywords
    article.nlp()
    print('Keywords in the article')
    print(article.keywords)

    # 7. Generate Summary of the article
    print('Article Summary')
    print(article.summary)


def check_url(url: str) -> str:
    r = requests.get(url, timeout=5)
    print(r.status_code)
    return r.status_code


if __name__ == '__main__':
    urls = tuple(open('course_launch_link.txt', 'r'))
    for url in urls:
        URL = 'http://10.126.100.201' + url.rstrip()
        print(URL)
        try:
            if check_url(URL) == 200:
                extract_article(URL)
        except (requests.exceptions.ConnectionError, newspaper.article.ArticleException) as e:
            pass
