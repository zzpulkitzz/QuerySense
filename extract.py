from datasets import load_dataset
from collections import defaultdict
import random
import json

# 1️⃣ Load the dataset
dataset = load_dataset("milistu/AMAZON-Products-2023", split="train")  # streaming

# 2️⃣ Count categories and initialize buckets
buckets = defaultdict(list)
for example in dataset:
    filename = example["filename"]
    buckets[filename].append(example)
    if sum(len(v) for v in buckets.values()) >= 10000:
        break

total_per_bucket = {k: len(v) for k, v in buckets.items()}
print("Collected so far:", total_per_bucket)

# 3️⃣ Uniform sampling across categories
n_total = 500
n_categories = len(buckets)
n_per_cat = n_total // n_categories

sampled = []
for cat, items in buckets.items():
    sample = random.sample(items, min(len(items), n_per_cat))
    sampled.extend(sample)

print("Final sampling:", {cat: sum(1 for x in sampled if x["filename"] == cat)
                          for cat in buckets})
def convert(obj):
    """Recursively convert timestamps and other unserializable objects to strings."""
    if isinstance(obj, dict):
        obj = {k: convert(v) for k, v in obj.items() if k != "embeddings"}
        return obj
    elif isinstance(obj, list):
        return [convert(i) for i in obj]
    elif hasattr(obj, "isoformat"):  # Handles Timestamp or datetime
        return obj.isoformat()
    else:
        return obj
# 4️⃣ Save sampled output
