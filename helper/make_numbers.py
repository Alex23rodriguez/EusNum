import polars as pl
from polars import col, lit

# %%
nums = pl.read_csv("data/numbers.csv")

# %%
lt = nums.filter(col("number") < 100)

# %%
hundreds = {
    100: "ehun",
    200: "berrehun",
    300: "hirurehun",
    400: "laurehun",
    500: "bostehun",
    600: "seiehun",
    700: "zazpiehun",
    800: "zortziehun",
    900: "bederatziehun",
}

# %%
nums = []
words = []
for k, v in hundreds.items():
    nums.append(k)
    words.append(v)
    for k2, v2 in lt.iter_rows():
        if k2 == 0:
            continue
        nums.append(k + k2)
        words.append(v + " eta " + v2)

# %%
df = pl.DataFrame({"number": nums, "word": words})

# %%
df = pl.concat([lt, df])
len(df)
# %%
df.write_csv("data/numbers.csv")

# %%
unique_words = set(" ".join(df["word"]).split())

# %%
len(unique_words)
