from wikitools import wiki
from wikitools import page
from wikitools import api
from wikitools import category

import wikisplit

site = wiki.Wiki('http://en.wikipedia.org/w/api.php')

cat = category.Category(site, '20th-century American novels')

pages = cat.getAllMembers()

#print len(pages)
i = 0
for page in pages:
    
    if (i == 97):
        print i
        content = page.getWikiText()
        split = wikisplit.Split(content)
        print split.book()
        print split.text()
    i = i + 1
    if (i > 100):
        break
