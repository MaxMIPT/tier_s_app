import torch
import soundfile as sf
import os
import re
from transliterate import translit
from pathlib import Path

# Функция для транслитерации английских слов
def transliterate_en_words(text):
    return re.sub(r'\b[a-zA-Z]+\b', lambda m: translit(m.group(), 'ru'), text)

text = "Привет! Hello! GPT is amazing. Это пример офлайн синтеза."

processed_text = transliterate_en_words(text)
print("Текст после транслитерации:", processed_text)

# Загружаем модель
model, _ = torch.hub.load(
    repo_or_dir='snakers4/silero-models',
    model='silero_tts',
    language='ru',            
    speaker='v4_ru',  
    trust_repo=True
)

# Синтез речи
audio = model.apply_tts(
    text=processed_text,
    speaker='aidar',   # Или aidar, kseniya, xenia, eugene
    sample_rate=48000
)

# Сохраняем WAV
wav_path = Path("output.wav")
sf.write(wav_path, audio, 48000)

# Конвертация в MP3
os.system(f"ffmpeg -y -i {wav_path} -ar 16000 output.mp3")

print("✅ Синтез завершён. Файлы: output.wav и output.mp3")
