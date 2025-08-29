import polars as pl

# %%
unique_words = set(" ".join(pl.read_csv("data/numbers.csv")["word"]).split())

# %%
with open("data/unique_words.txt", "w") as f:
    f.write("\n".join(unique_words))
