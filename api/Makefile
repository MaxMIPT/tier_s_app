CHANGED_FILES=$(shell git diff --name-only origin/main...HEAD -- '*.py')

ruff:
	@if [ -z "$(CHANGED_FILES)" ]; then \
		echo "Нет изменённых файлов для проверки ruff."; \
	else \
		echo "Проверка с помощью ruff..."; \
		ruff $(CHANGED_FILES); \
	fi


flake8:
	@if [ -z "$(CHANGED_FILES)" ]; then \
		echo "Нет изменённых файлов для проверки flake8."; \
	else \
		echo "Проверка с помощью flake8..."; \
		flake8 $(CHANGED_FILES); \
	fi

lint: ruff flake8
	@echo "Проверка завершена."


lint-flake8-local:
	.venv\Scripts\activate
	poetry run flake8 --exclude ".\.venv" .