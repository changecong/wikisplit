#! /usr/bin/env python   
# -*- coding: utf-8 -*-

######################################################################
## Filename:      wikiexample.py
## Copyright:     2014, Zhicong Chen
## Version:       
## Author:        Zhicong Chen <zhicong.chen@changecong.com>
## Created at:    Thu Feb 27 09:53:29 2014
## Modified at:   Mon Mar  3 22:44:27 2014
## Modified by:   Zhicong Chen <zhicong.chen@changecong.com>
## Status:        Experimental, do not distribute.
## Description:   an example
##
#####################################################################

from wikitools import wiki
from wikitools import page
from wikitools import api
from wikitools import category
import sys 
reload(sys) 
sys.setdefaultencoding('utf8') 

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
total_noval = 0;
total_author = 0;
total_date = 0;
total_title = 0;

# text = open('noval_stat.txt', 'w')
for page in pages:

    book.clear()

    if 0 <= c and c < 1250:

        # get split object
        content = page.getWikiText()
        split = wikisplit.Split(content)    

        '''

        '''    

        # print content
        print c
        book_info = split.book()

        # print book_info

        # book['title'] = book_info.get('name', '')
        # if book['title'] == "" :
        book['title'] = page.title

        if book['title'] != "":
            total_title = total_title + 1
        
        book['author'] = split.authors(book_info.get('author', ''))

        if book['author'] != [""]:
             total_author = total_author + 1

        if book_info.has_key('release_date'):
            book['publication_date'] = split.year(book_info['release_date'])
        elif book_info.has_key('pub_date'):
            book['publication_date'] = split.year(book_info['pub_date'])
        else:
            book['publication_date'] = ''

        if book['publication_date'] != "":
            total_date = total_date + 1

        line = str(c) + " : " + str(book['author']).encode('utf-8') + " : " + book['publication_date'].encode('utf-8') + " : " + book['title'].encode('utf-8')

        # text.write(line + '\n')

        # print split.book()
        # book['categories'] = split.category(page.getCategories())
        
        # book['text'] = split.text()

        # if book['author'] == [""]:
        # print json.dumps(book, indent=4)

    elif c > 1250:
        break

    c = c + 1



print "Total novels : " + str(c-1)
print "Total titles found : " + str(total_title) + " : " + str(total_title/float(c))
print "Total authors found : " + str(total_author) + " : " + str(total_author/float(c))
print "Total dates found : " + str(total_date) + " : " + str(total_date/float(c))

# text.write("Total novels : " + str(c-1) + '\n')
# text.write("Total titles found : " + str(total_title) + " : " + str(total_title/float(c)) + '\n')
# text.write("Total authors found : " + str(total_author) + " : " + str(total_author/float(c)) + '\n')
# text.write("Total dates found : " + str(total_date) + " : " + str(total_date/float(c)) + '\n')


# text.close()
