import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd

from src.config import RISKS
from src.reviewer import review_contract

PRICES = {  # USD per million tokens: (input, output)
    "claude-haiku-5-5": (0.10, 0.50),
    "claude-sonnet-5-5": (2.00, 10.00),
    "claude-opus-5-5": (4.00, 20.00),
}

model = sys.argv[1] if len(sys.argv) > 1 else "claude-haiku-5-5"
df = pd.read_csv("data/sample_25.csv")
texts = [Path(p).read_text(encoding="utf-8", errors="ignore") for p in df["txt_path"]]


def run(text):
    try:
        result, usage = review_contract(text, model=model)
        return result, usage.input_tokens, usage.output_tokens, None
    except Exception as e:
        return {}, 0, 0, str(e)


print(f"Reviewing {len(df)} contracts with {model}...")
with ThreadPoolExecutor(4) as pool:
    outputs = list(pool.map(run, texts))

# Save Claude's raw answers so we never pay twice for the same run
Path("results").mkdir(exist_ok=True)
raw = [
    {"contract": df.loc[i, "Filename"], "result": res, "tokens_in": t_in, "tokens_out": t_out, "error": err}
    for i, (res, t_in, t_out, err) in enumerate(outputs)
]
Path(f"results/raw_{model}.json").write_text(json.dumps(raw, indent=2))


def norm(s):
    return " ".join(s.split()).lower()


rows, quotes_total, quotes_found = [], 0, 0
for i, (res, _, _, _) in enumerate(outputs):
    for key, risk in RISKS.items():
        entry = res.get(key) or {}
        pred = bool(entry.get("present"))
        truth = df.loc[i, f"{risk['label']}-Answer"] == "Yes"
        rows.append({"contract": df.loc[i, "Filename"], "risk": key, "truth": truth, "predicted": pred})
        for q in entry.get("quotes") or []:
            quotes_total += 1
            quotes_found += norm(q) in norm(texts[i])

details = pd.DataFrame(rows)
details.to_csv(f"results/details_{model}.csv", index=False)

summary = []
for key in RISKS:
    d = details[details.risk == key]
    tp = int((d.truth & d.predicted).sum())
    fp = int((~d.truth & d.predicted).sum())
    fn = int((d.truth & ~d.predicted).sum())
    summary.append({
        "risk": key,
        "caught": f"{tp}/{tp + fn}",
        "false alarms": fp,
        "recall": round(tp / (tp + fn), 2) if tp + fn else None,
        "precision": round(tp / (tp + fp), 2) if tp + fp else None,
    })

t_in = sum(o[1] for o in outputs)
t_out = sum(o[2] for o in outputs)
p_in, p_out = PRICES[model]
cost = t_in / 1e6 * p_in + t_out / 1e6 * p_out
errors = sum(1 for o in outputs if o[3])
all_tp = int((details.truth & details.predicted).sum())
all_pos = int(details.truth.sum())

report = "\n".join([
    f"MODEL: {model} | contracts: {len(df)} | errors: {errors}",
    "",
    pd.DataFrame(summary).to_string(index=False),
    "",
    f"Overall: caught {all_tp}/{all_pos} real risks ({all_tp / all_pos:.0%}) | "
    f"false alarms: {int((~details.truth & details.predicted).sum())} | "
    f"accuracy: {(details.truth == details.predicted).mean():.0%}",
    f"Quotes found word-for-word: {quotes_found}/{quotes_total}"
    + (f" ({quotes_found / quotes_total:.0%})" if quotes_total else ""),
    f"Tokens: {t_in:,} in / {t_out:,} out | cost: ${cost:.3f}",
])
Path(f"results/summary_{model}.txt").write_text(report)
print(report)
