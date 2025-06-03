# конвертирует датасет data_orig в data_conv, в wav 16к битрейт

import os
from pydub import AudioSegment

def convert_folder_to_wav16k(src_dir: str, dst_dir: str):
    os.makedirs(dst_dir, exist_ok=True)

    for filename in os.listdir(src_dir):
        src_path = os.path.join(src_dir, filename)

        if not os.path.isfile(src_path):
            continue

        base_name, _ = os.path.splitext(filename)
        dst_filename = f"{base_name}.wav"
        dst_path = os.path.join(dst_dir, dst_filename)

        try:
            audio = AudioSegment.from_file(src_path)
            audio = audio.set_frame_rate(16000)
            audio = audio.set_sample_width(2)
            audio.export(dst_path, format="wav")

            print(f"[OK]  {filename} → {dst_filename}")
        except Exception as e:
            print(f"[ERROR] не удалось конвертировать {filename}: {e}")

if __name__ == "__main__":
    source_folder = "data_orig"
    target_folder = "data_conv"

    convert_folder_to_wav16k(source_folder, target_folder)
