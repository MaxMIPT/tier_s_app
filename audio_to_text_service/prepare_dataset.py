from datasets import load_dataset, Audio

def prepare():
    dataset = load_dataset("csv", data_files={"train": "transcripts.csv"})
    dataset["train"] = dataset["train"].cast_column("path", Audio(sampling_rate=16000))
    dataset["train"] = dataset["train"].rename_column("path", "audio")  # только эту переименовываем
    dataset["train"].save_to_disk("my_dataset")
    print("✅ Dataset сохранён в ./my_dataset")

if __name__ == "__main__":
    prepare()
