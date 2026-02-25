import sqlite3
conn = sqlite3.connect("school.db")
cur  = conn.cursor()

print("=== STUDENTS ===")
for row in cur.execute("SELECT id, name, father_name, current_class FROM students"):
    print(row)

print("\n=== MARKS COUNT PER EXAM ===")
q = "SELECT class_level, exam_type, COUNT(*)/9 FROM marks GROUP BY class_level, exam_type"
for row in cur.execute(q):
    print(f"  Class {row[0]} | {row[1]:12s} | {row[2]} students")

print("\n=== Sakina - Class 8 Finals ===")
q2 = """SELECT subject, marks, max_marks FROM marks
        WHERE student_id=(SELECT id FROM students WHERE name='Sakina Habib ur Rehman')
          AND class_level=8 AND exam_type='finals'"""
for r in cur.execute(q2):
    print(f"  {r[0]:12s}: {r[1]}/{r[2]}")

conn.close()
