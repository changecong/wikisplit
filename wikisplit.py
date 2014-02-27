# -*- coding: utf-8 -*-

######################################################################
## Filename:      wikisplit.py
## Copyright:     2014, Zhicong Chen
## Version:       
## Author:        Zhicong Chen <zhicong.chen@changecong.com>
## Created at:    Fri Feb 21 23:21:17 2014
## Modified at:   Thu Feb 27 11:03:28 2014
## Modified by:   Zhicong Chen <zhicong.chen@changecong.com>
## Status:        Experimental, do not distribute.
## Description:   A simple module to split the content that return by
##                getWikiText() of wikitools
##
#####################################################################

from wikitools import wiki
import re

class Split:

    def __init__(self, content=False):

        '''
        content [in] returned string value comes from getWikiText()
        '''

        self.__content = ''
        self.__book = {}
        self.__text = ''
        self.__category = {}

        if not content:
            raise wiki.WikiError("No content is given!")

        '''
        pre-precess of the wiki text
        '''

        self.__content = self.__pre_process(content)

        # get book's info
        self.__get_infobox_book()

        # get text of the wiki page
        self.__get_text()


    def book(self):
        '''
        return a dictionary of book's info
        '''
        return self.__book
        
    def text(self):
        '''
        return the text part
        '''
        return self.__text

    def category(self, category=False):
        '''
        generate a dict of categories
        '''
        if not category:
            raise wiki.WikiError("No content is given!")       

        
        

        return self.__category

    def __pre_process(self, content=False):
        
        p_comment = re.compile('<!--[^>]*-->')  # comments
        content = p_comment.sub('', content)

        p_file = re.compile('\[\[File:.*]]\n')  # [[File:]]
        content = p_file.sub('', content)

        return content

    def __get_infobox_book(self):
        '''
        get the template {{infobox_book}}
        '''
        # print self.__content

        patten0 = re.compile('\{\{[Ii]nfobox [Bb]ook([^}]*)}}')
        book_infobox = patten0.search(self.__content)

        # TODO need a stronger condition to ignore pages
        if not book_infobox or len(book_infobox.group()) < 18:

            # TODO need to return an empty book info
            #      instead of report an error
            # raise wiki.WikiError("No book infobox is found!")
            error = 'do something'
        else:

            # print book_infobox.group()
            
            # patten1 = re.compile('\n(.[^{]+)\n')
            patten1 = re.compile('\{\{[Ii]nfobox [Bb]ook\s*\|?\s*\n?')
            patten2 = re.compile('\n?}}')
            
            '''
            use findall to get the string within ( )
            '''
            # book_info = patten1.findall(book_infobox.group())[0]
            book_info = patten1.sub('', book_infobox.group())
            book_info = patten2.sub('', book_info)

            if book_info:

                # print book_info

                # book_info_str = book_info
                # remove two \n
                # print book_info_str
                # split book info and store into dict
                self.__split_book_info(book_info)
            else:
                raise wiki.WikiError("No book info is found!")

    def __split_book_info(self, string=False):
        
        if not string:
            raise wiki.WikiError("No book info is given!")

        # print string

        pairs = re.split('\n', string)

        # delete the first element whitch is a ''
        # del pairs[0]

        for pair in pairs:

            # a simple way to skip the invalid pair
            if len(pair) < 2:
                break


            # print pair
            '''
            each element looks like:
            "name          = The 19th Wife\n"
            '''
            
            # split by '=' & '\'
            key_value = re.split('=', pair)
            # print key_value

            if len(key_value) < 2:
                # split 
                key_value = self.__split_by_space(key_value[0])

            key = key_value[0].strip().lstrip('\|').strip()
            val = key_value[1].strip().lstrip('[').rstrip(']')

            if len(key) == 0 and len(val) == 0:
                continue
            else:
                self.__book[str.lower(key)] = val


    def __split_by_space(self, string):
        
        string = string.strip().lstrip('\|').strip()

        # print string

        pattern0 = re.compile('\w+\s')
        
        try:
            key = pattern0.match(string).group().strip()
        
            pattern1 = re.compile(key)
            value = pattern1.sub('', string).strip()
        except:
            key = ''
            value = ''
        return [key, value]

    def __get_text(self):
        
        '''
        get the text part of the wiki page
        '''
        # print self.__content

        self.__text = self.__text_only(self.__content)

        
    def __text_only(self, content=False):

        # remove [[Category:]]
        p_category = re.compile('\[\[Category:.*]]')  # category
        content = p_category.sub('', content)
        
        # remove {}
        # p_braces = re.compile('\{}')
        # content = p_braces.sub('', content)

        # remove templates
        p_template = re.compile('\{{2,}[^\{}]*}{2,}')
        content = p_template.sub('', content)

        content = p_template.sub('', content)

        # remove external links
        # TODO need a more acurate pattern
        p_external_links = re.compile('\*.*\n')
        content = p_external_links.sub('', content)

        # remove images
        p_image = re.compile('\[\[Image:.*]]')
        content = p_image.sub('', content)

        # remove header
        p_header = re.compile('={2,}')
        content = p_header.sub('', content)

        # remove bold
        p_bold = re.compile('\'{2,}')
        content = p_bold.sub('', content)

        # remove [[]]
        p_internal_links = re.compile('[\[\]]{2,}')
        content = p_internal_links.sub('', content)

        # remove reference
        p_reference_left = re.compile('<[^>]*>')
        p_reference_right = re.compile('</[^>]*>')

        content = p_reference_left.sub('', content)
        content = p_reference_right.sub('', content)

        return content.strip('\n')
