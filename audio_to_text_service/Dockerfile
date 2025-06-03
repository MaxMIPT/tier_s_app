FROM python:3.11-slim

WORKDIR /audio_to_text_service

COPY pyproject.toml .

RUN pip install poetry

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

RUN poetry config virtualenvs.create false
RUN poetry install --no-root
RUN transformers-cli download openai/whisper-small
# RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128

COPY . .

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]
