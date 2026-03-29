
from datetime import time
from pawpal_system import Owner, Pet, FeedingTask, WalkTask, MedicationTask, Scheduler


# Setup
owner = Owner(name="Alikhan", email="alikhan@email.com")
dog = Pet(name="Buddy", species="Dog", age=3)
cat = Pet(name="Whiskers", species="Cat", age=5)

# Add tasks out of order to test sorting
dog.add_task(WalkTask(
    title="Morning walk",
    deadline=time(9, 0),
    priority=1,
    duration=30,
    route="Park loop",
    distance=2.0,
    frequency="daily"
))
dog.add_task(FeedingTask(
    title="Morning feed",
    deadline=time(8, 0),
    priority=2,
    duration=10,
    food_type="kibble",
    portion=1.5,
    frequency="daily"
))
# Conflict: same deadline as morning feed
dog.add_task(FeedingTask(
    title="Vitamin supplement",
    deadline=time(8, 0),
    priority=1,
    duration=5,
    food_type="supplement",
    portion=0.5
))

cat.add_task(MedicationTask(
    title="Flea medication",
    deadline=time(7, 0),
    priority=3,
    duration=5,
    drug="Frontline",
    dose=1.0,
    frequency="weekly"
))

owner.add_pet(dog)
owner.add_pet(cat)

scheduler = Scheduler(owner)

# --- Today's schedule ---
print("=" * 40)
print("        TODAY'S SCHEDULE")
print("=" * 40)
plan = scheduler.generate_plan()
for i, (pet_name, task) in enumerate(plan, 1):
    status = "DONE" if task.is_done else "pending"
    print(f"{i}. [{task.deadline}] {task.title} ({pet_name})")
    print(f"   Priority: {task.priority} | Duration: {task.duration} mins | Status: {status}")
print()

# --- Conflict detection ---
print("=" * 40)
print("        CONFLICT DETECTION")
print("=" * 40)
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"WARNING: {warning}")
else:
    print("No conflicts detected.")
print()

# --- Filter pending tasks ---
print("=" * 40)
print("        PENDING TASKS")
print("=" * 40)
pending = scheduler.filter_by_status(done=False)
for pet_name, task in pending:
    print(f"- {task.title} ({pet_name}) at {task.deadline}")
print()

# --- Filter by pet ---
print("=" * 40)
print("        BUDDY'S TASKS")
print("=" * 40)
buddy_tasks = scheduler.filter_by_pet("Buddy")
for pet_name, task in buddy_tasks:
    print(f"- {task.title} at {task.deadline}")
print()

# --- Recurring task demo ---
print("=" * 40)
print("        RECURRING TASK DEMO")
print("=" * 40)
flea_task = cat.tasks[0]
print(f"Before: {flea_task.title} | done={flea_task.is_done} | next_due={flea_task.next_due}")
flea_task.mark_complete()
print(f"After:  {flea_task.title} | done={flea_task.is_done} | next_due={flea_task.next_due}")