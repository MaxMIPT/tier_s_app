FROM python:3.12-slim

WORKDIR /worker

COPY pyproject.toml .

RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY . .

CMD ["poetry", "run", "python3.12", "run_worker.py"]
