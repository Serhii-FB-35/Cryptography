from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

keys = {
    "r2": "он",
    "r3": "кот",
    "r4": "скат",
    "r5": "карст",
    "r10": "дешифровка",
    "r11": "непоколебим",
    "r12": "криптография",
    "r13": "доброжелатель",
    "r14": "датацентрустал",
    "r15": "самообразование",
    "r16": "интернетвотпуске",
    "r17": "кибербезопасность",
    "r18": "капибараподсолнцем",
    "r19": "роботанадалгоритмом",
    "r20": "немоймалварьэтоплохо",
}

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
M = 32

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

def encrypt(text: str, key: str):
    key_nums = text_to_numbers(key)
    key_len = len(key)
    ciphertext = ""

    key_index = 0
    for lett in text:
        x_i = lett_to_num[lett]
        k_i = key_nums[key_index % key_len]
        y_i = (x_i + k_i) % M
        ciphertext += num_to_lett[y_i]
        key_index += 1
    
    return ciphertext

def calc_indx_comp(text: str):
    counts = Counter(text)
    n = len(text)
    sum_N = 0
    for lett in ALPHABET:
        N_t = counts[lett]
        sum_N += N_t * (N_t - 1)
    
    i = sum_N / (n * (n - 1))
    return i


with open("text_without_spaces.txt", "r", encoding="utf-8") as t:
    plain_text = t.read()

i_plain_text = calc_indx_comp(plain_text)

result = list()
result.append({"Довжина ключа": "ВТ", "Індекс відповідності": round(i_plain_text, 6)})
text_result = f"Відкритий текст\n{plain_text}"

lett_df = pd.read_excel("frequency_letter.xlsx")
frequency_dict = lett_df.set_index('Letter')['Frequency'].to_dict()
f_yo = lett_df.loc[lett_df['Letter'] == 'ё', 'Frequency'].values[0]
f_e = lett_df.loc[lett_df['Letter'] == 'е', 'Frequency'].values[0]
f_e_new = f_e + f_yo
lett_df.loc[lett_df['Letter'] == 'е', 'Frequency'] = f_e_new
lett_df = lett_df[lett_df['Letter'] != 'ё']
lett_df['squared'] = lett_df['Frequency'] ** 2
i_rus = lett_df['squared'].sum()
result.append({"Довжина ключа": "РМ", "Індекс відповідності": round(i_rus, 6)})

for key_name in keys:
    key_value = keys[key_name]
    r = len(key_value)

    ciphertext = encrypt(plain_text, key_value)
    i_ciphertext = calc_indx_comp(ciphertext)
    result.append({"Довжина ключа": r, "Індекс відповідності": round(i_ciphertext, 6)})
    text_result += f"\n\n\n\nКлюч: {key_value}\n{ciphertext}"

df = pd.DataFrame(result)
df.to_excel("coincidence_index.xlsx", index=False)

with open("encode_result.txt", "w", encoding="utf-8") as f:
    f.write(text_result)


plt.figure(figsize=(15, 7))
sns.barplot(data=df, x='Довжина ключа', y='Індекс відповідності')
plt.xlabel('Довжина ключа')
plt.ylabel('Індекс відповідності')
plt.tight_layout()
plt.savefig("index.png")