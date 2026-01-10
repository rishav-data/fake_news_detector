import os
import pandas as pd
import torch
import numpy as np

from torch.utils.data import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments
)
from sklearn.metrics import accuracy_score

# --------------------------------------------------
# Paths
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TRAIN_PATH = os.path.join(BASE_DIR, "..", "data", "train.csv")
VAL_PATH   = os.path.join(BASE_DIR, "..", "data", "val.csv")
TEST_PATH  = os.path.join(BASE_DIR, "..", "data", "test.csv")

MODEL_OUTPUT_DIR = os.path.join(BASE_DIR, "bert_news_model")

# --------------------------------------------------
# Labels
# --------------------------------------------------
LABELS = ["Neutral", "Biased", "Contradictory"]
LABEL2ID = {label: idx for idx, label in enumerate(LABELS)}
ID2LABEL = {idx: label for label, idx in LABEL2ID.items()}

MODEL_NAME = "bert-base-uncased"

# --------------------------------------------------
# Safe CSV Loader (comma-proof)
# --------------------------------------------------
def load_csv_safe(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()

            if not line or line.lower().startswith("text,label"):
                continue

            if "," not in line:
                continue

            # split ONLY on last comma
            text, label = line.rsplit(",", 1)
            text = text.strip()
            label = label.strip()

            if label not in LABEL2ID:
                continue

            rows.append({"text": text, "label": label})

    if not rows:
        raise ValueError(f"No valid rows found in {path}")

    return pd.DataFrame(rows)

# --------------------------------------------------
# Dataset class
# --------------------------------------------------
class NewsDataset(Dataset):
    def __init__(self, texts, labels, tokenizer):
        self.encodings = tokenizer(
            texts,
            truncation=True,
            padding=True,
            max_length=512
        )
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        item = {k: torch.tensor(v[idx]) for k, v in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item

# --------------------------------------------------
# Load datasets
# --------------------------------------------------
train_df = load_csv_safe(TRAIN_PATH)
val_df   = load_csv_safe(VAL_PATH)
test_df  = load_csv_safe(TEST_PATH)

for name, df in [("train", train_df), ("val", val_df), ("test", test_df)]:
    df["label_id"] = df["label"].map(LABEL2ID)
    if df["label_id"].isnull().any():
        raise ValueError(f"Invalid labels detected in {name}.csv")

print("Train samples:", len(train_df))
print("Val samples:", len(val_df))
print("Test samples:", len(test_df))
print(train_df["label"].value_counts())

# --------------------------------------------------
# Tokenizer
# --------------------------------------------------
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

train_dataset = NewsDataset(
    train_df["text"].tolist(),
    train_df["label_id"].tolist(),
    tokenizer
)

val_dataset = NewsDataset(
    val_df["text"].tolist(),
    val_df["label_id"].tolist(),
    tokenizer
)

test_dataset = NewsDataset(
    test_df["text"].tolist(),
    test_df["label_id"].tolist(),
    tokenizer
)

# --------------------------------------------------
# Model
# --------------------------------------------------
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=len(LABELS),
    id2label=ID2LABEL,
    label2id=LABEL2ID
)

# --------------------------------------------------
# Metrics
# --------------------------------------------------
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=1)
    return {"accuracy": accuracy_score(labels, preds)}

# --------------------------------------------------
# Training arguments
# --------------------------------------------------
training_args = TrainingArguments(
    output_dir=MODEL_OUTPUT_DIR,
    do_train=True,
    do_eval=True,
    logging_dir=os.path.join(BASE_DIR, "logs"),
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    save_total_limit=2
)


# --------------------------------------------------
# Trainer
# --------------------------------------------------
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

# --------------------------------------------------
# Train
# --------------------------------------------------
trainer.train()

# --------------------------------------------------
# Evaluate on TEST set
# --------------------------------------------------
print("\n📊 Evaluating on TEST set...")
test_metrics = trainer.evaluate(test_dataset)
print(test_metrics)

# --------------------------------------------------
# Save model
# --------------------------------------------------
trainer.save_model(MODEL_OUTPUT_DIR)
tokenizer.save_pretrained(MODEL_OUTPUT_DIR)

print(f"\n✅ Model saved to: {MODEL_OUTPUT_DIR}")
