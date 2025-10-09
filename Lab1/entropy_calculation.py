from collections import Counter
import math
import pandas as pd


def H1(text: str):
    total = len(text)
    counts = Counter(text)
    entropy = 0

    for cnt in counts.values():
        p = cnt / total
        entropy += -p * math.log2(p)

    return entropy


def H2(text: str, step: int):
    bigrams = list()

    for i in range(0, len(text)-1, step):
        bigram = text[i : i+2]
        if len(bigram) == 2:
            bigrams.append(bigram)
    
    total = len(bigrams)
    counts = Counter(bigrams)
    entropy = 0

    for cnt in counts.values():
        p = cnt / total
        entropy += -p * math.log2(p)

    return entropy / 2


def redundancy(entropy):
    h0 = math.log2(33)
    r = 1 - (entropy / h0)
    return r


def redundancy_space(entropy):
    h0 = math.log2(34)
    r = 1 - (entropy / h0)
    return r


with open("cleaned_russian_text_with_spaces.txt", "r", encoding="utf-8") as t:
    text_spaces = t.read()
h1_space = H1(text_spaces)
r1_space = redundancy_space(h1_space)
h2_space_cross = H2(text_spaces, 1)
r2_space_cross = redundancy_space(h2_space_cross)
h2_space_steps = H2(text_spaces, 2)
r2_space_steps = redundancy_space(h2_space_steps)

with open("cleaned_russian_text_without_spaces.txt", "r", encoding="utf-8") as t:
    text = t.read()
h1 = H1(text)
r1 = redundancy(h1)
h2_cross = H2(text, 1)
r2_cross = redundancy(h2_cross)
h2_steps = H2(text, 2)
r2_steps = redundancy(h2_steps)

table = [("Н1|R1 (З пробілами)", h1_space, r1_space), ("Н1|R1 (Без пробілами)", h1, r1), ("H2|R2 (Перетинаються, з пробілами)", h2_space_cross, r2_space_cross), 
         ("H2|R2 (Перетинаються, без пробілів)", h2_cross, r2_cross), ("H2|R2 (Не перетинаються, з пробілами)", h2_space_steps, r2_space_steps), 
         ("H2|R2 (Не перетинаються, без пробілів)", h2_steps, r2_steps)]

df = pd.DataFrame(table, columns=[" ", "Ентропія", "Надлишковість"])
df.to_excel("Entropy_redundancy.xlsx", index=False)