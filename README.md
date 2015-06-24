massive-octo-tribble
====================

import,store et search bookmarks

* Default to SQLite through PonyOrm
* Flask
* bcrypt for passwords encryption

Installation
------------

```bash
git clone https://github.com/tristan-c/massive-octo-tribble && cd massive-octo-tribble
pyvenv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

Then don't forget to add a user:
```bash
python addUser.py
```

Everything is setup, You can open your browser at http://localhost:7777/.

importing bookmarks from firefox/chrome
---------------------------------------
```bash
python import_bookmarks.py /path/to/my/file MyUserName
```
