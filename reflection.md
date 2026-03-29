# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My initial UML design included five classes: `Owner`, `Pet`, `Task` (base class), `Scheduler`, and four `Task` subclasses — `FeedingTask`, `WalkTask`, `MedicationTask`, and `AppointmentTask`.

- `Owner` stores the pet owner's basic info (name, email) and holds a reference to their `Pet`.
- `Pet` stores the pet's attributes (name, species, age) and maintains a list of tasks assigned to it.
- `Task` is a base class that defines shared attributes for all task types: `title`, `deadline`, `priority`, `duration`, and `is_done`. Each subclass adds task-specific fields.
- `Scheduler` handles the core logic: sorting tasks by earliest deadline first (EDF), resolving conflicts by giving priority to higher-priority tasks, and generating a daily plan.

**b. Design changes**

Two changes were made during implementation. First, `Owner` was changed from holding a single `pet` attribute to a `pets` list, since the project required supporting multiple pets. Second, `Scheduler` was updated to take an `Owner` directly instead of a flat task list, so it could reach all pets and their tasks through one entry point. A `generate_plan()` method was also added to return a human-readable explanation of the schedule.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers two constraints: deadline (the time a task must be done by) and priority (how important the task is). Deadline was chosen as the primary sort key because time-sensitive tasks like medication should never be missed. Priority acts as a tiebreaker when two tasks share the same deadline.

**b. Tradeoffs**

The scheduler detects conflicts by checking for exact deadline matches rather than overlapping time windows. For example, if a 30-minute walk starts at 8:00 and a 10-minute feeding also starts at 8:00, the conflict is flagged — but a feeding at 8:20 would not be flagged even though it overlaps with the walk. This tradeoff keeps the logic simple and readable while still catching the most common scheduling mistakes.

---

## 3. AI Collaboration

**a. How you used AI**

AI was used throughout every phase — from brainstorming the UML diagram and generating class stubs, to implementing scheduling algorithms, writing tests, and polishing the Streamlit UI. The most helpful prompts were specific and included context, such as sharing the current file and asking a focused question about one method at a time.

**b. Judgment and verification**

At one point, the AI generated an `Owner` class with a single `pet` attribute instead of a `pets` list. This was caught by running `main.py` and seeing that only one pet's tasks appeared in the schedule. The fix — changing `pet: Pet = None` to `pets: list = field(default_factory=list)` — was a small but important correction that required human review to catch.

---

## 4. Testing and Verification

**a. What you tested**

Ten behaviors were tested: task completion, task addition, sorting correctness, conflict detection, no conflict at different times, daily recurrence, weekly recurrence, a pet with no tasks, filtering by status, and filtering by pet name. These tests cover both happy paths and edge cases.

**b. Confidence**

Confidence level: ⭐⭐⭐⭐ (4/5). The core scheduling logic is thoroughly tested. The main gap is the Streamlit UI layer, which was not covered by automated tests. Given more time, end-to-end UI tests using a tool like Playwright would increase confidence to 5/5.

---

## 5. Reflection

**a. What went well**

The CLI-first workflow worked really well. Building and verifying all the logic in `main.py` before touching `app.py` meant the Streamlit integration was smooth — there were no surprises because the backend was already proven to work.

**b. What you would improve**

With another iteration, the conflict detection logic would be improved to check for overlapping time windows rather than exact matches. For example, a 30-minute walk at 8:00 should conflict with a task at 8:20, not just one also starting at exactly 8:00.

**c. Key takeaway**

The most important lesson was that AI is a powerful tool for accelerating implementation, but the human architect still needs to make the key design decisions. AI generated code quickly, but it took human judgment to catch bugs, evaluate tradeoffs, and decide which suggestions to keep or discard. Being the "lead architect" means staying in control of the design even when AI is writing most of the code.