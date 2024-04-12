from pathlib import 
import os

#settings.pyからそのままコピー
SECRET_KEY = 'django-insecure-*uw3^g!_okd#dv@a2%_jp=dzesx6$p+cj6t+si6au!jm0wfzpp'

BASE_DIR = Path(__file__).resolve().parent.parent

#settings.pyからそのままコピー
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DEBUG = True #ローカルでDebugできるようになります。