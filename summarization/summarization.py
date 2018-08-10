#!/usr/bin/env python3

# pip3 install --upgrade gensim newspaper3k 
import sys
from newspaper import Article
from gensim.summarization.summarizer import summarize

def summarize_article(url):
 
    article = Article(url)
 
    #1 . Download the article
    article.download()
 
    #2. Parse the article
    article.parse()
    text = article.text
    article.nlp()

    print('Article Summary From Gensim')
    print(summarize(text))
    
    print('Article Summary From NewsPaper')
    print(article.summary)



if __name__ == '__main__':
    url = input()
    summarize_article(url)
