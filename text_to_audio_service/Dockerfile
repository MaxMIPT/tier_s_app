FROM python:3.11-slim

WORKDIR /text_to_audio

COPY pyproject.toml .

RUN apt-get update && apt-get install -y libgomp1 && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root
RUN pip install pathlib torch torchaudio
RUN pip install soundfile
RUN pip install transliterate
RUN pip install omegaconf

COPY . .

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8004"]
