"""Import Users and links from old massive version using mongoDB.

Usage:
    mongoToSqlite.py [(<links_path> <users_path>)]
"""

import json

from docopt import docopt
from massive import db, models
from massive.views import save_link
from pony.orm import db_session


if __name__ == '__main__':
    arguments = docopt(__doc__)

    list_users = {}

    with open(arguments['<users_path>']) as users_file:
        for file_line in users_file:

            line = json.loads(file_line)

            with db_session:
                user = models.Users.get(login=line["login"])

                if not user:
                    user = models.Users(
                        login=line["login"],
                        password=line["password"])

                list_users[line["_id"]["$oid"]] = user

    with open(arguments['<links_path>']) as links_file:
        for file_line in links_file:
            
            line = json.loads(file_line)

            with db_session:
                link = models.Users.get(url=line["url"])

                if not link:
                    save_link(
                            line.get("title",None),
                            line.get("url",None),
                            line.get("tags",None),
                            None,
                            list_users[line["user"]["$oid"]]
                            )


