from urllib.request import urlopen
from PIL import Image
from io import BytesIO
from massive.models import *
from bs4 import BeautifulSoup

def getPageFavicon(url, iconUri=None):
    page = None
    if iconUri:
        try:
            page = urlopen(iconUri)
        except:
            page = None

    if not page:
        page = urlopen("http://getfavicon.appspot.com/%s" % url)

    i = BytesIO(page.read())

    if i:
        image = BytesIO()
        Image.open(i).save(image, "PNG")
        image.seek(0)
        fav = Favicon()
        fav.image.put(image)
        fav.save()
        return fav
    else:
        return None

def getPageTitle(url):
        page = urlopen(url)
        text = page.read()
        page.close()
        soup = BeautifulSoup(text)

        for x in soup.findAll('title'):
            if x.string:
                return x.string

        return None
