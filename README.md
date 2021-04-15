## Install Django within a Virtual Environment
For better flexibility, we will install Django and all of its dependencies within a Python virtual environment.

You can get the virtualenv package that allows you to create these environments by typing:
```
sudo pip install virtualenv
```
Move into the project directory afterwards:
```
mkdir ~/trail-assignment
cd ~/trail-assignment
```
We can create a virtual environment to store our Django project’s Python requirements by typing:
```
virtualenv env
```
This will install a local copy of Python and pip into a directory called myprojectenv within your project directory.

Before we install applications within the virtual environment, we need to activate it. You can do so by typing:
```
source env/bin/activate
```
Your prompt will change to indicate that you are now operating within the virtual environment. It will look something like this 
```
(env)user@host:~/trail-assignment$.
```
Once your virtual environment is active, you can install Django with pip. We will also install the psycopg2 package that will allow us to use the database we configured:
```
pip install -r requirements.txt
```
We can now start a Django server within our myproject directory. 
```
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver
```

## Frontend repo setup
Node js installation
```
curl -sL https://deb.nodesource.com/setup_8.x -o nodesource_setup.sh
sudo bash nodesource_setup.sh
sudo apt install nodejs
```

Install the node libraries 
```
cd /trail-assignment/src/frontend/
npm install
npm run build
```
This will create a build folder inside the frontend application.
```
/trail-assignment/src/frontend/build
```
We have added this build in Django settings app so if this file is in this exact position We don't need to change anything else

## Serving React APP with Django

We need to add configuration ofr react static files in settings.py. Then a view to render the React page and a URL config to display the view is needed, bith of these can be added to the project directory where the settings.py is located.

First add the path to React build drectory in Djnago settings.py inside the project diretory

```
REACT_APP_DIR = os.path.join(BASE_DIR, "src/frontend")
STATICFILES_DIRS = [
    os.path.join(REACT_APP_DIR, "build", "static"),
]
```
Now we can create a views.py in Django project directory and add this code
```
import os
import logging
from django.conf import settings
from django.http import HttpResponse

index_file_path = os.path.join(settings.REACT_APP_DIR, "build", "index.html")


def react(request):
    """
    A view to serve the react app by reading the index.html from the
    build  react app and serving it as a Httpresponse.
    """
    try:
        with open(index_file_path) as f:
            return HttpResponse(f.read())
    except FileNotFoundError:
        logging.exception("Production build of app not found")
```

Now inside urls.py in project directory add the URL for this view

```
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    # path for user urls,
    # path for sales urls,
    re_path(r"^.*$", views.react, name="home"),
]

```
