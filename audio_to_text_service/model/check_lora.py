from pathlib import Path
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from peft import PeftModel
import torchaudio, torch

base  = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")
model = PeftModel.from_pretrained(base, "whisper-small-lora", local_files_only=True)

print("LoRA adapters:", model.peft_config)
print("trainable params:", sum(p.numel() for p in model.parameters() if p.requires_grad))
