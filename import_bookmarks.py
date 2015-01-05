"""Import Bookmarks.

Usage:
    manage_bookmarks.py [-f FILE] [-p | --populate] (user)
    manage_bookmarks.py (-h | --help)


Arguments:
    -h --help       show this
    -f --file       the bookmark file to import (html format)
    -p --populate   fetch additionnal information (title, favicon)
"""

from docopt import docopt
from massive.views import saveLink
from massive.models import *
from bs4 import BeautifulSoup
from massive.utils import *
import re


regex = re.compile('(?:http|ftp|https)://')

def populateInformation():
    for link in Links.objects():
        try:
            if not link.title:
                page = urlopen(link.url)
                text = page.read()
                page.close()
                soup = BeautifulSoup(text)

                for x in soup.findAll('title'):
                    if x.string:
                        link.title = x.string
                        print(link.title)
                        link.save()
        except Exception as e:
            print(e)
            pass

if __name__ == '__main__':
    arguments = docopt(__doc__)

    file = open(arguments['FILE'], 'rb')

    soup = BeautifulSoup(file.read())

    try:
        user = Users.objects.get(login=arguments['login'])
    except:
        print("User not found")
        return

    for td in soup.find_all('dt')[::-1]:
        url = td.a.get('href')
        if regex.match(url):
            if len(Links.objects(url=url)) != 0:
                print("%s : already in db" % url)
                
            saveLink(
                td.a.text,
                url,
                favicon= getPageFavicon(url, iconUri=td.a.get('icon_uri')),
                user = user
            )



