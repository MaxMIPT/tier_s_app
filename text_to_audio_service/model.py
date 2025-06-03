import torch
import soundfile as sf
import os
import re
import tempfile

from transliterate import translit
from pathlib import Path

device = torch.device("cpu")
print(device)

model, _ = torch.hub.load(
    repo_or_dir='snakers4/silero-models',
    model='silero_tts',
    language='ru',
    speaker='v4_ru',
    trust_repo=True
)

# Функция для транслитерации английских слов
def transliterate_en_words(text_):
    return re.sub(r'\b[a-zA-Z]+\b', lambda m: translit(m.group(), 'ru'), text_)

def text_to_audio(text_: str):
    processed_text = transliterate_en_words(text_)
    print("Текст после транслитерации:", processed_text)

    # Синтез речи
    audio = model.apply_tts(
        text=processed_text,
        speaker='aidar',   # Или aidar, kseniya, xenia, eugene
        sample_rate=48000
    )

    # Сохраняем WAV
    with tempfile.NamedTemporaryFile(
            suffix=".wav", delete=False) as tmp_output:
        tmp_output_path = tmp_output.name

    wav_path = Path(tmp_output_path)
    sf.write(wav_path, audio, 48000)

    with tempfile.NamedTemporaryFile(
            suffix=".mp3", delete=False) as tmp_output:
        tmp_output_final_path = tmp_output.name

    # Конвертация в MP3
    os.system(f"ffmpeg -y -i {tmp_output_path} -ar 16000 {tmp_output_final_path}")

    with open(tmp_output_final_path, 'rb') as f:
        file_bytes = f.read()
        return file_bytes
