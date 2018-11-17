# etoya

## Python version

This project was created with Python 3.7

## Virtual environment

This project uses pipenv. Run `pipenv install` and `pipenv shell` to install all dependencies and activate virtualenv related to this project, respectively.

All further instructions will assume that you've done that and dealth with all problems that arisen.

## Django

Run `python manage.py runserver` to launch an internal Django web-server (don't use it in production). Please mind the console output: you may need to run `python manage.py migrade` to run pending database migrations first. Then you'll be able to see the server running at `localhost:8000`.

## URLs

- */* -- root, implemented in `posts/views.py`
- *admin* - admin panel, used to modify site content. On a fresh database, also run `python manage.py createsuperuser` if you want to access admin panel.

## Project structure

- *manage.py* -- default Django entry point
- *Pipfile* -- for pipenv
- *Pipfile.lock* -- for pipenv
- *db.sqlite3* -- automatically created by Django for local testing, ignored by git
- *.gitignore* - git ignore file
- *.idea* -- Pycharm IDE folder
- *etoya* -- Django main project folder
- *posts* -- Django posts app folder

## Deployment checklist

- [ ] Go through *etoya/settings.py*
