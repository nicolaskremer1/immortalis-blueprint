import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config for better visuals
st.set_page_config(page_title="Immortalis Blueprint", layout="wide")

# Initialize session state for user data persistence
if 'user_data' not in st.session_state:
    st.session_state.user_data = {'age': 30, 'sleep_hours': 7.0, 'bmi': 22.0, 'exercise_hours': 1.0}
if 'level' not in st.session_state:
    st.session_state.level = "Homo Sapiens"
if 'streak' not in st.session_state:
    st.session_state.streak = 0

# Title and intro
st.title("Immortalis Blueprint")
st.markdown("Embark on your journey to Homo Immortalis through longevity and optimal health.")

# Sidebar for navigation
st.sidebar.header("Navigation")
page = st.sidebar.selectbox("Choose a page", ["Profile", "Dashboard", "Challenges"])

if page == "Profile":
    # User input form
    st.header("Your Profile")
    with st.form("profile_form"):
        age = st.number_input("Age", min_value=0, max_value=120, value=st.session_state.user_data['age'])
        sleep_hours = st.number_input("Average sleep per night (hours)", min_value=0.0, max_value=24.0, value=st.session_state.user_data['sleep_hours'])
        bmi = st.number_input("BMI", min_value=10.0, max_value=50.0, value=st.session_state.user_data['bmi'])
        exercise_hours = st.number_input("Weekly exercise hours", min_value=0.0, max_value=168.0, value=st.session_state.user_data['exercise_hours'])
        submitted = st.form_submit_button("Save Profile")
        if submitted:
            st.session_state.user_data.update({
                'age': age,
                'sleep_hours': sleep_hours,
                'bmi': bmi,
                'exercise_hours': exercise_hours
            })
            st.success("Profile saved!")

    # Simple biological age calculation
    st.header("Biological Age")
    if st.button("Calculate Biological Age"):
        # Dummy formula: Adjusts chronological age based on health metrics
        bio_age = age + (bmi - 22) * 0.5 - (sleep_hours - 8) * 0.3 + (exercise_hours - 7) * (-0.2)
        st.write(f"Your estimated biological age: {bio_age:.1f} years")
        if bio_age < age:
            st.markdown("🎉 You're aging slower than your chronological age!")

elif page == "Dashboard":
    # Progress dashboard
    st.header("Your Progress to Homo Immortalis")
    data = st.session_state.user_data
    df = pd.DataFrame([data], index=["Current"])
    st.write("### Your Metrics")
    st.dataframe(df)

    # Simple bar chart for metrics
    st.write("### Health Metrics Visualization")
    fig, ax = plt.subplots()
    metrics = ['Age', 'Sleep (hrs)', 'BMI', 'Exercise (hrs/wk)']
    values = [data['age'], data['sleep_hours'], data['bmi'], data['exercise_hours']]
    sns.barplot(x=metrics, y=values, ax=ax, palette="viridis")
    ax.set_ylabel("Value")
    st.pyplot(fig)

    # Level progress
    st.write("### Evolution Level")
    st.write(f"Current Level: {st.session_state.level}")
    if st.session_state.streak >= 7:
        st.session_state.level = "Homo Evolutis"
        st.markdown("🚀 You've evolved to Homo Evolutis! Keep optimizing to reach Homo Immortalis.")

elif page == "Challenges":
    # Daily challenges for engagement
    st.header("Daily Challenges")
    st.markdown("Complete these to boost your longevity score and evolve!")
    if st.button("Log today's healthy meal"):
        st.session_state.streak += 1
        st.success(f"Meal logged! Current streak: {st.session_state.streak} days")
    if st.button("Log 8+ hours of sleep"):
        st.session_state.streak += 1
        st.success(f"Sleep logged! Current streak: {st.session_state.streak} days")
    st.write("Tip: Log daily to unlock higher evolution levels!")
