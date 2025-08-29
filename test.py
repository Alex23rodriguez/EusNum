import polars as pl

from util import number_to_word


def test_number_to_word():

    for number, word in pl.read_csv("data/numbers.csv").iter_rows():
        print(number)
        assert (
            number_to_word(number) == word
        ), f"{number} should be {word}, but is {number_to_word(number)}"
