FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /audio_converter_service

COPY pyproject.toml .

RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY . .

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
