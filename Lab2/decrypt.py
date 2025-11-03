from collections import Counter
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
M = 32
COMMON_LETTERS = ["о","е", "а", "и", "т"]
KEY_LENGTH = 14

num_to_lett = dict()
for i, lett in enumerate(ALPHABET):
    num_to_lett[i] = lett

lett_to_num = dict()
for i, lett in enumerate(ALPHABET):
    lett_to_num[lett] = i

def text_to_numbers(text: str):
    numbers = list()
    for char in text:
        numbers.append(lett_to_num[char])
    
    return numbers

def calc_indx_comp(text: str):
    counts = Counter(text)
    n = len(text)
    sum_N = 0
    for lett in ALPHABET:
        N_t = counts[lett]
        sum_N += N_t * (N_t - 1)
    
    i = sum_N / (n * (n - 1))
    return i

def key_len(text: str, max_r: int):
    results = list()
    for r in range(2, max_r+1):
        total_i = 0
        for i in range(r):
            block = text[i::r]
            i_block = calc_indx_comp(block)
            total_i += i_block
        avrg_i = total_i / r
        results.append((r, avrg_i))
    df_results = pd.DataFrame(results, columns=['Довжина ключа', 'Індекс відповідності'])
    return df_results

def clean_text(text: str):
    cleaned_text = re.sub(r"\s+", "", text)
    return cleaned_text

def decrypt(ciphertext: str, key: str):
    key_length = len(key)
    decrypted_text = ""

    for i, ciph_char in enumerate(ciphertext):
        key_char = key[i % key_length]
        cipher_num = lett_to_num[ciph_char]
        key_num = lett_to_num[key_char]
        plain_num = (cipher_num - key_num) % M
        plain_char = num_to_lett[plain_num]
        decrypted_text += plain_char
    
    return decrypted_text

with open("encrypted_text.txt", "r", encoding="utf-8") as t:
    text = t.read()

text = clean_text(text)
df = key_len(text, 32)
df.to_excel("key_length.xlsx", index=False)

plt.figure(figsize=(15, 7))
sns.barplot(data=df, x='Довжина ключа', y='Індекс відповідності')
plt.xlabel('Довжина ключа')
plt.ylabel('Індекс відповідності')
plt.tight_layout()
plt.savefig("key_length.png")

probable_key_letters_1 = []
probable_key_letters_2 = []
probable_key_letters_3 = []
probable_key_letters_4 = []
probable_key_letters_5 = []

for i in range(KEY_LENGTH):
    block_text = text[i::KEY_LENGTH]
    block_counts = Counter(block_text)
    frq_lett = block_counts.most_common(1)[0][0]
    y_star_num = lett_to_num[frq_lett]
    for common_let in COMMON_LETTERS:
        x_star_num = lett_to_num[common_let]
        key_num = (y_star_num - x_star_num) % M
        key_letter = num_to_lett[key_num]
        if common_let == "о":
            probable_key_letters_1.append(key_letter)
        elif common_let == "е":
            probable_key_letters_2.append(key_letter)
        elif common_let == "а":
            probable_key_letters_3.append(key_letter)
        elif common_let == "и":
            probable_key_letters_4.append(key_letter)
        elif common_let == "т":
            probable_key_letters_5.append(key_letter)

key_1 = "".join(probable_key_letters_1)
key_2 = "".join(probable_key_letters_2)
key_3 = "".join(probable_key_letters_3)
key_4 = "".join(probable_key_letters_4)
key_5 = "".join(probable_key_letters_5)
print(f"Ключ при 'о': {key_1}")
print(f"Ключ при 'е': {key_2}")
print(f"Ключ при 'а': {key_3}")
print(f"Ключ при 'и': {key_4}")
print(f"Ключ при 'т': {key_5}")

key = "последнийдозор"
decrypted_text = decrypt(text, key)
with open("decrypted.txt", "w", encoding="utf-8") as f:
    f.write(decrypted_text)
