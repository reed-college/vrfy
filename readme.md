### Python3 Virtual Env

  * `mkdir ~/Envs/sds_vrfy`
  * `pyvenv ~/Envs/sds_vrfy`
  * and once you're in the directory where this project is, activate the virtual environment with: `source ~/Envs/sds_vrfy/bin/activate`

### Start the Database / Create a Table
* `pg_ctl start -D /usr/local/var/postgres`
* `psql -l`  //lists databases
* `createuser <username>`
* `createdb -O <username> <dbname>`

### Start Redis (Used as a message broker with Celery)
  * `redis-server`
  * Test to see if it's up & accepting connections with `redis-cli ping`

### Celery
  * in a new tab, start celery to monitor tasks with: `celery --app=vrfy.celery:app worker --loglevel=DEBUG`
  * in another tab, run `celery -A vrfy flower`, which starts a simple webserver so you can monitor the workers and tasks

**Use these names in the settings file**

------

### Running locally:
  * In Debian, run the following, `sudo apt install python3-pip virtualenv libpq-dev python-dev postgresql postgresql-client supervisor chromium`
  * Setup postgres database goodies: As the postgres user `psql -c "CREATE ROLE vrfy_dev_usr WITH PASSWORD 'pass'; ALTER ROLE vrfy_dev_usr with LOGIN; GRANT ALL PRIVILEGES ON DATABASE vrfy_dev to vrfy_dev_usr;"` and then `psql -c "CREATE DATABASE vrfy_dev OWNER vrfy_dev_usr;"`
  * In Debian, install Docker via these steps https://docs.docker.com/install/linux/docker-ce/debian/
  * Create the vrfy user: `adduser vrfy` and then add it to the sudo and docker groups: `sudo usermod -aG sudo,docker vrfy`
  * Create a python3 virtual environment for the project and source it: `cd ~; virtualenv --python=/usr/bin/python3.5 py3_env; source py3_env/bin/activate`
  * `pip3 install -r requirements.txt` this command installs the python libs for this project
  * Install npm on Debian via https://github.com/nodesource/distributions/blob/master/README.md#debinstall (good ole curl-to-bash as root)
  * Install bower via npm: `sudo npm install -g bower`
  * `bower install` this command installs the bower components required for this project
  * Run `mkdir /home/vrfy/vrfy/logging/`
  * `python3 manage.py collectstatic` this collects static files from the static folders and the bower_components directories (as per vrfy/settings.py).
  * Run `python3 manage.py migrate`
  * Install grunt: `sudo npm install -g grunt-cli`
  * `grunt` this command creates the files & folder necessary (e.g course/static/course)
  * Create the superuser for the admin console: `python3 manage.py createsuperuser`
  * `python3 manage.py gruntserver`  this is a *custom* command that integrates the task runner grunt with the traditional runserver command provided by django (see [https://lincolnloop.com/blog/simplifying-your-django-frontend-tasks-grunt/] if you're curious). Grunt compiles all .scss files into .css, concatenates all .js files and puts them into the /static/ subdirectory of the course app. Whenever a change is made to a .js file in course/js (and respectively, a .scss file in course/sass) grunt recompiles everything and the changes are reflected in the browser (at localhost:8000).  Of course, you can always use `python3 manage.py runserver`, which runs the server using localhost at port 8000. 

### If there are migrations to make:
  * `python3 manage.py makemigrations <app_name>`
  * `python3 manage.py migrate`

### Getting Tango to work
  * clone Tango to your machine
  * Follow [their instructions](https://github.com/autolab/Tango/wiki/Set-up-Local-Docker-VMMS) for getting Tango running with docker
  * In `vrfy/settings.py` change `TANGO_ADDRESS` to the Tango server's address, `TANGO_KEY` to one of the keys for the server and `TANGO_COURSELAB_DIR` to the directory where Tango will store its courselabs
  * When you start the server you may want to use sudo, ie: `sudo python restful-tango/server.py` to make sure it has permission to edit the courselabs

----------

### Notes on cs.reed.edu from the sysadmin side of things:
 * Startup scripts for all the necessary cshw/vrfy services are under /etc/supervisor/conf.d/
 * The main config file for Tango is /home/vrfy/Tango/config.py
 * The main config files for cshw/vrfy are /home/vrfy/vrfy/vrfy/settings.py and /home/vrfy/vrfy/vrfy/settings_local.py. Any variable set in settings_local.py will supercede the one in settings.py
 * Database backups are handled via a crontab entry for the vrfy user. It runs the following "/bin/sh $HOME/vrfy/scripts/backup.sh 2>&1 /dev/null". The entire virtualmachine also has weekly snapshots taken for disaster recovery if needed.
 * All the grading scripts live under /home/vrfy/vrfy/problem_assets/SECTION_NAME/solutions/PROBLEM_NAME/
