"""Import Bookmarks.

Usage:
    addUser.py (USERNAME)
"""

from docopt import docopt
from massive import bcrypt,db, models
from pony.orm import db_session

if __name__ == '__main__':
    arguments = docopt(__doc__)

    passwd = input("Enter password: ")

    with db_session:
        user = models.Users(
            login=arguments['USERNAME'],
            password=bcrypt.generate_password_hash(passwd))
        print("user %s saved" % user.login)
