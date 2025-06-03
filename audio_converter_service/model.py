import subprocess
import tempfile
import os


async def audio_converter(
    file_bytes: bytes,
    file_extension: str = ".wav"
) -> bytes | None:
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

        with open(tmp_output_path, "rb") as f:
            output_bytes = f.read()

        return output_bytes
    finally:
        os.remove(tmp_input_path)
        os.remove(tmp_output_path)
