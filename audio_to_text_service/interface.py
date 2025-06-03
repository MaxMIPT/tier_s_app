from pathlib import Path
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from peft import PeftModel
import torchaudio, torch

BASE_ID   = "openai/whisper-small"
ADAPTER   = Path(r"./whisper-small-lora-ru")

base   = WhisperForConditionalGeneration.from_pretrained(BASE_ID)
model  = PeftModel.from_pretrained(base, ADAPTER, local_files_only=True).to("cuda")
proc   = WhisperProcessor.from_pretrained(BASE_ID)


print("LoRA trainable:", sum(p.numel() for n,p in model.named_parameters() if "lora" in n))

wave, sr = torchaudio.load("output.wav")
wave = torchaudio.functional.resample(wave, sr, 16_000).squeeze().numpy()

inputs = proc(
    wave,
    sampling_rate=16_000,
    return_tensors="pt"
).input_features.to(model.device)

ids = model.generate(
    input_features=inputs,
    max_new_tokens=444,  
    language="ru"       
)
print("Результат:")
print(proc.batch_decode(ids, skip_special_tokens=True)[0])
