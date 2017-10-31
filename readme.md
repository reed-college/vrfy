# Running the server once you have everything installed
See 'Setting up Local Development` to learn how to install everything. Each time you want to run the server, you need to open 4 terminal tabs/windows and run these 4 programs:
### Start Django
  * activate virtualenv and go in to project direcotry (i.e the folder with `manage.py`)
  * `python manage.py gruntserver`

### Start Redis (Used as a message broker with Celery)
  * You don't need to activate the virtualenv or go in to the project directory
  * `redis-server`
  * Test to see if it's up & accepting connections with `redis-cli ping`

### Celery
  * activate virtualenv and go in to project direcotry
  * in a new tab, start celery to monitor tasks with: `celery --app=vrfy.celery:app worker --loglevel=DEBUG`
  * (optional) in another tab, run `celery -A vrfy flower`, which starts a simple webserver so you can monitor the workers and tasks
  
### Tango
  * activate virtualenv
  * run `mockTango`
  * (optional) see 'Getting Tango to work' For how to get a real version of Tango running.
  
------

# Setting up Local Development:
### Start the Database / Create a Table
* `pg_ctl start -D /usr/local/var/postgres`
* `psql -l`  //lists databases
* `createuser vrfy_dev_usr`
* `createdb -O vrfy_dev_usr vrfy_dev`

### Setting up the Django Server and everything:
  * (if you don't have python3 installed, `brew install python3`. if you don't have homwebrew installed, do that.)
  * start postgres database should be something like `pg_ctl start -D /usr/local/var/postgres`, where `/usr/local/var/postgres` is the location of the database. 
  * In another tab/window `cd <vrfy-dir>` and create/start a virtualenv
    - `mkdir ~/Envs/sds_vrfy`
    - `pyvenv ~/Envs/sds_vrfy`
    - and once you're in the directory where this project is, activate the virtual environment with: `source ~/Envs/sds_vrfy/bin/activate`
  * `pip install -r requirements.txt` this command installs the python libs for this project 
   * if you get errors installing pscopg2 and you're on ubuntu, try `sudo apt-get install libpq-dev python-dev`
  * `npm install` this command installs the node modules required for this project (if you don't have node installed `brew install node`)
  * `bower install` this command installs the bower components required for this project (if you don't have bower installed `npm install -g bower`)
  * `python3 manage.py collectstatic` this collects static files from the static folders and the bower_components directories (as per vrfy/settings.py).
  * if you're running this for the first time or have changed the models at all, make migrations (see below)
  * `grunt` this command creates the files & folder necessary (e.g course/static/course)
  * `python3 manage.py gruntserver`  this is a *custom* command that integrates the task runner grunt with the traditional runserver command provided by django (see [https://lincolnloop.com/blog/simplifying-your-django-frontend-tasks-grunt/] if you're curious). Grunt compiles all .scss files into .css, concatenates all .js files and puts them into the /static/ subdirectory of the course app. Whenever a change is made to a .js file in course/js (and respectively, a .scss file in course/sass) grunt recompiles everything and the changes are reflected in the browser (at localhost:8000).  Of course, you can always use `python3 manage.py runserver`, which runs the server using localhost at port 8000. 

  * (Add `/admin` to see the admin interface (which is all there really is to see right now, since the authentication is hardcoded in for this development environment) if you add some problems & problem sets and go back to the home page you'll be able to see the problem sets and problems on the main page)

### If there are migrations to make:
  * `python3 manage.py makemigrations <app_name>`
  * `python3 manage.py migrate`


### Testing via the admin interface
  * log in (create a superuser if you didn'd do that already)
  * any problems (and associated solution files) that are created will be added to the problem_assets folder (for more on the directory structure surrounding that, see solution_file_upload_path() and student_file_upload_path() in course/models.py)


### Create a user for the admin interface:
  * `python3 manage.py createsuperuser`

### Getting Tango to work
This part is optional. Instead of installing Tango, you can run the `mockTango` command in your virtualenv. You won't get full functionality, but it should be enough for most development. 
  * clone Tango to your machine
  * Follow [their instructions](https://github.com/autolab/Tango/wiki/Set-up-Local-Docker-VMMS) for getting Tango running with docker
  * In `vrfy/settings.py` change `TANGO_ADDRESS` to the Tango server's address, `TANGO_KEY` to one of the keys for the server and `TANGO_COURSELAB_DIR` to the directory where Tango will store its courselabs
  * When you start the server you may want to use sudo, ie: `sudo python restful-tango/server.py` to make sure it has permission to edit the courselabs

### To get tango to work (if you don't have a linux machine):
  * (get help with docker)[https://docs.docker.com/installation/mac/#from-your-command-line]
  * `brew install boot2docker`
  * `boot2docker init`
  * `boot2docker start`
  * `eval "$(boot2docker shellinit)"`

Docker examples
Starts an niginx webserver, keeps the process running, publishes the ports, uses the files at the given path, and calls it mysite
`docker run -d -P -v $HOME/site:/usr/share/nginx/html --name mysite nginx`
`docker ps` //lists processes
`boot2docker ip` //boot2docker's ip
`docker pull ubuntu` //grab a linux distro

### Goals
make sure there's markdown support for the problem statements
