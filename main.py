import streamlit as st
from input_module import collect_profile
from profile_module import display_profile
from preference_module import analyze_preferences
from prompt_module import build_prompt
from recommendation_module import generate_recommendations
from ranking_module import rank_recommendations
from explanation_module import explain_recommendations
from feedback_module import refine_recommendations
from intent_module import detect_intent
from save_module import save_recommendations
from utils import load_dataset

st.set_page_config(page_title="Personalized Recommendation System", page_icon="🎓", layout="wide")

st.markdown("""
<style>
.main {background-color: #f7f8fc;}
.block-container {padding-top: 2rem;}
.hero {padding: 1.5rem; border-radius: 16px; background: linear-gradient(110deg,#172554,#4f46e5); color:white;}
.hero h1 {color:white;}
.small-note {color:#64748b;font-size:0.9rem;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>🎓 Personalized Recommendation System</h1><p>Discover courses matched to your interests, skills and learning goals.</p></div>', unsafe_allow_html=True)
st.write("")

df = load_dataset()
if df is None or df.empty:
    st.error("Dataset could not be loaded. Place Coursera.csv inside the dataset folder.")
    st.stop()

with st.sidebar:
    st.header("⚙️ System")
    st.success(f"Dataset loaded: {len(df):,} courses")
    st.caption("AI engine: Ollama (local model)")
    model = st.text_input("Ollama model", value="llama3.2")
    st.caption("Make sure Ollama is running and the model is downloaded.")
    st.markdown("[Ollama download](https://ollama.com/download)")

tab1, tab2, tab3, tab4 = st.tabs(["👤 User Profile", "✨ Recommendations", "💬 Feedback & Intent", "📁 Saved Results"])

with tab1:
    st.subheader("1. Enter your profile")
    profile = collect_profile()
    if st.button("Analyze My Preferences", type="primary", use_container_width=True):
        st.session_state.profile = profile
        st.session_state.analysis = analyze_preferences(profile)
        st.session_state.prompt = build_prompt(profile, st.session_state.analysis)
        st.success("Your profile has been collected and analyzed.")
    if "profile" in st.session_state:
        st.divider()
        display_profile(st.session_state.profile)
        st.subheader("Preference Analysis")
        st.json(st.session_state.analysis)
        with st.expander("View generated prompt"):
            st.code(st.session_state.prompt, language="text")

with tab2:
    st.subheader("2. Generate personalized recommendations")
    if "profile" not in st.session_state:
        st.info("Enter your profile in the User Profile tab first.")
    else:
        st.write(f"Recommendations requested: **{st.session_state.profile['number_of_items']}**")
        if st.button("Generate Recommendations", type="primary", use_container_width=True):
            with st.spinner("Finding suitable courses and asking Ollama to personalize them..."):
                recs, status = generate_recommendations(
                    df, st.session_state.profile, st.session_state.analysis,
                    model=model
                )
                st.session_state.recommendations = rank_recommendations(recs)
                st.session_state.generation_status = status
        if "recommendations" in st.session_state:
            if st.session_state.get("generation_status"):
                st.info(st.session_state.generation_status)
            for i, rec in enumerate(st.session_state.recommendations, 1):
                with st.container(border=True):
                    st.markdown(f"**{i}. {rec.get('course_name','Course')}**")
                    st.caption(f"{rec.get('university','')} · {rec.get('difficulty','')} · ⭐ {rec.get('rating','N/A')}")
                    st.progress(max(0, min(100, int(rec.get("score", 0)))) / 100)
                    st.write(f"**Suitability:** {rec.get('score', 0)}%")
                    st.write(rec.get("reason", "Matches your profile and interests."))
                    if rec.get("url"):
                        st.markdown(f"[Open course]({rec['url']})")
                    st.caption(f"Explanation: {rec.get('explanation', rec.get('reason',''))}")

with tab3:
    st.subheader("3. Feedback and intelligent intent detection")
    user_message = st.text_area("Type what you want to do", placeholder="Example: I prefer beginner AI courses and do not want web development.")
    if st.button("Detect Intent"):
        intent = detect_intent(user_message, model=model)
        st.session_state.detected_intent = intent
    if "detected_intent" in st.session_state:
        st.success(f"Detected Intent: {st.session_state.detected_intent}")
    feedback = st.text_area("Recommendation feedback", placeholder="Example: I prefer Artificial Intelligence and practical courses. Avoid web development.")
    if st.button("Refine Recommendations", type="primary"):
        if "recommendations" not in st.session_state or "profile" not in st.session_state:
            st.warning("Generate recommendations first.")
        elif not feedback.strip():
            st.warning("Please enter feedback.")
        else:
            with st.spinner("Refining your recommendations..."):
                refined = refine_recommendations(
                    df, st.session_state.profile, st.session_state.recommendations,
                    feedback, model=model
                )
                st.session_state.refined = rank_recommendations(refined)
            st.success("Recommendations refined using your feedback.")
    if "refined" in st.session_state:
        st.markdown("### Refined Recommendations")
        for i, rec in enumerate(st.session_state.refined, 1):
            st.markdown(f"**{i}. {rec['course_name']} — {rec['score']}%**")
            st.write(rec["reason"])
            if rec.get("url"):
                st.markdown(f"[Open course]({rec['url']})")

with tab4:
    st.subheader("4. Save recommendations")
    if "recommendations" not in st.session_state:
        st.info("Generate recommendations first.")
    else:
        if st.button("Save Recommendations to File", type="primary"):
            path = save_recommendations(
                st.session_state.profile,
                st.session_state.get("refined", st.session_state.recommendations)
            )
            st.success(f"Saved successfully: {path}")
            with open(path, "rb") as f:
                st.download_button("Download recommendations.txt", f, file_name="recommendations.txt")
        st.caption("Saved files are stored in the outputs folder.")
