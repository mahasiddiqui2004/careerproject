"""
app.py  –  AI Career Guidance System
Fetches student marks from school.db (normalized schema) and shows:
  • A full report card (per-subject, per-exam, per-class)
  • AI recommendation with a 3-4 line explanation
"""

import streamlit as st
import sqlite3
import pandas as pd
import pickle
import csv
import os
from datetime import datetime

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Career Guidance",
    page_icon="🎓",
    layout="wide",
)

# ─── CSS Styling ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.main { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); min-height: 100vh; }

.report-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 24px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
}
.student-name {
    font-size: 2rem; font-weight: 700; color: #e2e8f0; margin: 0;
    background: linear-gradient(90deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.student-meta { color: #94a3b8; font-size: 0.9rem; margin-top: 6px; }

.class-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 18px;
}
.class-title {
    font-size: 1.05rem; font-weight: 600;
    color: #a78bfa; margin-bottom: 14px;
    border-bottom: 1px solid rgba(167,139,250,0.25);
    padding-bottom: 8px;
}

.marks-grid { width: 100%; border-collapse: collapse; }
.marks-grid th {
    background: rgba(96,165,250,0.15);
    color: #93c5fd; font-size: 0.78rem;
    font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.05em; padding: 8px 10px; text-align: center;
}
.marks-grid td {
    color: #e2e8f0; font-size: 0.88rem;
    padding: 7px 10px; text-align: center;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.marks-grid tr:last-child td { border-bottom: none; }
.marks-grid td:first-child { text-align: left; color: #cbd5e1; font-weight: 500; }

.mark-high { color: #4ade80 !important; font-weight: 600; }
.mark-mid  { color: #facc15 !important; }
.mark-low  { color: #f87171 !important; }

.ai-card {
    background: linear-gradient(135deg, rgba(167,139,250,0.12), rgba(96,165,250,0.08));
    border: 1px solid rgba(167,139,250,0.35);
    border-radius: 16px;
    padding: 28px 32px;
    margin-top: 10px;
}
.ai-badge {
    display: inline-block;
    background: linear-gradient(90deg, #7c3aed, #2563eb);
    color: white; font-size: 0.75rem; font-weight: 700;
    padding: 4px 14px; border-radius: 20px;
    letter-spacing: 0.08em; margin-bottom: 14px;
    text-transform: uppercase;
}
.ai-stream {
    font-size: 1.7rem; font-weight: 700; color: #e2e8f0;
    margin: 6px 0 16px 0;
    background: linear-gradient(90deg, #a78bfa, #34d399);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.ai-reason {
    color: #cbd5e1; font-size: 0.95rem; line-height: 1.7;
    border-left: 3px solid #a78bfa;
    padding-left: 16px;
}

.stat-pill {
    display: inline-block; background: rgba(96,165,250,0.15);
    border: 1px solid rgba(96,165,250,0.3);
    color: #93c5fd; border-radius: 20px;
    padding: 3px 12px; font-size: 0.8rem; margin: 2px;
}
</style>
""", unsafe_allow_html=True)

# ─── DB Helpers ───────────────────────────────────────────────────────────────
SUBJECTS = ["S.St", "Urdu", "Math", "Science", "Islamiat",
            "Eng_Text", "Eng_Gram", "Drawing", "Computer"]

SUBJECT_LABELS = {
    "S.St": "Social Studies", "Urdu": "Urdu",
    "Math": "Mathematics", "Science": "Science",
    "Islamiat": "Islamiat", "Eng_Text": "English (Text)",
    "Eng_Gram": "English (Grammar)", "Drawing": "Drawing",
    "Computer": "Computer"
}

EXAM_ORDER  = ["bimonthly1", "midterm", "bimonthly2", "finals"]
EXAM_LABELS = {
    "bimonthly1": "Bimonthly 1\n(/50)",
    "midterm":    "Midterm\n(/100)",
    "bimonthly2": "Bimonthly 2\n(/50)",
    "finals":     "Finals\n(/100)",
}
EXAM_MAX = {"bimonthly1": 50, "midterm": 100, "bimonthly2": 50, "finals": 100}


@st.cache_data
def get_all_students():
    conn = sqlite3.connect("school.db")
    cur  = conn.cursor()
    cur.execute("SELECT id, name, father_name, current_class FROM students ORDER BY name")
    rows = cur.fetchall()
    conn.close()
    return rows   # [(id, name, father_name, current_class), ...]


@st.cache_data
def get_student_marks(student_id):
    """Returns dict: {class_level: {exam_type: {subject: marks}}}"""
    conn = sqlite3.connect("school.db")
    cur  = conn.cursor()
    cur.execute("""
        SELECT class_level, exam_type, subject, marks, max_marks
        FROM marks WHERE student_id = ?
        ORDER BY class_level, exam_type, subject
    """, (student_id,))
    rows = cur.fetchall()
    conn.close()

    data = {}
    for cls, exam, subj, mrk, mx in rows:
        data.setdefault(cls, {}).setdefault(exam, {})[subj] = (mrk, mx)
    return data


# ─── AI Helpers ───────────────────────────────────────────────────────────────
def compute_avg(marks_dict, classes, subjects):
    """Average percentage across given classes and subjects."""
    total, count = 0, 0
    for cls in classes:
        for exam, subs in marks_dict.get(cls, {}).items():
            for sub in subjects:
                if sub in subs:
                    mrk, mx = subs[sub]
                    total += (mrk / mx) * 100
                    count += 1
    return round(total / count, 1) if count else 0


# Model feature names (match training_data.csv)
MODEL_FEATURES = ["Math", "Science", "Computer", "Urdu", "S_St",
                  "Eng_Text", "Eng_Gram", "Drawing", "Islamiat"]

# DB subject name → model feature name
SUBJ_TO_FEAT = {
    "Math": "Math", "Science": "Science", "Computer": "Computer",
    "Urdu": "Urdu", "S.St": "S_St", "Eng_Text": "Eng_Text",
    "Eng_Gram": "Eng_Gram", "Drawing": "Drawing", "Islamiat": "Islamiat",
}

@st.cache_resource
def load_model():
    with open("career_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("career_label_encoder.pkl", "rb") as f:
        le = pickle.load(f)
    return model, le


def get_recommendation(marks_dict):
    """
    ML-based recommendation using trained Random Forest.
    Features = per-subject average % across all classes and exams.
    """
    classes = sorted(marks_dict.keys())

    # Compute per-subject average %
    avgs = {}
    for sub in SUBJECTS:
        avgs[sub] = compute_avg(marks_dict, classes, [sub])
    eng_avg  = compute_avg(marks_dict, classes, ["Eng_Text", "Eng_Gram"])
    overall  = compute_avg(marks_dict, classes, SUBJECTS)

    # Build feature vector in model's expected order
    features = {feat: avgs.get(db_sub, 0)
                for db_sub, feat in SUBJ_TO_FEAT.items()}
    import pandas as _pd
    X = _pd.DataFrame([features])[MODEL_FEATURES]

    # Predict
    model, le = load_model()
    pred_enc   = model.predict(X)[0]
    stream     = le.inverse_transform([pred_enc])[0]
    proba      = model.predict_proba(X)[0]
    confidence = round(max(proba) * 100, 1)

    # Scores dict for bar chart (probabilities × 100)
    scores = {cls: round(p * 100, 1)
              for cls, p in zip(le.classes_, proba)}

    math_avg = avgs["Math"]
    sci_avg  = avgs["Science"]
    comp_avg = avgs["Computer"]
    urdu_avg = avgs["Urdu"]
    sst_avg  = avgs["S.St"]
    draw_avg = avgs["Drawing"]

    reasons = {
        "Biology": (
            f"The AI model analysed this student's performance across all classes and identified "
            f"Science (<b>{sci_avg}%</b>) and Math (<b>{math_avg}%</b>) as their dominant strengths. "
            f"These are the core pillars of Biology and Pre-Medical studies. "
            f"This stream opens the path to medicine, pharmacy, and health sciences — "
            f"with a model confidence of <b>{confidence}%</b>."
        ),
        "Computer Science": (
            f"After analysing marks across classes 6–8, the AI model found that this student excels "
            f"in Computer (<b>{comp_avg}%</b>) and Mathematics (<b>{math_avg}%</b>) — "
            f"the two core competencies for Computer Science. "
            f"Their technical aptitude makes them a strong fit for software, programming, and IT careers. "
            f"Model confidence: <b>{confidence}%</b>."
        ),
        "Commerce": (
            f"The AI model identified a strong balanced profile across Social Studies (<b>{sst_avg}%</b>), "
            f"Urdu (<b>{urdu_avg}%</b>), and Mathematics (<b>{math_avg}%</b>). "
            f"This makes Commerce the ideal fit — opening doors to Accounting, Economics, "
            f"Business Management, and Finance. Model confidence: <b>{confidence}%</b>."
        ),
    }

    return stream, reasons[stream], scores, {
        "math": math_avg, "science": sci_avg, "computer": comp_avg,
        "urdu": urdu_avg, "sst": sst_avg, "english": eng_avg,
        "drawing": draw_avg, "overall": overall
    }


# ─── Mark colour helper ────────────────────────────────────────────────────────
def mark_class(mrk, mx):
    pct = (mrk / mx) * 100
    if pct >= 70: return "mark-high"
    if pct >= 45: return "mark-mid"
    return "mark-low"


# ─── Build HTML report card table for one class ───────────────────────────────
def build_class_table(class_data):
    """Returns an HTML table string for one class level."""
    available_exams = [e for e in EXAM_ORDER if e in class_data]
    headers = "<th>Subject</th>" + "".join(
        f"<th>{EXAM_LABELS[e].replace(chr(10), ' ')}</th>" for e in available_exams
    )
    rows_html = ""
    for sub in SUBJECTS:
        label = SUBJECT_LABELS[sub]
        cells = f"<td>{label}</td>"
        for exam in available_exams:
            if sub in class_data.get(exam, {}):
                mrk, mx = class_data[exam][sub]
                css = mark_class(mrk, mx)
                cells += f'<td class="{css}">{mrk}<span style="color:#64748b;font-size:0.75rem">/{mx}</span></td>'
            else:
                cells += "<td>—</td>"
        rows_html += f"<tr>{cells}</tr>"

    return f"""
<table class="marks-grid">
  <thead><tr>{headers}</tr></thead>
  <tbody>{rows_html}</tbody>
</table>
"""


# ─── App UI ───────────────────────────────────────────────────────────────────
st.markdown("## 🎓 AI Career Guidance System")
st.markdown("---")

students = get_all_students()
student_names = [f"{s[1]}" for s in students]
student_map   = {s[1]: s for s in students}  # name → (id, name, father, class)

col_search, col_spacer = st.columns([2, 3])
with col_search:
    query = st.text_input("Write student name", placeholder="e.g. Sakina, Noman, Urooj...")

if not query:
    st.info("Type a student name above to see their report card.")
    st.stop()

matches = [n for n in student_names if query.lower() in n.lower()]

if not matches:
    st.warning("No student found. Check the spelling and try again.")
    st.stop()

selected = next((n for n in matches if n.lower() == query.lower()), matches[0])

if len(matches) > 1:
    st.caption(f"Showing: **{selected}** ({len(matches)} matches found)")

student_row = student_map[selected]
sid, sname, father, curr_class = student_row

marks_dict = get_student_marks(sid)
stream, reason, all_scores, avgs = get_recommendation(marks_dict)

# ── Save to CSV log ─────────────────────────────────────────────────────────
LOG_FILE = "recommendations_log.csv"
log_exists = os.path.exists(LOG_FILE)
with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    if not log_exists:
        writer.writerow(["Date", "Time", "Student Name", "Father Name",
                         "Recommended Stream", "Confidence %",
                         "Math %", "Science %", "Computer %",
                         "Urdu %", "S.St %", "English %", "Drawing %", "Overall %"])
    writer.writerow([
        datetime.now().strftime("%Y-%m-%d"),
        datetime.now().strftime("%H:%M:%S"),
        sname, father, stream,
        max(all_scores.values()),
        avgs["math"], avgs["science"], avgs["computer"],
        avgs["urdu"], avgs["sst"], avgs["english"], avgs["drawing"], avgs["overall"]
    ])

# ── Header ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="report-header">
  <p class="student-name">{sname}</p>
  <p class="student-meta">
    Father: <strong style="color:#e2e8f0">{father}</strong>
    &nbsp;|&nbsp; Current Class: <strong style="color:#e2e8f0">Class {curr_class}</strong>
    &nbsp;|&nbsp; Overall Average: <strong style="color:#a78bfa">{avgs['overall']}%</strong>
  </p>
  <div style="margin-top:10px">
    <span class="stat-pill">Math {avgs['math']}%</span>
    <span class="stat-pill">Science {avgs['science']}%</span>
    <span class="stat-pill">Computer {avgs['computer']}%</span>
    <span class="stat-pill">Urdu {avgs['urdu']}%</span>
    <span class="stat-pill">S.St {avgs['sst']}%</span>
    <span class="stat-pill">English {avgs['english']}%</span>
    <span class="stat-pill">Drawing {avgs['drawing']}%</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Report Card ─────────────────────────────────────────────────────────────
st.markdown("### 📋 Academic Report Card")

classes = sorted(marks_dict.keys())
tabs = st.tabs([f"Class {c}" for c in classes])

for tab, cls in zip(tabs, classes):
    with tab:
        table_html = build_class_table(marks_dict[cls])
        st.markdown(f'<div class="class-card"><div class="class-title">Class {cls} — Subject-wise Results</div>{table_html}</div>',
                    unsafe_allow_html=True)

# ── AI Recommendation ───────────────────────────────────────────────────────
st.markdown("### 🤖 AI Recommendation")

# Stream score bar chart
score_df = pd.DataFrame({
    "Stream": list(all_scores.keys()),
    "Score":  [round(v, 1) for v in all_scores.values()]
}).sort_values("Score", ascending=True)

col_rec, col_chart = st.columns([3, 2])

with col_rec:
    st.markdown(f"""
<div class="ai-card">
  <div class="ai-badge">AI Recommendation</div>
  <div class="ai-stream">{stream}</div>
  <div class="ai-reason">{reason}</div>
</div>
""", unsafe_allow_html=True)

with col_chart:
    st.markdown("**Subject Averages (all classes)**")
    chart_data = pd.DataFrame({
        "Subject": ["Math", "Science", "Computer", "Urdu", "S.St", "English", "Drawing"],
        "Average %": [avgs["math"], avgs["science"], avgs["computer"],
                      avgs["urdu"], avgs["sst"], avgs["english"], avgs["drawing"]]
    }).set_index("Subject")
    st.bar_chart(chart_data, height=280)

st.markdown("**Stream Suitability Scores**")
st.bar_chart(score_df.set_index("Stream"), height=220)

# ── Search History ───────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 📜 Search History")

if os.path.exists(LOG_FILE):
    log_df = pd.read_csv(LOG_FILE)
    if not log_df.empty:
        st.dataframe(
            log_df.sort_values("Time", ascending=False),
            use_container_width=True,
            hide_index=True,
        )
        with open(LOG_FILE, "rb") as f:
            st.download_button(
                label="Download as Excel/CSV",
                data=f,
                file_name="recommendations_log.csv",
                mime="text/csv",
            )
    else:
        st.info("No searches yet.")
else:
    st.info("No searches yet. Search a student above to log recommendations.")
