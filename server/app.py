from flask import Flask

flaskApp = Flask(__name__)

import routes

if __name__ == "__main__":
    flaskApp.run()