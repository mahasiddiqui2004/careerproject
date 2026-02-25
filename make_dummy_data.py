import pandas as pd
import numpy as np
import random

random.seed(42)
np.random.seed(42)

male_first = ["Muhammad", "Ahmed", "Ali", "Hassan", "Hussain", "Umar", "Usman", "Abdullah",
              "Abdul Rehman", "Abdul Hadi", "Abdul Wahab", "Abdul Rafay", "Abdul Moiz",
              "Bilal", "Hamza", "Zain", "Zayan", "Ayaan", "Rayyan", "Daniyal", "Saad",
              "Talha", "Huzaifa", "Ibrahim", "Musa", "Yousuf", "Haris", "Faizan", "Taha"]

female_first = ["Ayesha", "Fatima", "Zainab", "Maryam", "Khadija", "Hania", "Eman", "Iqra",
                "Laiba", "Mahnoor", "Dua", "Amna", "Hira", "Noor", "Anaya", "Zara", "Alina",
                "Sana", "Rabia", "Hafsa", "Aleena", "Aiza", "Hoorain", "Minahil", "Aqsa"]

all_first_names = male_first + female_first
last_names = ["Khan", "Ahmed", "Ali", "Shah", "Raja", "Malik", "Qureshi", "Butt", "Mirza", "Chaudhry", "Ansari", "Siddiqui", "Baig", "Sheikh", "Jutt", "Dogar", "Wattoo", "Rehman", "Aziz", "Mehmood"]

names = []
used = set()

while len(names) < 100:
    first = random.choice(all_first_names)
    last = random.choice(last_names)
    name = f"{first} {last}"
    
    if name not in used:
        used.add(name)
        names.append(name)

student_ids = [f"S{i:04d}" for i in range(1001, 1101)]

subjects = ["Math", "Science", "English", "Urdu", "Social Studies"]

data = {
    "student_id": student_ids,
    "student_name": names
}

for year in [6, 7, 8]:
    for sub in subjects:
        col_name = f"{sub}_{year}"
        marks = np.random.randint(42, 99, size=100)
        data[col_name] = marks

def choose_stream(row):
    # Weighted Average: Class 8 matters most (50%), then 7 (30%), then 6 (20%)
    math_avg = (row["Math_6"] * 0.2) + (row["Math_7"] * 0.3) + (row["Math_8"] * 0.5)
    sci_avg  = (row["Science_6"] * 0.2) + (row["Science_7"] * 0.3) + (row["Science_8"] * 0.5)
    
    # Original logic was strict (>78). New logic is more realistic.
    # If Math is good and Science is decent -> Computer Science
    if math_avg > 70 and sci_avg > 60:
        return "Computer Science"
    # If Science is good (but Math might be lower) -> Biology
    elif sci_avg > 70:
        return "Biology"
    # Otherwise -> Commerce
    else:
        return "Commerce"

df = pd.DataFrame(data)
df["recommended_stream"] = df.apply(choose_stream, axis=1)

df.to_csv("students_data_100.csv", index=False)

print("Done! File created: students_data_100.csv")
print("Total students:", len(df))
print("\nFirst 6 students:\n")
print(df.head(6))
print("\nStream counts:\n")
print(df["recommended_stream"].value_counts())