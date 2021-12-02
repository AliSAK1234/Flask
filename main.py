from flask import Flask
app = Flask(__name__)
from routes.files_attach import *
from models import *

app.config['SECRET_KEY'] = 'FLASK_AUTHENTICATION_SECRET'

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=4444)
