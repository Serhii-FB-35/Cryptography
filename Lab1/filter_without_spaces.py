import re


def clean_text(text: str):
    text = text.lower()
    cleaned_text = re.sub(f"[^а-яёъ]", "", text)
    cleaned_text = re.sub(r"\s+", "", cleaned_text).strip()
    return cleaned_text


with open("russian_text.txt", "r", encoding="utf-8") as t:
    text = t.read()
cleaned_text = clean_text(text)
with open("cleaned_russian_text_without_spaces.txt", "w", encoding="utf-8") as t:
    t.write(cleaned_text)
