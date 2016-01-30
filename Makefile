option?=""
process?=db-celery:db-worker

include Makefile.in

help:
	@echo "Choose 'make <target> where target is one of the following:"
	@echo ""
	@echo "----------------------------"
	@echo " containers      Start postgres and redis docker containters"
	@echo " flower          Start celery flower on port 8001"
	@echo " notebook        Start ipython notebook on port 8002"
	@echo " redis           Start redis web-client on port 8003"
	@echo " worker          Start celery worker"
	@echo " beat            Start celery beat"
	@echo " processes       Start supervisor processes in background"
	@echo " restart         Restart specific supervisord process"
	@echo " restartall      Restart all supervisord processes"
	@echo " status          Check status or supervisord processes"
	@echo " stopall         Stop all supervisord process"
	@echo " database        Create and migrate Django apps to database"
	@echo " createdb        Create database"
	@echo " migrate         Migrate Django apps to database"
	@echo " makemigrations  Create Django apps migrations"
	@echo " createsu        Create Django admin superuser"
	@echo " graphmodels     Graph and save Django app models"
	@echo " runserverplus   Start Django development server on port 8000"
	@echo " shellplus       Start Django shell using ipython"
	@echo ""


containers:
	docker restart ironapi_db_1
	docker restart ironapi_redis_1
flower:
	celery --app=db.celery:app flower --port=8001

notebook:
	ipython notebook --port=8002

redis:
	redis-commander --redis-port 6380 --port=8003

worker:
	celery worker --app=db.celery:app

beat:
	celery beat --app=db.celery:app

processes:
	supervisord -c supervisord.conf

restart:
	supervisorctl restart $(process)

restartall:
	supervisorctl restart db-celery:db-worker
	supervisorctl restart db-celery:db-beat
	supervisorctl restart web-client:flower
	supervisorctl restart web-client:notebook
	supervisorctl restart web-client:redis
status:
	supervisorctl status db-celery:db-worker
	supervisorctl status db-celery:db-beat
	supervisorctl status web-client:flower
	supervisorctl status web-client:notebook
	supervisorctl status web-client:redis

stopall:
	supervisorctl stop all
	supervisorctl shutdown

database: createdb makemigrations migrate

# execute this in web-app container
createdb:
	$(call _info, Creating databases)
	dropdb -h localhost -p 5433 -U postgres securities_master --if-exists
	createdb -h localhost -p 5433 -U postgres securities_master

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
