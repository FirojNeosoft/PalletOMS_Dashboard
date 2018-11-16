from flask_script import Manager
from app import app
# from config import *

# app.config.from_object(DevelopmentConfig())

manager = Manager(app)



if __name__ == '__main__':
    manager.run()
