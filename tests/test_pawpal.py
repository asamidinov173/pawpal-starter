from datetime import time, date, timedelta
from pawpal_system import Owner, Pet, FeedingTask, WalkTask, MedicationTask, Scheduler


# --- Helper to build a standard owner/pet/scheduler ---
def make_scheduler():
    owner = Owner(name="Alikhan", email="alikhan@email.com")
    pet = Pet(name="Buddy", species="Dog", age=3)
    owner.add_pet(pet)
    return owner, pet, Scheduler(owner)


# --- Phase 2 tests (kept) ---

def test_task_completion():
    """Verify that mark_complete() changes task status to done."""
    task = FeedingTask(title="Morning feed", deadline=time(8, 0), priority=2, duration=10)
    assert task.is_done == False
    task.mark_complete()
    assert task.is_done == True


def test_task_addition():
    """Verify that adding a task increases the pet's task count."""
    _, pet, _ = make_scheduler()
    assert len(pet.tasks) == 0
    pet.add_task(FeedingTask(title="Morning feed", deadline=time(8, 0), priority=2, duration=10))
    assert len(pet.tasks) == 1


# --- Phase 4 tests ---

def test_sorting_correctness():
    """Verify tasks are returned in chronological order."""
    owner, pet, scheduler = make_scheduler()
    pet.add_task(WalkTask(title="Late walk", deadline=time(9, 0), priority=1, duration=30))
    pet.add_task(FeedingTask(title="Early feed", deadline=time(7, 0), priority=2, duration=10))
    pet.add_task(MedicationTask(title="Mid meds", deadline=time(8, 0), priority=3, duration=5))

    plan = scheduler.generate_plan()
    deadlines = [task.deadline for _, task in plan]
    assert deadlines == sorted(deadlines)


def test_conflict_detection():
    """Verify that scheduler flags two tasks at the same time."""
    owner, pet, scheduler = make_scheduler()
    pet.add_task(FeedingTask(title="Morning feed", deadline=time(8, 0), priority=2, duration=10))
    pet.add_task(WalkTask(title="Morning walk", deadline=time(8, 0), priority=1, duration=30))

    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 1
    assert "08:00:00" in conflicts[0]


def test_no_conflict_when_different_times():
    """Verify no conflicts reported when tasks are at different times."""
    owner, pet, scheduler = make_scheduler()
    pet.add_task(FeedingTask(title="Morning feed", deadline=time(8, 0), priority=2, duration=10))
    pet.add_task(WalkTask(title="Morning walk", deadline=time(9, 0), priority=1, duration=30))

    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 0


def test_recurring_daily_task():
    """Verify that marking a daily task complete sets next_due to tomorrow."""
    task = FeedingTask(
        title="Daily feed", deadline=time(8, 0), priority=2,
        duration=10, frequency="daily"
    )
    task.mark_complete()
    assert task.is_done == True
    assert task.next_due == date.today() + timedelta(days=1)


def test_recurring_weekly_task():
    """Verify that marking a weekly task complete sets next_due to next week."""
    task = MedicationTask(
        title="Weekly meds", deadline=time(9, 0), priority=3,
        duration=5, frequency="weekly"
    )
    task.mark_complete()
    assert task.next_due == date.today() + timedelta(weeks=1)


def test_pet_with_no_tasks():
    """Verify scheduler handles a pet with no tasks gracefully."""
    owner, pet, scheduler = make_scheduler()
    plan = scheduler.generate_plan()
    assert plan == []


def test_filter_by_status():
    """Verify filter_by_status returns only pending or done tasks."""
    owner, pet, scheduler = make_scheduler()
    task1 = FeedingTask(title="Morning feed", deadline=time(8, 0), priority=2, duration=10)
    task2 = WalkTask(title="Morning walk", deadline=time(9, 0), priority=1, duration=30)
    task1.mark_complete()
    pet.add_task(task1)
    pet.add_task(task2)

    pending = scheduler.filter_by_status(done=False)
    done = scheduler.filter_by_status(done=True)
    assert len(pending) == 1
    assert len(done) == 1


def test_filter_by_pet():
    """Verify filter_by_pet returns only tasks for the specified pet."""
    owner = Owner(name="Alikhan", email="alikhan@email.com")
    dog = Pet(name="Buddy", species="Dog", age=3)
    cat = Pet(name="Whiskers", species="Cat", age=5)
    dog.add_task(FeedingTask(title="Dog feed", deadline=time(8, 0), priority=2, duration=10))
    cat.add_task(MedicationTask(title="Cat meds", deadline=time(7, 0), priority=3, duration=5))
    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner)
    buddy_tasks = scheduler.filter_by_pet("Buddy")
    assert len(buddy_tasks) == 1
    assert buddy_tasks[0][1].title == "Dog feed"