# qr-code-task

### Setup

Clone the repository:
```sh
$ git clone https://github.com/IslombekOrifov/qr-code-task.git
$ cd qr-code-task
```

Create a virtual environment for bot:
```sh
$ cd bot
$ python -m venv env
$ source env/bin/activate
```

Create a virtual environment for admin:
```sh
$ python -m venv env
$ source env/bin/activate
```

Install the dependencies for bot:
```sh
(env)$ pip install -r requirements.txt
```

Install the dependencies for admin:
```sh
(env)$ pip install -r requirements.txt
```

Download ngrok and run after that set create env
```sh
(env)$ 
```

In the root of the project create a .env file and set the environment variables
```sh
# Environment
ENVIRONMENT = 'production'

# Django Secret Key
SECRET_KEY = 

# Database configs
ADMINS =  # example 8596841,18496223,645441
BOT_TOKEN = # example 6363356505:AAFqSXkt2VJfd
ip = # example localhost
SERVER_IP = # example https://3962-80-80-212-48.ngrok-free.app

DB_NAME =
DB_USER =
DB_PASS =
DB_HOST =

Migrate database:
```sh
(env)$ python manage.py migrate
```

Create superuser:
```sh
(env)$ python manage.py createsuperuser
```

Run admin:
```sh
(env)$ python manage.py runserver
```

Run bot:
```sh
(env)$ python app.py
```
