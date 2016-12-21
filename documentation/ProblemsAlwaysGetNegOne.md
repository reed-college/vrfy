# Oh no! cs.reed.edu is not working! What do I do?!?!
  Before the school year started, Jim tested vrfy and found that none of the problems he submitted were getting graded. This is a short guide on how to fix that quickly and easily.
  This assumes knowlege of how python virtualenvs work
## Log on to vrfy user
  !This step must be done before the rest!
  This makes sure you have proper permissions to the vrfy user's things
  * Just type `ksudo su - vrfy` to log on
  
## Restart Tango
  * cd into `Tango` directorty in vrfy's home folder
  * `source bin/activate`
  * `sh startTangoREST.sh`
  * If tango is already running, it will tell you in the log info.
  * press `ctrl-c` If Tango is running, stop here.
  * `sh startTangoREST.sh &`
  * `ctrl-c`. This will run the `startTangoREST.sh` in the background
  
## Restart Redis
  * `redis-server &` and `ctrl-c`
  * Also, celery (next step) will tell you if redis is not running
  
## Restart Celery
  * Make sure you're in the virtualenv and the vrfy project folder (the one that has `manage.py`)
  * run `celery --app=vrfy.celery:app worker --loglevel=DEBUG --detach`
