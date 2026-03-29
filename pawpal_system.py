from dataclasses import dataclass, field
from datetime import time, date, timedelta
from typing import Optional


@dataclass
class Task:
    """Represents a single pet care activity."""
    title: str
    deadline: time
    priority: int
    duration: int
    is_done: bool = False
    frequency: Optional[str] = None  # "daily", "weekly", or None
    next_due: Optional[date] = None

    def execute(self):
        """Mark this task as done."""
        self.is_done = True

    def mark_complete(self):
        """Mark task complete and schedule next occurrence if recurring."""
        self.is_done = True
        if self.frequency == "daily":
            self.next_due = date.today() + timedelta(days=1)
        elif self.frequency == "weekly":
            self.next_due = date.today() + timedelta(weeks=1)


@dataclass
class FeedingTask(Task):
    """A feeding activity with food type and portion size."""
    food_type: str = ""
    portion: float = 0.0

    def execute(self):
        """Execute the feeding task."""
        self.is_done = True


@dataclass
class WalkTask(Task):
    """A walk activity with route and distance."""
    route: str = ""
    distance: float = 0.0

    def execute(self):
        """Execute the walk task."""
        self.is_done = True


@dataclass
class MedicationTask(Task):
    """A medication activity with drug name and dose."""
    drug: str = ""
    dose: float = 0.0

    def execute(self):
        """Execute the medication task."""
        self.is_done = True


@dataclass
class AppointmentTask(Task):
    """A vet appointment with vet name and location."""
    vet: str = ""
    location: str = ""

    def execute(self):
        """Execute the appointment task."""
        self.is_done = True


@dataclass
class Pet:
    """Stores pet details and a list of care tasks."""
    name: str
    species: str
    age: int
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet's task list."""
        self.tasks.append(task)


@dataclass
class Owner:
    """Manages pet owner info and their pets."""
    name: str
    email: str
    pets: list = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def get_all_tasks(self):
        """Return all tasks across all pets as (pet_name, task) tuples."""
        all_tasks = []
        for pet in self.pets:
            for task in pet.tasks:
                all_tasks.append((pet.name, task))
        return all_tasks


class Scheduler:
    """Retrieves, organizes, and manages tasks across all pets."""

    def __init__(self, owner: Owner):
        """Initialize scheduler with an owner."""
        self.owner = owner

    def get_all_tasks(self):
        """Retrieve all tasks from the owner's pets."""
        return self.owner.get_all_tasks()

    def sort_by_deadline(self):
        """Sort all tasks by earliest deadline first (EDF)."""
        tasks = self.get_all_tasks()
        return sorted(tasks, key=lambda x: x[1].deadline)

    def resolve_conflict(self, tasks):
        """If two tasks share a deadline, higher priority wins."""
        return sorted(tasks, key=lambda x: (x[1].deadline, -x[1].priority))

    def filter_by_status(self, done: bool = False):
        """Filter tasks by completion status."""
        return [(pet, task) for pet, task in self.get_all_tasks()
                if task.is_done == done]

    def filter_by_pet(self, pet_name: str):
        """Filter tasks by pet name."""
        return [(pet, task) for pet, task in self.get_all_tasks()
                if pet.lower() == pet_name.lower()]

    def detect_conflicts(self):
        """Detect tasks scheduled at the exact same time for the same pet."""
        warnings = []
        for pet in self.owner.pets:
            seen_times = {}
            for task in pet.tasks:
                if task.deadline in seen_times:
                    warnings.append(
                        f"Conflict for {pet.name}: '{task.title}' and "
                        f"'{seen_times[task.deadline]}' are both at {task.deadline}"
                    )
                else:
                    seen_times[task.deadline] = task.title
        return warnings

    def generate_plan(self):
        """Generate a daily schedule sorted by deadline and priority."""
        tasks = self.sort_by_deadline()
        tasks = self.resolve_conflict(tasks)
        return tasks