"""
create_db.py
Creates a normalized SQLite database 'school.db' with:
  - students table (id, name, father_name, current_class)
  - marks table   (student_id, class_level, exam_type, subject, marks, max_marks)

Exams per class:
  bimonthly1  → out of 50
  midterm     → out of 100
  bimonthly2  → out of 50
  finals      → out of 100

Subjects: S.St, Urdu, Math, Science, Islamiat, Eng_Text, Eng_Gram, Drawing, Computer
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "school.db")

# ─── Student list (Class 8 → going to Class 9) ────────────────────────────────
STUDENTS = [
    ("Idrees Naimatullah",    "Naimatullah",    8),
    ("Asif Shabbir",          "Shabbir",        8),
    ("Uzair Farooq",          "Farooq",         8),
    ("Usman Pir Zada",        "Pir Zada",       8),
    ("Noman Mehmood Alam",    "Mehmood Alam",   8),
    ("Asmatullah Hafizullah", "Hafizullah",     8),
    ("Abdullah Khalid",       "Khalid",         8),
    ("Umair Bakhtiyar",       "Bakhtiyar",      8),
    ("Attaullah Matiullah",   "Matiullah",      8),
    ("Asfandyar Aman Zaib",   "Aman Zaib",      8),
    ("Hamza Suleman",         "Suleman",        8),
    ("Sakina Habib ur Rehman","Habib ur Rehman",8),
    ("Bushra Anwat Zaib",     "Anwat Zaib",     8),
    ("Fatima Tariq",          "Tariq",          8),
    ("Nida Tariq",            "Tariq",          8),
    ("Urooj Umer Khalid",     "Umer Khalid",    8),
    ("Iqra Peer Muhammad",    "Peer Muhammad",  8),
    ("Umaima Javed",          "Muhammad Javed", 8),
]

SUBJECTS = ["S.St", "Urdu", "Math", "Science", "Islamiat",
            "Eng_Text", "Eng_Gram", "Drawing", "Computer"]

# ─── Class 8 Marks ────────────────────────────────────────────────────────────
# Each row = one student (same order as STUDENTS list)
# Each value = [S.St, Urdu, Math, Science, Islamiat, Eng_Text, Eng_Gram, Drawing, Computer]

CLASS8_BIMONTHLY1 = [  # out of 50
    [34, 41, 29, 36, 44, 38, 33, 46, 31],  # Idrees
    [27, 35, 22, 30, 39, 32, 28, 40, 26],  # Asif
    [45, 42, 48, 44, 46, 47, 43, 49, 45],  # Uzair
    [31, 29, 37, 33, 40, 35, 30, 42, 34],  # Usman
    [47, 46, 49, 48, 45, 44, 46, 50, 47],  # Noman
    [25, 33, 28, 30, 36, 31, 27, 39, 29],  # Asmatullah
    [43, 40, 45, 41, 44, 42, 38, 47, 46],  # Abdullah
    [32, 30, 36, 34, 41, 33, 31, 43, 35],  # Umair
    [29, 34, 31, 32, 38, 36, 35, 41, 30],  # Attaullah
    [48, 45, 50, 47, 49, 48, 44, 50, 49],  # Asfandyar
    [37, 39, 42, 38, 43, 40, 36, 45, 41],  # Hamza
    [49, 48, 46, 47, 50, 49, 47, 50, 46],  # Sakina
    [40, 44, 38, 42, 45, 41, 39, 48, 43],  # Bushra
    [44, 46, 47, 45, 48, 46, 42, 49, 48],  # Fatima
    [33, 37, 39, 35, 42, 38, 34, 44, 40],  # Nida
    [46, 49, 48, 50, 47, 45, 46, 50, 49],  # Urooj
    [28, 32, 30, 27, 37, 29, 33, 40, 28],  # Iqra
    [42, 43, 44, 41, 46, 43, 40, 47, 45],  # Umaima
]

CLASS8_MIDTERM = [  # out of 100
    [78, 85, 69, 74, 88, 81, 76, 90, 72],  # Idrees
    [65, 73, 58, 62, 80, 70, 68, 75, 66],  # Asif
    [82, 79, 91, 84, 86, 88, 83, 92, 89],  # Uzair
    [71, 67, 74, 69, 77, 73, 70, 85, 78],  # Usman
    [88, 90, 95, 92, 91, 87, 89, 93, 94],  # Noman
    [60, 72, 64, 66, 75, 69, 63, 80, 68],  # Asmatullah
    [84, 78, 88, 81, 85, 82, 79, 86, 90],  # Abdullah
    [73, 69, 77, 75, 83, 74, 71, 88, 76],  # Umair
    [68, 74, 70, 72, 79, 76, 73, 82, 69],  # Attaullah
    [90, 87, 93, 89, 92, 91, 88, 95, 96],  # Asfandyar
    [76, 81, 85, 78, 84, 80, 77, 89, 83],  # Hamza
    [92, 94, 89, 91, 95, 93, 90, 97, 88],  # Sakina
    [81, 86, 79, 83, 87, 84, 82, 90, 85],  # Bushra
    [85, 88, 92, 90, 89, 91, 87, 94, 93],  # Fatima
    [74, 77, 80, 76, 82, 79, 75, 86, 81],  # Nida
    [89, 92, 94, 93, 90, 88, 91, 96, 95],  # Urooj
    [70, 75, 72, 68, 78, 73, 74, 84, 71],  # Iqra
    [83, 80, 86, 82, 88, 85, 84, 91, 87],  # Umaima
]

CLASS8_BIMONTHLY2 = [  # out of 50
    [33, 38, 27, 31, 42, 35, 30, 44, 29],  # Idrees
    [26, 32, 21, 28, 37, 30, 25, 39, 24],  # Asif
    [41, 39, 44, 40, 43, 42, 38, 46, 41],  # Uzair
    [30, 28, 34, 32, 36, 31, 29, 40, 33],  # Usman
    [44, 45, 47, 43, 46, 42, 44, 48, 45],  # Noman
    [24, 31, 26, 29, 35, 28, 27, 37, 30],  # Asmatullah
    [39, 36, 42, 38, 41, 40, 34, 45, 43],  # Abdullah
    [32, 30, 35, 33, 38, 34, 31, 41, 36],  # Umair
    [28, 34, 29, 31, 37, 33, 32, 38, 30],  # Attaullah
    [45, 43, 48, 44, 47, 46, 41, 49, 46],  # Asfandyar
    [36, 37, 40, 35, 39, 38, 34, 42, 38],  # Hamza
    [47, 46, 45, 44, 48, 47, 43, 49, 44],  # Sakina
    [38, 40, 36, 39, 42, 37, 35, 46, 40],  # Bushra
    [43, 44, 46, 42, 45, 43, 39, 47, 44],  # Fatima
    [31, 35, 37, 33, 40, 36, 32, 43, 37],  # Nida
    [46, 47, 48, 45, 46, 44, 42, 48, 47],  # Urooj
    [27, 30, 28, 26, 34, 29, 31, 38, 27],  # Iqra
    [40, 41, 43, 39, 44, 40, 36, 45, 42],  # Umaima
]

CLASS8_FINALS = [  # out of 100
    [66, 74, 58, 63, 82, 71, 60, 86, 65],  # Idrees
    [52, 61, 45, 55, 70, 62, 50, 72, 54],  # Asif
    [84, 79, 91, 86, 88, 85, 76, 93, 89],  # Uzair
    [60, 57, 69, 64, 72, 63, 59, 78, 68],  # Usman
    [90, 92, 95, 89, 94, 87, 88, 96, 93],  # Noman
    [48, 59, 53, 57, 68, 55, 52, 70, 58],  # Asmatullah
    [81, 75, 88, 83, 86, 80, 72, 91, 87],  # Abdullah
    [64, 62, 73, 68, 74, 67, 63, 79, 71],  # Umair
    [58, 65, 60, 61, 73, 69, 66, 77, 62],  # Attaullah
    [92, 89, 97, 93, 95, 91, 84, 98, 94],  # Asfandyar
    [72, 76, 80, 74, 78, 75, 70, 85, 79],  # Hamza
    [95, 94, 90, 92, 96, 93, 88, 97, 91],  # Sakina
    [78, 82, 74, 79, 84, 77, 73, 90, 83],  # Bushra
    [87, 88, 93, 89, 90, 86, 79, 94, 92],  # Fatima
    [63, 71, 76, 69, 80, 72, 68, 84, 75],  # Nida
    [91, 93, 96, 94, 92, 88, 85, 97, 95],  # Urooj
    [55, 60, 57, 52, 67, 59, 62, 74, 56],  # Iqra
    [80, 83, 86, 82, 87, 81, 75, 92, 88],  # Umaima
]

# ─── Class 7 & 6 placeholders (will be filled when user provides data) ─────────
CLASS7_BIMONTHLY1 = [  # out of 50
    [36, 49, 16, 28, 42, 39, 38, 41, 49],  # Idrees
    [14, 13, 43, 14, 12, 44, 20, 46, 13],  # Asif
    [11, 45, 29, 21, 44, 26, 49, 17, 15],  # Uzair
    [32, 46, 47, 38, 45, 39, 38, 48, 45],  # Usman
    [22, 40, 10, 50, 24, 28, 45, 18, 46],  # Noman
    [21, 46, 40, 41, 11, 37, 18, 19, 42],  # Asmatullah
    [38, 34, 13, 27, 35, 47, 19, 45, 34],  # Abdullah
    [25, 30, 26, 24, 21, 30, 16, 42, 27],  # Umair
    [25, 29, 15, 12, 41, 35, 15, 29, 10],  # Attaullah
    [41, 42, 14, 45, 27, 48, 44, 34, 38],  # Asfandyar
    [40, 33, 26, 37, 22, 23, 13, 29, 46],  # Hamza
    [25, 46, 17, 14, 42, 40, 19, 12, 46],  # Sakina
    [30, 21, 49, 20, 39, 49, 35, 17, 49],  # Bushra
    [43, 47, 23, 31, 31, 33, 16, 47, 14],  # Fatima
    [44, 16, 31, 20, 33, 37, 17, 24, 16],  # Nida
    [35, 25, 21, 11, 26, 44, 37, 44, 14],  # Urooj
    [48, 48, 20, 26, 40, 46, 15, 42, 43],  # Iqra
    [16, 37, 37, 49, 34, 31, 46, 41, 15],  # Umaima
]

CLASS7_MIDTERM = [  # out of 100
    [68, 75, 59, 62, 72, 57, 60, 63, 70],  # Idrees
    [77, 80, 66, 74, 61, 73, 71, 52, 58],  # Asif
    [60, 48, 55, 63, 54, 67, 59, 62, 51],  # Uzair
    [82, 76, 64, 59, 78, 61, 69, 57, 74],  # Usman
    [71, 67, 76, 69, 64, 56, 63, 60, 55],  # Noman
    [73, 65, 58, 61, 70, 88, 84, 59, 72],  # Asmatullah
    [66, 79, 74, 85, 69, 81, 60, 54, 68],  # Abdullah
    [88, 63, 61, 65, 79, 66, 77, 72, 70],  # Umair
    [72, 84, 81, 69, 90, 74, 62, 83, 87],  # Attaullah
    [69, 72, 55, 67, 74, 60, 64, 79, 63],  # Asfandyar
    [64, 75, 58, 62, 66, 68, 89, 78, 73],  # Hamza
    [61, 59, 63, 70, 67, 64, 72, 74, 60],  # Sakina
    [60, 62, 82, 76, 84, 58, 81, 70, 61],  # Bushra
    [67, 71, 69, 78, 88, 73, 85, 90, 82],  # Fatima
    [63, 80, 69, 60, 72, 68, 74, 77, 76],  # Nida
    [86, 74, 79, 92, 58, 83, 70, 75, 73],  # Urooj
    [89, 78, 72, 76, 54, 65, 80, 69, 84],  # Iqra
    [70, 73, 68, 81, 66, 59, 71, 72, 64],  # Umaima
]

CLASS7_BIMONTHLY2 = [  # out of 50
    [34, 38, 29, 31, 36, 28, 30, 32, 35],  # Idrees
    [39, 40, 33, 37, 30, 36, 35, 26, 29],  # Asif
    [30, 24, 27, 32, 25, 34, 28, 31, 26],  # Uzair
    [41, 38, 32, 29, 39, 30, 34, 28, 37],  # Usman
    [35, 33, 38, 34, 31, 27, 32, 30, 28],  # Noman
    [36, 32, 26, 28, 35, 44, 42, 27, 36],  # Asmatullah
    [33, 39, 37, 43, 34, 41, 30, 25, 34],  # Abdullah
    [44, 31, 30, 32, 39, 33, 38, 36, 35],  # Umair
    [36, 42, 40, 34, 45, 37, 31, 41, 43],  # Attaullah
    [34, 36, 25, 33, 37, 29, 32, 39, 31],  # Asfandyar
    [32, 38, 26, 28, 30, 34, 44, 39, 36],  # Hamza
    [30, 29, 31, 35, 33, 32, 36, 37, 30],  # Sakina
    [30, 31, 41, 38, 42, 27, 40, 35, 29],  # Bushra
    [34, 36, 35, 39, 44, 37, 43, 45, 41],  # Fatima
    [32, 40, 35, 30, 36, 34, 37, 38, 37],  # Nida
    [43, 37, 39, 46, 27, 41, 35, 38, 36],  # Urooj
    [44, 39, 36, 38, 25, 33, 40, 34, 42],  # Iqra
    [35, 37, 34, 40, 32, 29, 36, 36, 33],  # Umaima
]

CLASS7_FINALS = [  # out of 100
    [72, 64, 83, 77, 69, 58, 74, 61, 88],  # Idrees
    [81, 73, 67, 84, 62, 79, 71, 55, 69],  # Asif
    [59, 48, 72, 66, 53, 61, 57, 70, 63],  # Uzair
    [86, 75, 60, 68, 82, 73, 65, 59, 90],  # Usman
    [64, 70, 78, 73, 58, 62, 69, 54, 60],  # Noman
    [77, 66, 55, 63, 74, 91, 85, 52, 71],  # Asmatullah
    [69, 82, 88, 93, 72, 84, 67, 58, 76],  # Abdullah
    [90, 62, 58, 65, 87, 60, 79, 73, 68],  # Umair
    [74, 85, 81, 72, 95, 78, 63, 86, 89],  # Attaullah
    [63, 71, 54, 67, 76, 59, 62, 80, 57],  # Asfandyar
    [56, 74, 52, 61, 64, 70, 92, 75, 83],  # Hamza
    [60, 58, 66, 79, 73, 68, 77, 82, 65],  # Sakina
    [62, 69, 91, 87, 88, 55, 84, 71, 59],  # Bushra
    [75, 80, 73, 89, 94, 76, 90, 93, 85],  # Fatima
    [68, 83, 71, 64, 79, 72, 75, 78, 74],  # Nida
    [92, 76, 85, 97, 57, 88, 70, 81, 79],  # Urooj
    [88, 79, 74, 82, 53, 66, 86, 72, 91],  # Iqra
    [71, 75, 69, 84, 67, 63, 73, 77, 62],  # Umaima
]


CLASS6_BIMONTHLY1 = [  # out of 50
    [24, 45, 17, 39, 36, 35, 43, 34, 48],  # Idrees
    [17, 18, 44, 14, 22, 35, 13, 18, 14],  # Asif
    [42, 29, 25, 41, 42, 29, 40, 19, 33],  # Uzair
    [44, 32, 24, 50, 19, 37, 32, 24, 38],  # Usman
    [16, 45, 41, 35, 28, 27, 28, 29, 27],  # Noman
    [13, 44, 22, 11, 49, 27, 35, 11, 40],  # Asmatullah
    [35, 12, 14, 26, 13, 13, 47, 27, 33],  # Abdullah
    [22, 10, 43, 30, 28, 22, 15, 39, 41],  # Umair
    [10, 19, 40, 24, 33, 34, 36, 45, 29],  # Attaullah
    [46, 11, 28, 21, 39, 49, 27, 37, 50],  # Asfandyar
    [48, 32, 30, 45, 34, 36, 21, 17, 22],  # Hamza
    [28, 34, 45, 10, 49, 38, 34, 10, 42],  # Sakina
    [18, 12, 36, 23, 48, 46, 17, 33, 13],  # Bushra
    [14, 49, 47, 10, 49, 29, 28, 25, 31],  # Fatima
    [23, 14, 10, 45, 19, 21, 26, 13, 48],  # Nida
    [36, 49, 21, 47, 42, 33, 49, 17, 37],  # Urooj
    [46, 15, 45, 32, 30, 43, 33, 13, 50],  # Iqra
    [41, 12, 33, 26, 26, 28, 10, 21, 15],  # Umaima
]

CLASS6_MIDTERM = [  # out of 100
    [55, 59, 38, 83, 50, 63, 32, 99, 58],  # Idrees
    [28, 38, 91, 68, 85, 80, 67, 90, 78],  # Asif
    [85, 53, 33, 69, 58, 36, 96, 56, 78],  # Uzair
    [90, 98, 87, 37, 24, 68, 80, 61, 50],  # Usman
    [95, 34, 49, 60, 48, 24, 44, 38, 79],  # Noman
    [43, 41, 60, 32, 92, 75, 37, 85, 72],  # Asmatullah
    [90, 72, 22, 92, 54, 58, 59, 57, 57],  # Abdullah
    [27, 78, 65, 54, 64, 61, 89, 61, 89],  # Umair
    [68, 53, 47, 57, 77, 63, 84, 27, 51],  # Attaullah
    [81, 94, 56, 36, 87, 75, 22, 49, 47],  # Asfandyar
    [41, 88, 42, 77, 35, 58, 99, 30, 79],  # Hamza
    [97, 87, 99, 78, 41, 65, 91, 91, 87],  # Sakina
    [26, 89, 69, 53, 44, 43, 51, 41, 76],  # Bushra
    [87, 87, 52, 61, 88, 95, 58, 63, 28],  # Fatima
    [55, 54, 85, 32, 53, 60, 77, 87, 35],  # Nida
    [50, 28, 49, 35, 50, 98, 60, 91, 30],  # Urooj
    [45, 20, 45, 32, 53, 29, 36, 43, 72],  # Iqra
    [68, 66, 74, 52, 44, 80, 56, 65, 28],  # Umaima
]

CLASS6_BIMONTHLY2 = [  # out of 50
    [16, 35, 12, 15, 16, 10, 11, 14, 47],  # Idrees
    [42, 22, 30, 49, 46, 15, 49, 19, 30],  # Asif
    [40, 40, 14, 18, 44, 49, 45, 44, 40],  # Uzair
    [22, 27, 41, 44, 35, 40, 41, 19, 23],  # Usman
    [36, 28, 33, 34, 28, 20, 49, 35, 45],  # Noman
    [13, 40, 34, 47, 12, 27, 25, 20, 41],  # Asmatullah
    [33, 20, 37, 28, 28, 34, 33, 33, 33],  # Abdullah
    [34, 12, 32, 43, 41, 24, 13, 34, 26],  # Umair
    [16, 17, 13, 50, 48, 22, 49, 30, 47],  # Attaullah
    [19, 35, 26, 28, 48, 50, 48, 12, 25],  # Asfandyar
    [46, 29, 35, 10, 25, 20, 27, 18, 35],  # Hamza
    [20, 46, 10, 10, 50, 46, 14, 44, 32],  # Sakina
    [14, 19, 28, 31, 23, 49, 21, 43, 15],  # Bushra
    [19, 43, 48, 39, 24, 40, 20, 31, 31],  # Fatima
    [33, 45, 49, 25, 50, 18, 38, 22, 24],  # Nida
    [25, 44, 45, 37, 29, 40, 43, 46, 40],  # Urooj
    [46, 28, 14, 41, 11, 19, 35, 26, 18],  # Iqra
    [30, 30, 34, 13, 11, 21, 48, 17, 34],  # Umaima
]

CLASS6_FINALS = [  # out of 100
    [86,  52, 39, 37,  45, 84, 49, 69, 75],  # Idrees
    [40,  79, 33, 41, 100, 99, 55, 45, 90],  # Asif
    [96, 100, 22, 52,  95, 90, 59, 50, 76],  # Uzair
    [55,  89, 70, 74,  53, 53, 31, 37, 91],  # Usman
    [77,  83, 74,100,  61, 56, 27, 52, 97],  # Noman
    [92,  86, 42, 62,  51, 37, 87, 94, 21],  # Asmatullah
    [34,  28, 57, 90,  49, 46, 56, 66, 90],  # Abdullah
    [75,  43, 92, 27,  79, 79, 41, 35, 56],  # Umair
    [34,  80, 90, 89,  48, 61, 91, 65, 25],  # Attaullah
    [20,  23, 75, 20,  48, 51, 53, 99, 89],  # Asfandyar
    [97,  32, 27, 75,  31, 70, 87, 79, 77],  # Hamza
    [44,  85, 67, 35,  80, 79, 73, 33, 85],  # Sakina
    [100, 37, 85, 30,  26, 84, 73, 33, 32],  # Bushra
    [75,  64, 49, 24,  37, 41, 68, 95, 97],  # Fatima
    [99,  79, 67, 96,  80, 95, 80, 97, 83],  # Nida
    [45,  49, 32, 78,  40, 41, 46, 96, 87],  # Urooj
    [74,  59, 36, 34,  90, 29, 27, 28, 36],  # Iqra
    [90,  51, 28, 87,  90, 51, 52, 91, 64],  # Umaima
]

# ─── DB Builder ───────────────────────────────────────────────────────────────

def insert_marks(cursor, student_id, class_level, exam_type, max_marks, data_row):
    for subject, mark in zip(SUBJECTS, data_row):
        cursor.execute("""
            INSERT INTO marks (student_id, class_level, exam_type, subject, marks, max_marks)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (student_id, class_level, exam_type, subject, mark, max_marks))


