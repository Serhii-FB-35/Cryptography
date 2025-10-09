from collections import Counter
import pandas as pd


def bigram_frq(text: str, step: int):
    bigrams = list()

    for i in range(0, len(text)-1, step):
        bigram = text[i : i+2]
        if len(bigram) == 2:
            bigrams.append(bigram)

    bigram_counts = Counter(bigrams)
    total_bigrams = sum(bigram_counts.values())
    freqs = list()

    for bigr, cnt in bigram_counts.items():
        fst = bigr[0]
        scnd = bigr[1]
        freq = cnt / total_bigrams
        freqs.append((fst, scnd, freq))

    df = pd.DataFrame(freqs, columns=["First_letter", "Second_letter", "Frequency"])
    matrix = df.pivot_table(index="First_letter", columns="Second_letter", values="Frequency", fill_value=0)
    return matrix


with open("cleaned_russian_text_with_spaces.txt", "r", encoding="utf-8") as t:
    text_spaces = t.read()
frequency_spaces_cross = bigram_frq(text_spaces, 1)
frequency_spaces_cross.to_excel("Frequency_bigram_cross_russian_text_with_spaces.xlsx")
frequency_spaces_steps = bigram_frq(text_spaces, 2)
frequency_spaces_steps.to_excel("Frequency_bigram_russian_text_with_spaces.xlsx")

with open("cleaned_russian_text_without_spaces.txt", "r", encoding="utf-8") as t:
    text = t.read()
frequency_cross = bigram_frq(text, 1)
frequency_cross.to_excel("Frequency_bigram_cross_russian_text_without_spaces.xlsx")
frequency_steps = bigram_frq(text, 2)
frequency_steps.to_excel("Frequency_bigram_russian_text_without_spaces.xlsx")
