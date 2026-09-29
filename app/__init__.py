from flask import Flask
def create_app():
    app=Flask(__name__); app.config['MAX_CONTENT_LENGTH']=32*1024*1024
    from .routes import bp; app.register_blueprint(bp); return app
