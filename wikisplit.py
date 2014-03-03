# -*- coding: utf-8 -*-

######################################################################
## Filename:      wikisplit.py
## Copyright:     2014, Zhicong Chen
## Version:       
## Author:        Zhicong Chen <zhicong.chen@changecong.com>
## Created at:    Fri Feb 21 23:21:17 2014
## Modified at:   Mon Mar  3 16:35:26 2014
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
        self.__category = []

        self.__author_stop_words = [
            "novel", "biographical novel", "debut novel", "book", "american novel", "novella",
            "historical novel|historical fiction", "natural history|naturalist"
            "united states|american", "united states", 
            "african-american", "filipino-american", 
            "writer",
            "Southern literature|Southern",
            "preserve and protect#come nineveh, come tyre",
            "anti-war", "world war", "world war i", "world war ii",
            "propaganda", "various", "various"
            ]

        if not content:
            raise wiki.WikiError("No content is given!")

        '''
        pre-precess of the wiki text
        '''

        self.__content = self.__pre_process(content)

        # get book's info
        self.__get_infobox_book()

        # check if all flieds contains
        if not self.__book.has_key('author'):
            
            # try to get info form the brief introduction
            brief_intro = self.__first_paragraph(self.__content)
            authors = self.__get_authors_from_content(brief_intro)
            self.__book['author'] = authors

        if not self.__book.has_key('release_date') and not self.__book.has_key('pub_date'):
            # try to get info form the brief introduction
            brief_intro = self.__first_paragraph(self.__content)
            self.__book['release_date'] = self.year(brief_intro)


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

    def year(self, date=False):
        if not date:
            # raise wiki.WikiError("No year is given!")       
            return ""

        p_year = re.compile('(19|20)\d{2}')  # 1900 - 

        year = p_year.search(date)

        if not year:
            return ""  # not NA
        else:
            return year.group() 

    def category(self, categories=False):
        '''
        generate a dict of categories
        '''
        if not categories:
            raise wiki.WikiError("No content is given!")       

        '''
        categories from wikitools are in a list with a format of
        ['category:xxxxx', ...]
        '''
        for category in categories:
            p_category = re.compile('[^\[category:|^\[Category:]([^\]]*)')
            category = p_category.search(category).group().strip()

            self.__category.append(category)

        return self.__category

    def authors(self, authors=''): 

        authors = re.sub(r'\(.*\)', '', authors)
        authors = re.sub(r'with', '', authors)
        # authors = re.sub(r'\&', '', authors)

        # print authors

        return re.split('\||\<br\s*\/?\>|,|\&| and |#', authors)

    def cleanup(self, string=False):

        if not string:
            raise wiki.WikiError("No string is given!")

        # remove all <> {} [] ()

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

            book_info = self.__get_infobox_book_template(pos=book_infobox.start())
            book_info = book_info.lstrip('\{').rstrip('\}').strip()

            # print book_info
            
            # patten1 = re.compile('\n(.[^{]+)\n')
            # patten1 = re.compile('\{\{[Ii]nfobox [Bb]ook\s*\|?\s*\n?')
            patten1 = re.compile('[Ii]nfobox [Bb]ook\s*\|?\s*\n?')
            # patten2 = re.compile('\n?}}')
            
            '''
            use findall to get the string within ( )
            '''
            book_info = patten1.sub('', book_info)
            # book_info = patten2.sub('', book_info)

            if book_info:

                # print book_info

                # book_info_str = book_info
                # remove two \n
                # print book_info_str
                # split book info and store into dict
                self.__split_book_info(book_info)
            else:
                raise wiki.WikiError("No book info is found!")

    def __get_infobox_book_template(self, pos=0):

        '''
        this function finds {{}} pair with nest        
        '''
        content = self.__content

        if not content:
            raise wiki.WikiError("No string is given!")

        result = ''
        end = 0

        stack = []
        pushed = False
        for i in range(len(content)):
            if i > pos:
                # if {{ push to stack
                if content[i] == '{' and content[i-1] == '{':
                    pushed = True
                    stack.append(1)
                if content[i] == '}' and content[i-1] == '}':
                    stack.pop()
                
                if pushed:
                    # check validity
                    if len(stack) == 0:
                        end = i
                        break

        return content[pos:end+1].strip()

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
            # val = key_value[1].strip().lstrip('[').rstrip(']')
            val = key_value[1].strip()
            # reomve [[]]
            val = re.sub(r'\[|\]', '', val)

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

    def __first_paragraph(self, content=False):

        # remove [[Category:]]
        p_category = re.compile('\[\[Category:.*]]')  # category
        content = p_category.sub('', content)
        
        # remove comments
        p_comments = re.compile('\<!--[^\>]*--\>')
        content = p_comments.sub('', content)

        # content = re.sub(r'^\n|\n+(?=\n)|\n$', r'', content)        

        # remove templates
        p_template = re.compile('\{{2,}[^\{\}]+\}{2,}')
        content = p_template.sub('', content)
     
        content = p_template.sub('', content)

        # remove images
        p_image = re.compile('\[\[Image:.*]]')
        content = p_image.sub('', content)

        content = content.strip('\n ')

        # print content
        

        # get the first line
        first_line = re.split(r'\n', content)[0]

        return first_line

        
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

        return content.strip('\n ')

    def __get_authors_from_content(self, intro):

        # find all external links in the intro 
        external_links = re.findall(r'\[\[[^\[\]]*\]\]', intro)
        
        for link in external_links:
            
            # print link

            link = re.sub(r'[\[\]\{\}]', '', link)

            # not in the stop words
            if str.lower(link) not in self.__author_stop_words:

                # not contain numbers
                if not re.match(r'.*(\d+|author|novel|fiction|literature|united states|american|new york|florida|chicago|preserve|protect)', str.lower(link)):
                
                    return link
        
        
        return ""

