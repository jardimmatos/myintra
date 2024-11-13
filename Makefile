.PHONY: docs clean

COMMAND = python manage.py

run-daphne:
	daphne condominio.asgi:application -b 127.0.0.1 -p 8000

collectstatic:
	$(COMMAND) collectstatic

run:
	$(COMMAND) runserver

migrations:
	$(COMMAND) makemigrations && $(COMMAND) migrate

cmdBase:
	$(COMMAND) BaseCmd

super:
	$(COMMAND) createsuperuser

celery:
	celery -A condominio worker -B -l info

flake:
	flake8 --exclude=migrations,venv,pwa-condominio ./

bandit:
	bandit -r ./

precommit:
	pre-commit run --all-files

installprecommit:
	pre-commit install

validateall:
	autopep8 -a -a --diff ./*/*.py && flake8 ./ && bandit -r ./ && pre-commit run --all-files

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  run             Para execução do runserver"
	@echo "  run-daphne      Para execução do runserver via ASGI"
	@echo "  migrations  	 Para gerar e aplicar migrações"
	@echo "  cmdBase         Para Executar o Command BaseCmd"
	@echo "  collectstatic   Para obter os arquivos estáticos"
	@echo "  super           Criar um superusuário"
	@echo "  celery          Executar o Celery da aplicação"
	@echo "  installprecommit Instalar pre-commit"
	@echo "  precommit       Executar verificação do pre-commit"
	@echo "  flake           Executar checagem de padrão de código"
	@echo "  bandit          Executar checagem de segurança e confiabilidade"
