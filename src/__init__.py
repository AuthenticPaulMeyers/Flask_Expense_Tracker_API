from flask import Flask, Blueprint
import os
from src.auth import auth
from src.expenses import expenses

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        SECRET_KEY=os.environ.get("SECRET_KEY"),
        
    else:
        app.config.from_mapping(test_config)
    
    # register modules
    app.register_blueprint(auth)
    app.register_blueprint(expenses)
    return app