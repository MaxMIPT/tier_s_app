#!/usr/bin/env python
# whisper_lora_stable_fast.py  (Windows)

import os, multiprocessing as mp, types, torch
from datasets import load_dataset, Audio
from transformers import (
    AutoProcessor,
    AutoModelForSpeechSeq2Seq,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer,
)
from peft import LoraConfig, get_peft_model, TaskType


CSV_PATH   = "transcripts.csv" 
OUTPUT_DIR = "whisper-small-lora-ru"
MODEL_NAME = "openai/whisper-small"

BATCH_SIZE = 8         
GRAD_ACC   = 1        
MAX_STEPS  = 300  
LR         = 2e-4
# ────────────────

# 1) датасет
ds = load_dataset("csv", data_files=CSV_PATH, split="train")
ds = ds.cast_column("path", Audio(sampling_rate=16_000))

# 2) процессор и модель
proc  = AutoProcessor.from_pretrained(MODEL_NAME, language="ru", task="transcribe")
base  = AutoModelForSpeechSeq2Seq.from_pretrained(MODEL_NAME)

class WhisperTrainer(Seq2SeqTrainer):
    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        inputs.pop("input_ids", None)       
        inputs.pop("decoder_input_ids", None) 
        out = model(input_features=inputs["input_features"],
                    labels=inputs["labels"])
        return (out.loss, out) if return_outputs else out.loss

# 3) LoRA
model = get_peft_model(
    base,
    LoraConfig(
        r=16, lora_alpha=32, lora_dropout=0.05,
        target_modules=["q_proj", "v_proj"],
        task_type=TaskType.SEQ_2_SEQ_LM,
        bias="none",
    ),
)

orig_forward = model.base_model.forward
def patched_forward(self, *args, **kw):
    kw.pop("input_ids", None)
    kw.pop("inputs_embeds", None)
    kw.pop("decoder_input_ids", None)
    return orig_forward(*args, **kw)

model.base_model.forward = types.MethodType(patched_forward, model.base_model)
model.print_trainable_parameters()

def prepare(ex):
    wav = ex["path"]
    ex["input_features"] = proc.feature_extractor(
        wav["array"], sampling_rate=wav["sampling_rate"],
        return_tensors="pt").input_features[0]
    ex["labels"] = proc.tokenizer(ex["text"], return_tensors="pt").input_ids[0]
    return ex

ds = ds.map(prepare, remove_columns=ds.column_names,
            num_proc=1, desc="Preparing")

def collate(batch):
    feats = torch.stack([torch.as_tensor(b["input_features"], dtype=torch.float32)
                         for b in batch])
    lbls  = torch.nn.utils.rnn.pad_sequence(
        [torch.as_tensor(b["labels"], dtype=torch.long) for b in batch],
        batch_first=True, padding_value=-100)
    return {"input_features": feats, "labels": lbls}

args = Seq2SeqTrainingArguments(
    output_dir                = OUTPUT_DIR,
    per_device_train_batch_size= BATCH_SIZE,
    gradient_accumulation_steps= GRAD_ACC,
    learning_rate             = LR,
    max_steps                 = MAX_STEPS,
    fp16                      = torch.cuda.is_available(),
    logging_steps             = 10,    
    save_steps                = 0,      
    save_total_limit          = 2,
    predict_with_generate     = False,
    report_to                 = "none",
    remove_unused_columns     = False,
)

trainer = WhisperTrainer(
    model=model,
    args=args,
    train_dataset=ds,
    data_collator=collate,
)

if __name__ == "__main__":
    mp.freeze_support()
    trainer.train()
    model.save_pretrained(OUTPUT_DIR)
    proc.save_pretrained(OUTPUT_DIR)
