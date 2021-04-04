.PHONY: publish deploy-local deploy-db deploy-api deploy-web

build:
	docker-compose build

publish:
	docker-compose build && docker-compose push

deploy-local:
	docker-compose pull db searchserver web && docker-compose up -d db searchserver web && sleep 10 && docker exec -it hdbguru_db_1 bash ./run_migrate.sh up

deploy-db:
	docker-compose -f docker-compose.prod.yml pull db\
	&& docker-compose -f docker-compose.prod.yml up -d db\
	&& sleep 10\
	&& docker exec -it hdbguru_db_1 bash ./run_migrate.sh up

deploy-api:
	docker-compose -f docker-compose.prod.yml pull searchserver\
	&& docker-compose -f docker-compose.prod.yml up -d searchserver

deploy-web:
	docker-compose -f docker-compose.prod.yml pull web\
	&& docker-compose -f docker-compose.prod.yml up -d web

updatedb:
	docker-compose -f docker-compose.prod.yml pull dataserver\
	&& docker-compose -f docker-compose.prod.yml up dataserver

updatedb-local:
	docker-compose pull dataserver && docker-compose up dataserver