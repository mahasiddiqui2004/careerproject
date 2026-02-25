"""
make_training_data.py
Generates synthetic training data for the 3-stream career recommendation model.
Features: per-subject average % across all classes (9 subjects)
Label: Biology | Computer Science | Commerce
"""

import numpy as np
import pandas as pd
import random

random.seed(42)
np.random.seed(42)

SUBJECTS = ["Math", "Science", "Computer", "Urdu", "S_St",
            "Eng_Text", "Eng_Gram", "Drawing", "Islamiat"]

def rand(lo, hi):
    return round(random.uniform(lo, hi), 1)

def gen_student(stream):
    """
    Generate realistic per-subject averages (%) for a student.
    Each stream has a distinct strength profile with some noise.
    """
    if stream == "Biology":
        return {
            "Math":     rand(55, 92),
            "Science":  rand(72, 99),   # primary strength
            "Computer": rand(35, 68),
            "Urdu":     rand(52, 88),
            "S_St":     rand(48, 82),
            "Eng_Text": rand(58, 90),
            "Eng_Gram": rand(55, 88),
            "Drawing":  rand(50, 85),
            "Islamiat": rand(58, 92),
            "stream":   stream,
        }
    elif stream == "Computer Science":
        return {
            "Math":     rand(72, 99),   # primary strength
            "Science":  rand(55, 86),
            "Computer": rand(70, 99),   # primary strength
            "Urdu":     rand(45, 78),
            "S_St":     rand(40, 72),
            "Eng_Text": rand(52, 84),
            "Eng_Gram": rand(50, 82),
            "Drawing":  rand(42, 74),
            "Islamiat": rand(52, 84),
            "stream":   stream,
        }
    else:  # Commerce
        return {
            "Math":     rand(58, 90),
            "Science":  rand(38, 70),
            "Computer": rand(38, 68),
            "Urdu":     rand(65, 96),   # primary strength
            "S_St":     rand(68, 97),   # primary strength
            "Eng_Text": rand(60, 90),
            "Eng_Gram": rand(58, 88),
            "Drawing":  rand(48, 78),
            "Islamiat": rand(60, 92),
            "stream":   stream,
        }

# 200 students per stream = 600 total
rows = []
for stream in ["Biology", "Computer Science", "Commerce"]:
    for _ in range(200):
        rows.append(gen_student(stream))

df = pd.DataFrame(rows)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)  # shuffle

df.to_csv("training_data.csv", index=False)
print(f"[OK] training_data.csv created: {len(df)} rows")
print(df["stream"].value_counts().to_string())
