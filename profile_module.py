import streamlit as st

def display_profile(profile):
    st.subheader("Collected User Profile")
    left, right = st.columns(2)
    with left:
        st.write(f"**Name:** {profile['name']}")
        st.write(f"**Age:** {profile['age']}")
        st.write(f"**Background:** {profile['background'] or 'Not specified'}")
        st.write(f"**Skill Level:** {profile['skill_level']}")
    with right:
        st.write(f"**Interests:** {profile['interests'] or 'Not specified'}")
        st.write(f"**Preferred Category:** {profile['preferred_category']}")
        st.write(f"**Goal:** {profile['goal'] or 'Not specified'}")
        st.write(f"**Preferences:** {profile['preferences'] or 'Not specified'}")
        st.write(f"**Number of Items:** {profile['number_of_items']}")
