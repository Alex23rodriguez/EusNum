import polars as pl

unique_words: dict[str, str] = {
    k: v for k, v in pl.read_csv("data/unique_words.csv").iter_rows()
}

# %%


def number_to_word(n: int):
    """Converts a number to euskera."""
    if str(n) in unique_words:
        return unique_words[str(n)]

    if n > 100:
        if n % 100 == 0:
            return unique_words[str(n // 100 * 100)]

        return unique_words[str(n // 100 * 100)] + " eta " + number_to_word(n % 100)

    return unique_words[str(n // 20 * 20) + "_"] + " " + unique_words[str(n % 20)]
