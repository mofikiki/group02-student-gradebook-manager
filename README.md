# Student Gradebook Manager

A comprehensive **Flask-based** web application for managing students, assignments, grades, class analytics, and GPA—featuring **role‑based access control** (Teacher/Viewer), CSV exports, and a clean, responsive UI.

> The team initially explored a Tkinter desktop GUI for prototyping; the final MVP is implemented as a **Flask** web app for easier collaboration and deployment.

---

## ✨ Features

### Core
- **Student Management** — add/view students; optional manual IDs with duplicate checks
- **Assignment Management** — create weighted assignments (**Exam / Quiz / Homework**)
- **Grade Recording** — record grades with validation (0–100)
- **Analytics** — per‑student **weighted average** and **GPA**; **class average**
- **Export** — per‑student **CSV** report
- **RBAC** — switch between **Teacher** (full CRUD) and **Viewer** (read‑only) in session

### Object‑Oriented Design
- `Student`, abstract `Assignment` (with `ExamAssignment`, `QuizAssignment`, `HomeworkAssignment`), `Grade`, and `Gradebook` orchestrator
- Special methods: `__str__`, `__repr__`, `__eq__`
- **Custom exceptions:** `InvalidGradeError`, `DuplicateStudentIDError`

### Architecture
- **MVC style:** `src/storage.py` (models + persistence), `src/app.py` (routes/controllers), `templates/` (Jinja2), `static/style.css`
- **Session‑based roles** with simple in‑app role switching
- **JSON persistence** at `data/data.json` (auto‑created if missing)

---

## 📂 Project Structure

```text
group02_studentgradebook/
├── src/
│   ├── __init__.py
│   ├── app.py               # Flask routes, RBAC/session, CSV export endpoint
│   ├── storage.py           # Models + persistence + business logic
│   └── models.py            # (lightweight dataclasses)
├── templates/
│   ├── layout.html          # Base template + role switcher + nav
│   ├── index.html           # Dashboard: add grades, view summaries
│   ├── students.html        # Student CRUD
│   └── assignments.html     # Assignment CRUD
├── static/
│   └── style.css            # Responsive styling
├── data/
│   └── data.json            # Example data (auto‑created if absent)
├── tests/
│   └── test_core.py         # Pytest: core logic + CSV export
├── Pipfile
├── Pipfile.lock
└── README.md                # You are here
```

> **Note:** Flask is configured with `template_folder='../templates'` and `static_folder='../static'`. **Run from the project root** so those paths resolve correctly.

---

## 🛠 Requirements

- **Python** 3.13 (as pinned in `Pipfile`; 3.12+ can work if you adjust `Pipfile` and re‑lock)
- **pipenv** (recommended) — `pip install pipenv`  

---

## 🚀 How to Run

### Option A — Using `pipenv` (recommended)

```bash
# 1) From the project root
cd group02_studentgradebook

# 2) Create/activate env (pin to 3.13 or your installed version)
pipenv --python 3.13
pipenv install

# 3) Run the app (module mode)
pipenv run python -m src.app
# App will start on http://127.0.0.1:5000
```

**Flask CLI alternative**
```bash
# macOS/Linux
export FLASK_APP=src.app
export FLASK_DEBUG=1
pipenv run flask run

# Windows PowerShell
$env:FLASK_APP="src.app"
$env:FLASK_DEBUG="1"
pipenv run flask run
```

### Open the App
```
http://127.0.0.1:5000
```

---

## 🔐 Roles & Permissions

- **Teacher** — full create/read/update/delete + CSV export  
- **Viewer** — read‑only + CSV export  
Switch via the sidebar buttons (Teacher/Viewer). Role is stored in session.

---

## 🔗 Routes (Quick Reference)

| Route                         | Method(s)     | Purpose                                   |
|------------------------------|---------------|-------------------------------------------|
| `/`                          | GET           | Dashboard: grades, summaries, class avg   |
| `/role/<role_name>`          | GET           | Switch role: `teacher` / `viewer`         |
| `/students`                  | GET, POST     | List/add students                          |
| `/assignments`               | GET, POST     | List/add assignments (type + weight)      |
| `/add_grade`                 | POST          | Record a grade                             |
| `/export_csv/<int:student_id>` | GET         | Download per‑student CSV report           |

---

## 📊 Data & Calculations

- **Validation:** Scores must be `0–100` (else `InvalidGradeError`)
- **Weighted Average (per student):** sum of `score × weight` over sum of weights
- **GPA:** simple mapping in `Gradebook.percent_to_gpa` (adjust as needed)
- **Class Average:** mean of available student weighted averages
- **Storage:** `data/data.json` is auto‑created and updated on every change

---

## 🧪 Tests

```bash
# From project root
pipenv run pytest -q
```

Included tests (`tests/test_core.py`):
- add student/assignment/grade and compute weighted average
- export CSV and verify contents

---

## 🧱 Development Plan (Group 2)

1) **Core Classes & Data Models** — `Student`, `Assignment` (+ subclasses), `Gradebook` + special methods  
2) **Grade & GPA Logic** — weighted averages, GPA conversion, class averages; custom exceptions  
3) **CRUD** — students, assignments, grades  
4) **UI** — Flask + Jinja2 + CSS (role switching in sidebar)  
5) **Reports** — per‑student CSV (PDF optional later)

A one‑day integration buffer was kept to absorb risks and align deliverables.

---

## 📦 Dependencies (from `Pipfile.lock`)

**Direct**
- **Flask** `==3.1.2`
- **pytest** `==8.4.2`

**Flask (transitive)**
- **Werkzeug** `==3.1.3`
- **Jinja2** `==3.1.6`
- **Click** `==8.3.0`
- **itsdangerous** `==2.2.0`
- **MarkupSafe** `==3.0.2`
- **blinker** `==1.9.0`

**pytest (transitive)**
- **pluggy** `==1.6.0`
- **iniconfig** `==2.1.0`
- **packaging** `==25.0`
- **colorama** `==0.4.6` (Windows)
- **pygments** `==2.19.2`

> Versions may change if you re‑lock with a different Python version. To keep exact versions, run with Python **3.13** and the included `Pipfile.lock`.

---

## 🧰 Troubleshooting

- **“Module not found” / template issues** — run from the **project root** and use module mode:  
  `pipenv run python -m src.app`
- **CSS not loading** — confirm `static/style.css`; hard refresh (`Ctrl/Cmd+Shift+R`)
- **Port already in use** — `pipenv run flask run --port 5001`
- **Different Python version** — update `Pipfile`’s `python_version`, then `pipenv --rm && pipenv install`

---

## 🙌 Credits

**Project Team (Group 2)**  
**Open‑Source Acknowledgements**  
Flask, Werkzeug, Jinja2, Click, itsdangerous, MarkupSafe, blinker, pytest, pluggy, iniconfig, packaging, colorama, pygments,chatgpt.

---

## 📜 License

This project is licensed under the **MIT License**. See [LICENSE](./LICENSE) for the full text.

SPDX-License-Identifier: MIT


Educational project for learning OOP and web development with Flask.
