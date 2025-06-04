import json
import subprocess
import tempfile
import os


async def audio_converter(
    file_bytes: bytes,
    file_extension: str = ".wav"
) -> (bytes, float):
    with tempfile.NamedTemporaryFile(
            suffix=file_extension, delete=False) as tmp_input:
        tmp_input.write(file_bytes)
        tmp_input_path = tmp_input.name

    with tempfile.NamedTemporaryFile(
            suffix=".wav", delete=False) as tmp_output:
        tmp_output_path = tmp_output.name

    try:
        cmd = [
            "ffmpeg",
            "-y",
            "-i", tmp_input_path,
            "-ar", "16000",
            "-ac", "1",
            tmp_output_path
        ]

        subprocess.run(
            cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        duration_task = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "json",
                tmp_output_path,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            check=True,
        )
        audio_meta = json.loads(duration_task.stdout)
        audio_duration = float(audio_meta["format"]["duration"])

        with open(tmp_output_path, "rb") as f:
            output_bytes = f.read()

        return output_bytes, audio_duration
    finally:
        os.remove(tmp_input_path)
        os.remove(tmp_output_path)
