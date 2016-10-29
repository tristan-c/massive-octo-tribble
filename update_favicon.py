import json

from docopt import docopt
from massive.models import Links
from massive.views import save_link
from massive.utils import get_page_favicon
from pony.orm import db_session,select

if __name__ == '__main__':
    #arguments = docopt(__doc__)

    with db_session:
        links = select(l for l in Links)
        for link in links:
            favicon = get_page_favicon(link.url)
            if favicon:
                link.favicon = favicon
