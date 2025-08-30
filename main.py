import json
import os
from random import choice, randint, random

from cligame import Game

from util import concat_audio_files, number_to_word

# %%
with open("data/unique_words.json", "r") as f:
    unique_words = json.load(f)

nums = {v: k for k, v in unique_words.items()}

audio_dir = "./audio"


# %%
numbers_with_audio = list(range(60)) + [60, 80, 100] * 5


# %%
def rev_map(sentence):
    words = sentence.split(" ")
    return [nums[w] for w in words]


# %%
# Game modes


def audio_quiz(_):
    n = choice(numbers_with_audio)
    word = number_to_word(n)

    concat_audio_files(
        rev_map(word), audio_dir, output_file="tmp/result.wav", ext="wav"
    )
    os.system("afplay tmp/result.wav")

    ans = input(f"Which number did you hear? ")
    correct_ans = str(n)

    return ans == correct_ans, f"{correct_ans}: {word}"


def spelling_quiz(_):
    n = randint(0, 999)
    word = number_to_word(n)

    ans = input(f"Spell {n}: ".ljust(17))
    correct_ans = word

    return ans == correct_ans, f"{correct_ans}"


def mixed_quiz(_):
    if random() < 0.5:
        return audio_quiz(_)
    else:
        return spelling_quiz(_)


# %%


# choose game
prompt = """Available games:
    1 - spelling
    2 - audio
    3 - mixed
Game: """

games = {
    "1": spelling_quiz,
    "2": audio_quiz,
    "3": mixed_quiz,
}

chosen_game = input(prompt)

mygame = Game(games[chosen_game])
mygame.start()

stats_files = {
    "1": "stats/spelling.json",
    "2": "stats/audio.json",
    "3": "stats/mixed.json",
}

mygame.save_raw(stats_files[chosen_game])
