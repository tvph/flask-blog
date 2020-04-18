from blog import create_app  # this file use app.run() so import app here
# flask script to create command
from flask_script import Manager
from flask_migrate import MigrateCommand


# add db command to migrate db
manager = Manager(create_app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    """
    If run app: python manage.py runserver
    If run shell: python manage.py shell
    If migrate database: python manage.py db [sub-command]
    """
    manager.run()
