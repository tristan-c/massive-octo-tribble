#!flask/bin/python
from massive import app

app.run(debug=True, port=7777, host="0.0.0.0")
