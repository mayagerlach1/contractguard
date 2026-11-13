from pathlib import Path

import pandas as pd

from src.config import RISKS
from src.reviewer import review_contract

df = pd.read_csv("data/sample_25.csv")

for i in range(3):
    row = df.iloc[i]
    text = Path(row["txt_path"]).read_text(encoding="utf-8", errors="ignore")
    result, usage = review_contract(text)

    print(f"\n=== {row['Filename'][:60]} ({row['words']} words) ===")
    for key, risk in RISKS.items():
        claude = "Yes" if result.get(key, {}).get("present") else "No"
        lawyers = row[f"{risk['label']}-Answer"]
        mark = "✅" if claude == lawyers else "❌"
        print(f"{mark} {risk['label']:<28} Claude: {claude:<4} Lawyers: {lawyers}")
    print(f"Tokens: {usage.input_tokens} in / {usage.output_tokens} out")
    