option?=""
process?=db-celery:db-worker

include Makefile.in

help:
	@echo "Choose 'make <target> where target is one of the following:"
	@echo ""
	@echo "----------------------------"
	@echo " setup             Start docker containers, create database and log files"
	@echo " process-logs      Create log files"
	@echo " docker-services   Start postgres and redis docker containters"
	@echo " celery-flower     Start celery flower on port 8001"
	@echo " ipython-notebook  Start ipython notebook on port 8002"
	@echo " redis-commander   Start redis web-client on port 8003"
	@echo " celery-worker     Start celery worker"
	@echo " celery-beat       Start celery beat"
	@echo " processes         Start supervisor processes in background"
	@echo " restart           Restart specific supervisord process"
	@echo " restartall        Restart all supervisord processes"
	@echo " status            Check status or supervisord processes"
	@echo " stopall           Stop all supervisord process"
	@echo " database          Create and migrate Django apps to database"
	@echo " createdb          Create database"
	@echo " migrate           Migrate Django apps to database"
	@echo " makemigrations    Create Django apps migrations"
	@echo " createsu          Create Django admin superuser"
	@echo " graphmodels       Graph and save Django app models"
	@echo " runserverplus     Start Django development server on port 8000"
	@echo " shellplus         Start Django shell using ipython"
	@echo ""

test_systems:
	py.test -vv --cov=systems systems/

setup: docker-services database process-logs


process-logs:
	$(call _info, Creating logs files)
	cd db/; mkdir logs; cd logs/; \
	touch supervisord.log celery-worker.log \
	celery-beat.log flower.log notebook.log \
	redis.log server.log

docker-services:
	$(call _info, Starting postgres and redis docker containers)
	docker-compose -p trading up -d db redis

celery-flower:
	$(call _info, Starting celery flower on port 8001)
	celery --app=db.celery:app flower --port=8001

ipython-notebook:
	$(call _info, Starting ipython notebook on port 8002)
	./db/manage.py shell_plus --notebook

redis-commander:
	$(call _info, Starting redis-commander web client on port 8003)
	redis-commander --redis-port 6378 --port=8003

celery-worker:
	$(call _info, Starting celery worker)
	celery worker --app=db.celery:app

celery-beat:
	$(call _info, Starting celery beat)
	celery beat --app=db.celery:app

processes:
	$(call _info, Starting supervisord processes)
	supervisord -c supervisord.conf
	sleep 5
	supervisorctl restart web-client:flower

restart:
	$(call _info, Restarting $(process) supervisord processes)
	supervisorctl restart $(process)

restartall:
	$(call _info, Restarting all supervisord processes)
	supervisorctl restart web-client:server
	supervisorctl restart db-celery:db-worker
	supervisorctl restart db-celery:db-beat
	supervisorctl restart web-client:flower
	supervisorctl restart web-client:notebook
	supervisorctl restart web-client:redis
status:
	$(call _info, Checking status of supervisord processes)
	supervisorctl status db-celery:*
	supervisorctl status web-client:*


stopall:
	$(call _info, Stoping all supervisord processes)
	supervisorctl stop all
	supervisorctl shutdown

database: createdb makemigrations migrate createsu

# execute this in web-app container
createdb:
	$(call _info, Creating database)
	dropdb -h localhost -p 5431 -U postgres securities_master --if-exists
	createdb -h localhost -p 5431 -U postgres securities_master

# migrate db changes
migrate:
	$(call _info, Migrating Django app to database)
	./db/manage.py migrate

# make migrations
makemigrations:
	$(call _info, Creating new database migrations)
	./db/manage.py makemigrations

# create superuser
createsu:
	$(call _info, Creating superuser for Django app)
	./db/manage.py createsuperuser

# visualize models
graphmodels:
	$(call _info, Graphing Django app models)
	./db/manage.py graph_models --pygraphviz -a -g -o graphed_models.png

# start server
runserverplus:
	$(call _info, Start server with Werkzeug debugger)
	./db/manage.py runserver_plus

# shell_plus
shellplus:
	$(call _info, Starting ipython shell with notebook plugin)
	./db/manage.py shell_plus --$(option)

# tree
tree:
	$(call _info, Showing directory structure for project)
	tree -I '*.pyc|logs|*.pid|*schedule|*.png|00*'

# collect statis files into static folder
collectstatic:
	$(call _info, Collecting static files)
	./db/manage.py collectstatic --noinput
	cp -r ${IPYTHON_STATIC}/* db/static/
	cp -r ${REDIS_STATIC}/* db/static/
	cp -r ${FLOWER_STATIC}/* db/static/
