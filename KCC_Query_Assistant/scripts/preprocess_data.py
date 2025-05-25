import pandas as pd
import re
import os

df = pd.read_csv("data/kcc_raw.csv", encoding='utf-8', low_memory=False)

def clean_text(text):
    if pd.isna(text):
        return ""
    text = str(text).strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text

df['QueryText'] = df['QueryText'].apply(clean_text)
df['KccAns'] = df['KccAns'].apply(clean_text)

df = df[(df['QueryText'] != "") & (df['KccAns'] != "")]

df['chunk'] = df.apply(lambda x: f"Q: {x['QueryText']}\nA: {x['KccAns']}", axis=1)

os.makedirs("data", exist_ok=True)
df[['chunk']].to_csv("data/cleaned_kcc_data.csv", index=False)
df[['chunk']].to_json("data/cleaned_kcc_data.json", orient='records', lines=True)

print(f"Cleaned {len(df)} rows and saved successfully.")
