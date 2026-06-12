import streamlit as st
import json
import os
import random
import time
from datetime import datetime

DATA_FILE = "pet_data.json"
POOP_FOLDER = "poop"

os.makedirs(POOP_FOLDER, exist_ok=True)

DEFAULT_DATA = {
    "name": "Dumpster Pup",
    "hunger": 40,
    "happiness": 70,
    "energy": 80,
    "files_eaten": 0,
    "poops_produced": 0,
    "times_petted": 0,
    "birth_time": str(datetime.now()),
    "favorite_type": "Unknown",
    "eaten_types": {}
}


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return DEFAULT_DATA.copy()


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


pet = load_data()

# Simulate passage of time
pet["hunger"] = min(100, pet["hunger"] + 1)
pet["energy"] = max(0, pet["energy"] - 1)

if pet["energy"] < 30:
    state = "Sleeping"
elif pet["hunger"] > 70:
    state = "Hungry"
else:
    state = random.choice(["Awake", "Awake", "Sleeping"])

save_data(pet)

st.set_page_config(page_title="Dumpster Pup", page_icon="🐶")

st.title("🐶 Dumpster Pup")

# Pet display
if state == "Sleeping":
    pet_face = "😴"
    message = random.choice([
        "zzz...",
        "dreaming of garbage...",
        "five more minutes..."
    ])
elif state == "Hungry":
    pet_face = "🥺"
    message = random.choice([
        "feed me junk...",
        "i crave spreadsheets...",
        "any trash today?"
    ])
else:
    pet_face = random.choice(["🐶", "😄", "😊"])
    message = random.choice([
        "hello human",
        "anything tasty?",
        "seen any trash lately?"
    ])

st.markdown(
    f"""
    <div style="text-align:center;font-size:120px;">
    {pet_face}
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <h3 style="text-align:center;">
    "{message}"
    </h3>
    """,
    unsafe_allow_html=True
)

# Stats
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🍗 Hunger", pet["hunger"])

with col2:
    st.metric("😊 Happiness", pet["happiness"])

with col3:
    st.metric("⚡ Energy", pet["energy"])

st.divider()

# Petting
if st.button("🖐 Pet Dumpster Pup"):
    pet["happiness"] = min(100, pet["happiness"] + 5)
    pet["times_petted"] += 1
    save_data(pet)

    st.success(
        random.choice([
            "Tail wagging!",
            "Happy bark!",
            "The pup loves that.",
            "You received one emotional support point."
        ])
    )

st.divider()

st.subheader("🗑 Feed Trash Files")

uploaded = st.file_uploader(
    "Drop unwanted files here",
    accept_multiple_files=True
)

if uploaded:

    eaten_now = []

    for file in uploaded:

        save_path = os.path.join(
            POOP_FOLDER,
            file.name
        )

        with open(save_path, "wb") as f:
            f.write(file.getbuffer())

        ext = os.path.splitext(file.name)[1]

        pet["eaten_types"][ext] = pet["eaten_types"].get(ext, 0) + 1

        eaten_now.append(file.name)

        pet["files_eaten"] += 1
        pet["hunger"] = max(0, pet["hunger"] - 10)
        pet["happiness"] = min(100, pet["happiness"] + 3)

    if pet["eaten_types"]:
        pet["favorite_type"] = max(
            pet["eaten_types"],
            key=pet["eaten_types"].get
        )

    # Produce poop every 5 files
    if pet["files_eaten"] % 5 == 0:

        poop_name = f"poop_{pet['poops_produced']+1:03d}.txt"

        with open(
            os.path.join(POOP_FOLDER, poop_name),
            "w"
        ) as poop_file:

            poop_file.write(
                "Dumpster Pup Digest Report\n\n"
            )

            for item in eaten_now:
                poop_file.write(
                    f"- {item}\n"
                )

            poop_file.write(
                "\nRating: Very crunchy.\n"
            )

        pet["poops_produced"] += 1

    save_data(pet)

    st.success(
        f"🍴 Dumpster Pup consumed {len(uploaded)} file(s)!"
    )

    st.balloons()

st.divider()

st.subheader("📊 Statistics")

days_alive = (
    datetime.now() -
    datetime.fromisoformat(
        pet["birth_time"]
    )
).days

st.write(f"**Files Consumed:** {pet['files_eaten']}")
st.write(f"**Poops Produced:** {pet['poops_produced']}")
st.write(f"**Times Petted:** {pet['times_petted']}")
st.write(f"**Favorite File Type:** {pet['favorite_type']}")
st.write(f"**Days Alive:** {days_alive}")

st.divider()

st.subheader("🎲 Random Event")

if st.button("Trigger Event"):

    event = random.choice([
        "Found an ancient receipt.",
        "Dreamed about infinite garbage.",
        "Zoomed across the room.",
        "Burped loudly.",
        "Discovered a mysterious USB."
    ])

    st.info(event)

st.caption(
    "Dumpster Pup spends most of the day sleeping and occasionally eating your digital junk."
)