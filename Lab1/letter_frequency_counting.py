from collections import Counter
import pandas as pd


def letter_frq(text: str):
    total_letters = len(text)
    letter_counts = Counter(text)

    freqs = list()

    for let, cnt in letter_counts.items():
        freq = cnt / total_letters
        freqs.append((let, freq))

    df = pd.DataFrame(freqs, columns=["Letter", "Frequency"])
    df = df.sort_values(by="Frequency", ascending=False)
    return df


with open("cleaned_russian_text_with_spaces.txt", "r", encoding="utf-8") as t:
    text_spaces = t.read()
frequency_spaces = letter_frq(text_spaces)
frequency_spaces.to_excel("Frequency_letter_russian_text_with_spaces.xlsx", index=False)

with open("cleaned_russian_text_without_spaces.txt", "r", encoding="utf-8") as t:
    text = t.read()
frequency = letter_frq(text)
frequency.to_excel("Frequency_letter_russian_text_without_spaces.xlsx", index=False)
