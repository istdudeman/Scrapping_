import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from tqdm import tqdm
import json

# ✅ Load dataset
df = pd.read_csv("reddit_tuntutan178_indonesia.csv")
print(f"Loaded {len(df)} posts")

# ✅ Load IndoBERT sentiment model
model_name = "w11wo/indonesian-roberta-base-sentiment-classifier"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# ✅ Function for sentiment prediction
def predict_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        label_id = torch.argmax(probs).item()
        labels = ["negative", "neutral", "positive"]
        return labels[label_id]

# ✅ Apply to dataset (title + body combined)
tqdm.pandas()
df["content"] = (df["title"].fillna("") + " " + df["text"].fillna("")).str.strip()
df["sentiment"] = df["content"].progress_apply(predict_sentiment)

# ✅ Save results to CSV
csv_path = "reddit_tuntutan178_sentiment.csv"
df.to_csv(csv_path, index=False, encoding="utf-8-sig")
print(f"✅ Sentiment analysis complete. Saved to {csv_path}")

# ✅ Convert to JSON
json_path = "reddit_tuntutan178_sentiment.json"
df.to_json(json_path, orient="records", force_ascii=False, indent=2)
print(f"📁 JSON file saved to {json_path}")

# ✅ Print summary
print("\n📊 Sentiment distribution:")
print(df["sentiment"].value_counts())

# ✅ Print first 5 sentiment results as JSON preview
preview_json = df[["title", "sentiment"]].head(5).to_dict(orient="records")
print("\n🔎 JSON preview of first 5 results:")
print(json.dumps(preview_json, indent=2, ensure_ascii=False))
