from utils.CreateAPP import create_app
from flask_script import Manager

manage = Manager(app=create_app())

if __name__ == '__main__':
    manage.run()
