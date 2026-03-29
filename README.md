# 🐾 PawPal+

A smart pet care planning assistant built with Python and Streamlit. PawPal+ helps pet owners organize daily care tasks for their pets, automatically scheduling them by priority and deadline.

---

## 🚀 Features

- **Owner & pet management** — create an owner profile and register pets
- **Task tracking** — add feeding, walk, medication, and appointment tasks
- **Smart scheduling** — tasks sorted using Earliest Deadline First (EDF) algorithm
- **Priority conflict resolution** — when two tasks share a deadline, higher priority wins
- **Conflict detection** — warns the user when two tasks are scheduled at the same time
- **Recurring tasks** — daily and weekly tasks automatically schedule their next occurrence
- **Filtering** — filter tasks by completion status or by pet name

---

## 🏗️ System Architecture

Classes:
- `Owner` — stores owner info and manages a list of pets
- `Pet` — stores pet details and a list of care tasks
- `Task` (base class) — shared attributes for all task types
- `FeedingTask`, `WalkTask`, `MedicationTask`, `AppointmentTask` — task subclasses
- `Scheduler` — the "brain" that sorts, filters, detects conflicts, and generates the daily plan

See `uml_pawpal.png` for the full class diagram.

---

## ⚙️ Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## ▶️ Run the App

```bash
python3 -m streamlit run app.py
```

---

## 🧪 Testing PawPal+

Run the full test suite:

```bash
python -m pytest tests/ -v
```

Tests cover:
- Task completion status
- Task addition to a pet
- Sorting correctness (chronological order)
- Conflict detection (same-time tasks)
- No conflict when tasks are at different times
- Recurring daily task scheduling
- Recurring weekly task scheduling
- Pet with no tasks (edge case)
- Filtering by status
- Filtering by pet name

**Confidence level: ⭐⭐⭐⭐ (4/5)**

The core scheduling logic is well tested. The main untested area is the Streamlit UI layer, which would require end-to-end testing tools like Selenium or Playwright.

---

## 📸 Demo

> Screenshot of the running app goes here.

---

## 🤖 Smarter Scheduling

PawPal+ uses two core algorithms to build a smart daily plan:

1. **Earliest Deadline First (EDF)** — tasks with the earliest deadline are scheduled first, ensuring time-sensitive care never gets skipped.
2. **Priority conflict resolution** — when two tasks land at the same time, the higher priority task is placed first and a warning is shown to the user.

Recurring tasks use Python's `timedelta` to automatically calculate the next due date when marked complete.