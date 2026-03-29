import streamlit as st
from datetime import time
from pawpal_system import Owner, Pet, FeedingTask, WalkTask, MedicationTask, AppointmentTask, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# --- Session state setup ---
# Streamlit reruns top to bottom on every interaction.
# We store Owner in session_state so it persists across reruns.
if "owner" not in st.session_state:
    st.session_state.owner = None

# --- Owner + Pet Setup ---
st.subheader("Owner & Pet Info")

owner_name = st.text_input("Owner name", value="Jordan")
owner_email = st.text_input("Owner email", value="jordan@email.com")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
pet_age = st.number_input("Pet age", min_value=0, max_value=30, value=2)

if st.button("Save owner & pet"):
    pet = Pet(name=pet_name, species=species, age=pet_age)
    owner = Owner(name=owner_name, email=owner_email)
    owner.add_pet(pet)
    st.session_state.owner = owner
    st.success(f"Saved! Owner: {owner_name}, Pet: {pet_name} ({species})")

st.divider()

# --- Add Tasks ---
st.subheader("Add Tasks")

if st.session_state.owner is None:
    st.warning("Please save your owner & pet info first.")
else:
    pet = st.session_state.owner.pets[0]

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (mins)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", [1, 2, 3], format_func=lambda x: {1: "low", 2: "medium", 3: "high"}[x])

    deadline_hour = st.slider("Deadline hour", min_value=0, max_value=23, value=8)
    task_type = st.selectbox("Task type", ["Feeding", "Walk", "Medication", "Appointment"])

    if st.button("Add task"):
        deadline = time(deadline_hour, 0)
        if task_type == "Feeding":
            task = FeedingTask(title=task_title, deadline=deadline, priority=priority, duration=duration)
        elif task_type == "Walk":
            task = WalkTask(title=task_title, deadline=deadline, priority=priority, duration=duration)
        elif task_type == "Medication":
            task = MedicationTask(title=task_title, deadline=deadline, priority=priority, duration=duration)
        else:
            task = AppointmentTask(title=task_title, deadline=deadline, priority=priority, duration=duration)

        pet.add_task(task)
        st.success(f"Added task: {task_title}")

    if pet.tasks:
        st.write("Current tasks:")
        st.table([{
            "Title": t.title,
            "Deadline": str(t.deadline),
            "Priority": t.priority,
            "Duration (mins)": t.duration,
            "Done": t.is_done
        } for t in pet.tasks])
    else:
        st.info("No tasks yet. Add one above.")

st.divider()

# --- Generate Schedule ---
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    if st.session_state.owner is None:
        st.error("Please save your owner & pet info first.")
    elif not st.session_state.owner.pets[0].tasks:
        st.error("Please add at least one task first.")
    else:
        scheduler = Scheduler(st.session_state.owner)
        plan = scheduler.generate_plan()

        st.success("Here is today's schedule:")
        for i, (pet_name, task) in enumerate(plan, 1):
            status = "✅ Done" if task.is_done else "⏳ Pending"
            st.markdown(f"**{i}. [{task.deadline}] {task.title}** ({pet_name})")
            st.caption(f"Priority: {task.priority} | Duration: {task.duration} mins | {status}")