import os


def get_audio(n):
    url = "https://www.euskerabiok.com/wp-content/uploads/audios-vocabulario/numeros/"
    os.system(f"curl {url}{n}.mp3 -o _audio/{n}.mp3")


# %%
for i in range(22):
    print(i)
    get_audio(i)

# %%
for i in range(10, 101, 10):
    print(i)
    get_audio(i)
