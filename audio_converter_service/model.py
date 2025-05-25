import random

def audio_converter(file):
    magic_number = random.randint(1, 10)
    if magic_number == 1:
        raise Exception
    else:
        with open("./example.wav", "rb") as file:
            data = file.read()
        return data