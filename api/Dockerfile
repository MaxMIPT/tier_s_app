FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml .

RUN apt-get update && apt-get install -y \
    libmagic1 \
    libmagic-dev \
    file \
    && rm -rf /var/lib/apt/lists/*


RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root
COPY . .
CMD ["poetry", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
