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
