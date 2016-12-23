# Supervisor
Supervisor is a service that will run programs that you ask it to on startup. We use it so that when the machine reboots for whatever reason, the services running on the machine still operate normally. 

All of the supervisor configuration files are stored on the server in `/etc/supervisor/conf.d/`. There are 4 files in this folder:
  1. gunicorn.conf
  2. tango.conf
  3. redis.conf
  4. celery.conf
  
You can lookup [here](http://supervisord.org/configuration.html#program-x-section-settings) what the individual settings in each of these files mean.
