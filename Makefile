
include Makefile.in

help:
	@echo "Choose 'make <target> where target is one of the following:"
	@echo ""
	@echo "----------------------------"
	@echo " database          Creates and migrates database"
	@echo " create_db         Creates database"
	@echo " migrate           Migrate Django app to database"
	@echo " makemigrations    Create Django app migrations"
	@echo " createsu          Create Django admin superuser"
	@echo " graph_models      Graph and save Django app models"
	@echo ""

database: create_db makemigrations migrate

# execute this in web-app container
create_db:
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
graph_models:
	$(call _info, Graphing Django app models)
	./db/manage.py graph_models --pygraphviz -a -g -o graphed_models.png
