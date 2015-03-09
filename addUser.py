"""Import Bookmarks.

Usage:
    addUser.py (USERNAME)
"""

from docopt import docopt
from massive.models import Users
from massive import bcrypt

if __name__ == '__main__':
    arguments = docopt(__doc__)

    passwd = input("Enter password: ")
    user = Users(
        login=arguments['USERNAME'],
        password=bcrypt.generate_password_hash(passwd))
    user.save()
    print("user %s saved" % user.login)
