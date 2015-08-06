"""Import Bookmarks.

Usage:
    manage_bookmarks.py FILE LOGIN
    manage_bookmarks.py -h | --help


Arguments:
    -h --help           Show help
"""

import re
import sys

from docopt import docopt
from bs4 import BeautifulSoup

from massive.views import save_link
from massive.models import *
from massive.utils import *

from pony.orm import db_session

regex = re.compile('(?:http|ftp|https)://')

@db_session
def populateInformation():
    for link in Links.select():
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
                commit()
        except Exception as e:
            print(e)
            pass

if __name__ == '__main__':
    arguments = docopt(__doc__)

    file = open(arguments['FILE'], 'rb')

    soup = BeautifulSoup(file.read())

    try:
        user = Users.objects.get(login=arguments['LOGIN'])
    except Exception as e:
        print(e)
        sys.exit()

    for td in soup.find_all('dt')[::-1]:
        url = td.a.get('href')
        if regex.match(url):
            if len(Links.objects(url=url)) != 0:
                print("%s : already in db" % url)

            save_link(
                td.a.text,
                url,
                favicon=getPageFavicon(url, iconUri=td.a.get('icon_uri')),
                user=user
            )
