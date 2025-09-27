import os
import subprocess

import polars as pl

# %%
unique_words: dict[str, str] = {
    k: v for k, v in pl.read_csv("data/unique_words.csv").iter_rows()
}

# %%


def number_to_word(n: int):
    """Converts a number to euskera."""
    assert n < 1_000_000, f"{n} is too big to convert"

    if str(n) in unique_words:
        return unique_words[str(n)]

    if n > 1000:
        return f"{number_to_word(n // 1000)} mila {number_to_word(n % 1000)}"

    if n > 100:
        if n % 100 == 0:
            return unique_words[str(n // 100 * 100)]

        return unique_words[str(n // 100 * 100)] + " eta " + number_to_word(n % 100)

    return unique_words[str(n // 20 * 20) + "_"] + " " + unique_words[str(n % 20)]


# %%
def concat_audio_files(file_names, audio_dir, output_file="tmp/output.wav", ext="wav"):
    """
    Concatenates audio files using ffmpeg.

    Parameters:
        file_names (list): List of files to concatenate.
        audio_dir (str): Directory containing word audio files (e.g., 'hello.mp3').
        output_file (str): Final concatenated audio file.
        ext (str): Extension of audio files (e.g., 'mp3' or 'wav').
    """
    # Collect matching audio file paths
    audio_files = []
    for word in file_names:
        filename = f"{word.lower()}.{ext}"
        filepath = os.path.join(audio_dir, filename)
        if os.path.exists(filepath):
            audio_files.append(filepath)
        else:
            print(f"Warning: Missing audio for '{word}' -> {filepath}")

    if not audio_files:
        print("No audio files found. Exiting.")
        return

    # Create a temporary text file listing files for ffmpeg concat
    list_file = "tmp/file_list.txt"
    with open(list_file, "w") as f:
        for file in audio_files:
            f.write(f"file '{os.path.abspath(file)}'\n")

    # Run ffmpeg concat
    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        list_file,
        "-c",
        "copy",
        output_file,
    ]

    try:
        subprocess.run(cmd, check=True, stderr=subprocess.DEVNULL)

    except subprocess.CalledProcessError as e:
        print("Error running ffmpeg:", e)
    finally:
        os.remove(list_file)
