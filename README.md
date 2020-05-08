# Flask blog

## A basic CRUD appplication

- Personal blog using `flask`, `bootstrap`
- It use `pipenv` to create `virtualenv` and manage dependencies

## Dependencies

- `flask`
- `boostrap`
- `flask-wtf`
- `wtforms`
- `flask-login`
- `flask-mail`
- `flask-bcrypt`
- `flask-script`
- `flask-migrate`
- `flask-admin`
- `python-dotenv`

## How to use?

- First: Run `pipenv run python manage.py db init` or `flask db init`to start initializing migrations database.
- Then: Run `pipenv run python manage.py db migrate` or `flask db migrate` to migrate.
- Run: Run `pipenv run python manage.py db upgrade` or `flask db upgrade` to apply the migrations to the database.
- Finally: Run `pipenv run python manage.py runserver` or `flask run` to run this application locally.
- Or you can deploy to [heroku](https://heroku.com)
