import streamlit as st

def collect_profile():
    with st.form("profile_form"):
        name = st.text_input("Name", placeholder="Your name")
        c1, c2 = st.columns(2)
        with c1:
            age = st.number_input("Age", min_value=10, max_value=100, value=20)
            background = st.text_input("Educational / Professional Background", placeholder="Computer Science")
            skill = st.selectbox("Skill Level", ["Beginner", "Intermediate", "Advanced"])
        with c2:
            category = st.selectbox("Preferred Category", ["Artificial Intelligence", "Programming", "Data Science", "Business", "Design", "Cloud Computing", "Cybersecurity", "Other"])
            count = st.slider("Number of recommendations", 1, 10, 5)
        interests = st.text_input("Interests (comma-separated)", placeholder="Artificial Intelligence, Python")
        goal = st.text_area("Goal", placeholder="What do you want to learn or achieve?")
        preferences = st.text_input("Preferences", placeholder="Practical learning, short courses, certificates")
        submitted = st.form_submit_button("Submit Profile")
    return {
        "name": name.strip() or "Learner",
        "age": int(age),
        "background": background.strip(),
        "interests": interests.strip(),
        "skill_level": skill,
        "preferred_category": category,
        "goal": goal.strip(),
        "preferences": preferences.strip(),
        "number_of_items": int(count),
    }
