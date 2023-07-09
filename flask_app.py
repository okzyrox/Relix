from .server import app

application = app.flaskApp

if __name__ == "__main__":
    application.run()