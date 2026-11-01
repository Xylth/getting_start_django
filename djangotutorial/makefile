.PHONY: up down logs superuser shell deploy

up:
    @test -f .env && echo ".env existe déjà" || ( \
		cp .env.example .env && \
		echo "SECRET_KEY=$$(python3 -c 'import secrets; print(secrets.token_urlsafe(50))')" >> .env && \
		echo ".env créé avec une nouvelle SECRET_KEY" )
    @mkdir -p data
	docker compose up -d --build

down:
	docker compose down


logs:
	docker compose logs -f web

superuser:
	docker compose exec web python manage.py createsuperuser

shell:
	docker compose exec web python manage.py shell

deploy:
	git pull
	$(MAKE) up