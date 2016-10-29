
import os
import urllib

from io import BytesIO
from massive.models import *
from massive import app
from bs4 import BeautifulSoup


def get_page_favicon(url, name):
    final_url = "http://www.google.com/s2/favicons?domain=%s" % url
    file_path = os.path.join(app.config['FAVICON_REPO'], name)
    urllib.request.urlretrieve(final_url, file_path)

def get_page_title(url):
    try:
        req = urllib.request.Request(
            url, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        text = urllib.request.urlopen(req, timeout=3).read()
    except:
        return None
    
    soup = BeautifulSoup(text, "html.parser")

    title = soup.findAll('title')

    if title:
        return title[0].string

    return None
