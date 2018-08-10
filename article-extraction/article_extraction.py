#!/usr/bin/env python3

#pip3 install newspaper3k --user
import sys
from newspaper import Article

def extract_article(url):
 
    article = Article(url)
 
    #1 . Download the article
    article.download()
 
    #2. Parse the article
    article.parse()
 
    #3. Fetch Author Name(s)
    print(article.authors)
 
    #4. Fetch Publication Date
    print('Article Publication Date:')
    print(article.publish_date)
    
    #5. The URL of the Major Image
    print('Major Image in the article:')
    print(article.top_image)
 
    #6. Natural Language Processing on Article to fetch Keywords
    article.nlp()
    print ('Keywords in the article')
    print(article.keywords)
 
    #7. Generate Summary of the article
    print('Article Summary')
    print(article.summary)
    
    print('Full Text')
    print(article.text)
    




if __name__ == '__main__':
    url = input()
    extract_article(url)
