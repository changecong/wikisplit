######################################################################
## Filename:      wikiexample.py
## Copyright:     2014, Zhicong Chen
## Version:       
## Author:        Zhicong Chen <zhicong.chen@changecong.com>
## Created at:    Thu Feb 27 09:53:29 2014
## Modified at:   Thu Feb 27 20:29:26 2014
## Modified by:   Zhicong Chen <zhicong.chen@changecong.com>
## Status:        Experimental, do not distribute.
## Description:   an example
##
#####################################################################

from wikitools import wiki
from wikitools import page
from wikitools import api
from wikitools import category

# a tool used to split wikitext
import wikisplit

# os
import os

# json
import json

# connect the wiki site
site = wiki.Wiki('http://en.wikipedia.org/w/api.php')

# get the category
category_name = '20th-century American novels'
cat = category.Category(site, category_name)

# get all pages of the category
pages = cat.getAllMembers()

# initial book
book = {}

# for each book page
c = 0;

for page in pages:

    book.clear()

    # get split object
    content = page.getWikiText()
    split = wikisplit.Split(content)    

    '''

    '''

    if c < 10:
        
        book_info = split.book()

        # print book_info

        book['title'] = book_info.get('name', '')
        
        book['author'] = split.authors(book_info.get('author', ''))
        
        if book_info.has_key('release_date'):
            book['publication_date'] = split.year(book_info['release_date'])
        elif book_info.has_key('pub_date'):
            book['publication_date'] = split.year(book_info['pub_date'])
        else:
            book['publication_date'] = ''
            
        # print split.book()
        book['categories'] = split.category(page.getCategories())
        
        book['text'] = split.text()

        print json.dumps(book, indent=4)

    else:
        break

    c = c + 1