def build_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()

    # ── Schema ────────────────────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE students (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            name         TEXT NOT NULL,
            father_name  TEXT NOT NULL,
            current_class INTEGER NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE marks (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id  INTEGER NOT NULL REFERENCES students(id),
            class_level INTEGER NOT NULL,   -- 6, 7, or 8
            exam_type   TEXT    NOT NULL,   -- bimonthly1 | midterm | bimonthly2 | finals
            subject     TEXT    NOT NULL,
            marks       INTEGER NOT NULL,
            max_marks   INTEGER NOT NULL    -- 50 or 100
        )
    """)

    cur.execute("CREATE INDEX idx_marks_student ON marks(student_id, class_level)")

    # ── Insert students ────────────────────────────────────────────────────────
    cur.executemany(
        "INSERT INTO students (name, father_name, current_class) VALUES (?, ?, ?)",
        STUDENTS
    )
    conn.commit()

    # Fetch assigned IDs in insertion order
    cur.execute("SELECT id FROM students ORDER BY id")
    student_ids = [row[0] for row in cur.fetchall()]

    # ── Insert Class 8 marks ───────────────────────────────────────────────────
    exam_map_8 = [
        ("bimonthly1", 50,  CLASS8_BIMONTHLY1),
        ("midterm",    100, CLASS8_MIDTERM),
        ("bimonthly2", 50,  CLASS8_BIMONTHLY2),
        ("finals",     100, CLASS8_FINALS),
    ]
    for exam_type, max_marks, data in exam_map_8:
        for sid, row in zip(student_ids, data):
            insert_marks(cur, sid, 8, exam_type, max_marks, row)

    # ── Insert Class 7 marks (when available) ─────────────────────────────────
    if CLASS7_BIMONTHLY1:
        exam_map_7 = [
            ("bimonthly1", 50,  CLASS7_BIMONTHLY1),
            ("midterm",    100, CLASS7_MIDTERM),
            ("bimonthly2", 50,  CLASS7_BIMONTHLY2),
            ("finals",     100, CLASS7_FINALS),
        ]
        for exam_type, max_marks, data in exam_map_7:
            for sid, row in zip(student_ids, data):
                insert_marks(cur, sid, 7, exam_type, max_marks, row)

    # ── Insert Class 6 marks ───────────────────────────────────────────────────
    if CLASS6_BIMONTHLY1:
        exam_map_6 = [
            ("bimonthly1", 50,  CLASS6_BIMONTHLY1),
            ("midterm",    100, CLASS6_MIDTERM),
            ("bimonthly2", 50,  CLASS6_BIMONTHLY2),
            ("finals",     100, CLASS6_FINALS),
        ]
        for exam_type, max_marks, data in exam_map_6:
            for sid, row in zip(student_ids, data):
                insert_marks(cur, sid, 6, exam_type, max_marks, row)

    conn.commit()
    conn.close()

    # ── Summary ────────────────────────────────────────────────────────────────
    conn2 = sqlite3.connect(DB_PATH)
    cur2  = conn2.cursor()
    cur2.execute("SELECT COUNT(*) FROM students")
    n_students = cur2.fetchone()[0]
    cur2.execute("SELECT COUNT(*) FROM marks")
    n_marks = cur2.fetchone()[0]
    conn2.close()

    print(f"[OK] school.db created at: {DB_PATH}")
    print(f"     Students : {n_students}")
    print(f"     Mark rows: {n_marks}")
    print(f"     Classes stored: 8" +
          (" 7" if CLASS7_BIMONTHLY1 else "") +
          (" 6" if CLASS6_BIMONTHLY1 else ""))


if __name__ == "__main__":
    build_db()
