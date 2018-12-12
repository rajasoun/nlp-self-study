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



def check_url(url: str) -> str:
    r = requests.get(url, timeout=5)
    print(r.status_code)
    return r.status_code


if __name__ == '__main__':
    url = input()
    try:
        if check_url(url) == 200:
            extract_article(url)
    except (requests.exceptions.ConnectionError, newspaper.article.ArticleException) as e:
        pass
