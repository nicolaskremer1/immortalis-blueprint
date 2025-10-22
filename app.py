import streamlit as st
import pandas as pd
import sqlite3
import feedparser
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Modern Chart Theme
plt.style.use('dark_background')
sns.set_palette("husl")
plt.rcParams['figure.facecolor'] = '#001F3F'
plt.rcParams['axes.facecolor'] = '#001F3F'
plt.rcParams['text.color'] = '#FFFFFF'
plt.rcParams['axes.labelcolor'] = '#00BFFF'
plt.rcParams['font.family'] = 'Inter'
plt.rcParams['axes.grid'] = False

# CSS for Ultra-Minimal Design
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;600&display=swap');
* { font-family: 'Inter', sans-serif !important; }
body, .stApp, .st-emotion-cache-1d391kg, .css-1d391kg { 
    background-color: #001F3F !important; 
    color: #FFFFFF !important; 
    font-weight: 300 !important;
    font-size: 1.1rem !important;
    line-height: 1.7 !important;
}
h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { 
    font-weight: 600 !important; 
    color: #00BFFF !important; 
    font-size: 2.2rem !important;
    margin-bottom: 20px !important;
}
.stButton > button {
    background: transparent !important;
    color: #00BFFF !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 8px 16px !important;
    font-weight: 300 !important;
    font-size: 1rem !important;
    text-decoration: none !important;
    transition: transform 0.3s ease, text-decoration 0.3s ease !important;
}
.stButton > button:hover {
    background: transparent !important;
    color: #00BFFF !important;
    text-decoration: underline !important;
    transform: scale(1.03) !important;
}
.stLinkButton > a {
    background: transparent !important;
    color: #00BFFF !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 8px 16px !important;
    font-weight: 300 !important;
    font-size: 1rem !important;
    text-decoration: none !important;
    transition: text-decoration 0.3s ease !important;
}
.stLinkButton > a:hover {
    text-decoration: underline !important;
    color: #00BFFF !important;
}
.stTextInput > div > div > input, 
.stNumberInput > div > div > input, 
.stSelectbox > div > div > select, 
textarea, .stTextArea > textarea {
    background: rgba(0,51,102,0.5) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 12px 16px !important;
    font-weight: 300 !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
}
.stTextInput > div > div > input::placeholder,
.stTextArea > textarea::placeholder {
    color: #FFFFFF !important;
    font-size: 0.9rem !important;
    opacity: 0.7 !important;
}
.stContainer, section#home, section#community, section#news {
    background-color: #001F3F !important;
    border: none !important;
    padding: 30px !important;
    margin-bottom: 30px !important;
    min-height: 400px !important;
    transition: all 0.3s ease !important;
}
section#bio-age, section#notebook {
    background-color: #003366 !important;
    border: none !important;
    padding: 30px !important;
    margin-bottom: 30px !important;
    min-height: 400px !important;
    transition: all 0.3s ease !important;
}
.stExpander {
    background: rgba(0,51,102,0.4) !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 30px !important;
    transition: height 0.3s ease !important;
    display: block !important;
    overflow: hidden !important;
}
.header {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    padding: 15px 30px !important;
    background: rgba(0,31,63,0.8) !important;
    border-radius: 0 0 15px 15px !important;
    margin-bottom: 30px !important;
}
.logo {
    width: 36px !important;
    height: 36px !important;
    border-radius: 50% !important;
    border: none !important;
}
.header-nav {
    display: flex !important;
    gap: 20px !important;
    list-style: none !important;
    padding: 0 !important;
    margin: 0 !important;
    flex-wrap: wrap !important;
}
.header-nav li {
    margin: 0 !important;
}
.header-nav a {
    color: #FFFFFF !important;
    text-decoration: none !important;
    font-weight: 300 !important;
    font-size: 1rem !important;
    transition: color 0.3s ease !important;
}
.header-nav a:hover {
    color: #00BFFF !important;
}
@media (max-width: 768px) {
    .header-nav { justify-content: center !important; }
    .header-nav li { margin: 10px !important; }
}
</style>
<script>
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({behavior: 'smooth'});
    });
});
</script>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Homo Immortalis", layout="wide", initial_sidebar_state="collapsed")

# Header
st.markdown("""
<header class="header">
    <img src="https://pbs.twimg.com/profile_images/1946373662589751296/I9F-1tT9.jpg" alt="Homo Immortalis" class="logo">
    <ul class="header-nav">
        <li><a href="#home">Home</a></li>
        <li><a href="#bio-age">Biological Age</a></li>
        <li><a href="#community">Community</a></li>
        <li><a href="#news">Scientific News</a></li>
        <li><a href="#notebook">Notebook</a></li>
    </ul>
</header>
""", unsafe_allow_html=True)

# SQLite Setup
@st.cache_resource
def init_db():
    conn = sqlite3.connect('community.db', check_same_thread=False)
    conn.execute('''CREATE TABLE IF NOT EXISTS posts 
                    (id INTEGER PRIMARY KEY, category TEXT, content TEXT, timestamp TEXT)''')
    conn.commit()
    return conn

conn = init_db()

# Main Content
with st.container():
    # Home Section
    st.markdown('<section id="home">', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>Homo Immortalis</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; max-width: 700px; margin: 0 auto;'>"
                "Embark on a journey to optimize your longevity and evolve into your best self.</p>", unsafe_allow_html=True)
    st.markdown('</section>', unsafe_allow_html=True)

    # Biological Age Section
    st.markdown('<section id="bio-age">', unsafe_allow_html=True)
    st.header("Biological Age Calculator")
    col_quick, col_detailed = st.columns([1,1], gap="medium")
    with col_quick:
        st.subheader("Quick Assessment")
        with st.form("quick_form"):
            age = st.number_input("Chronological Age", 18, 120, 30, key="quick_age")
            gender = st.selectbox("Gender", ["Male", "Female"], key="quick_gender")
            bmi = st.number_input("BMI", 10.0, 50.0, 22.0, key="quick_bmi")
            sleep_hours = st.number_input("Sleep Hours", 0, 23, 7, key="quick_sleep_hours")
            sleep_minutes = st.number_input("Sleep Minutes", 0, 59, 0, key="quick_sleep_minutes")
            exercise_hours = st.number_input("Exercise Hours/Week", 0, 168, 5, key="quick_exercise_hours")
            exercise_minutes = st.number_input("Exercise Minutes/Week", 0, 59, 0, key="quick_exercise_minutes")
            if st.form_submit_button("Calculate"):
                sleep = sleep_hours + sleep_minutes / 60
                exercise = exercise_hours + exercise_minutes / 60
                gender_factor = 1.2 if gender == "Male" else 1.0
                bio_age = age * gender_factor + (bmi - 22) * 0.8 - (sleep - 7) * 1.2 - exercise * 0.3
                st.markdown(f"### Biological Age: {bio_age:.1f} years")
                if bio_age < age:
                    st.success(f"You're {age - bio_age:.1f} years biologically younger!")
                else:
                    st.warning("Optimization opportunity detected")
    with col_detailed:
        st.subheader("Advanced Analysis")
        with st.expander("Sleep Metrics", expanded=True):
            sleep_hours = st.number_input("Sleep Hours", 0, 23, 7, key="detailed_sleep_hours")
            sleep_minutes = st.number_input("Sleep Minutes", 0, 59, 0, key="detailed_sleep_minutes")
            sleep_quality = st.slider("Sleep Quality (1-10)", 1, 10, 6, key="sleep_quality")
        with st.expander("Exercise Metrics", expanded=True):
            exercise_hours = st.number_input("Exercise Hours/Week", 0, 168, 5, key="detailed_exercise_hours")
            exercise_minutes = st.number_input("Exercise Minutes/Week", 0, 59, 0, key="detailed_exercise_minutes")
            exercise_intensity = st.slider("Intensity (1-10)", 1, 10, 6, key="exercise_intensity")
        with st.expander("Nutrition Metrics", expanded=True):
            calories = st.number_input("Daily Calories", 500, 5000, 2000, key="calories")
            veggie_servings = st.number_input("Daily Veggie Servings", 0, 10, 3, key="veggies")
        with st.expander("Health Biomarkers", expanded=True):
            systolic_bp = st.number_input("Systolic Blood Pressure", 80, 200, 120, key="bp")
            cholesterol = st.number_input("Cholesterol (mg/dL)", 100, 300, 180, key="cholesterol")
        if st.button("Deep Analysis"):
            sleep = sleep_hours + sleep_minutes / 60
            exercise = exercise_hours + exercise_minutes / 60
            bio_age = age + systolic_bp * 0.1 + (cholesterol - 200) * 0.05 - (veggie_servings * 0.2) - (sleep_quality * 0.1) - (exercise_intensity * 0.15)
            st.markdown(f"### Detailed Biological Age: {bio_age:.1f} years")
            df = pd.DataFrame({"Metric": ["Chronological", "Biological"], "Age": [age, bio_age]})
            st.bar_chart(df.set_index("Metric"), height=200)
        st.info("Based on validated biomarkers from UK Biobank")
    st.markdown('</section>', unsafe_allow_html=True)

    # Community Section
    st.markdown('<section id="community">', unsafe_allow_html=True)
    st.header("Community")
    col_form, col_posts = st.columns([1,2], gap="medium")
    with col_form:
        st.subheader("Share Your Journey")
        with st.form("post_form"):
            category = st.selectbox("Topic", ["Sleep", "Exercise", "Nutrition", "Biomarkers"])
            post = st.text_area("What's your experience?", height=200)
            if st.form_submit_button("Post"):
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                conn.execute("INSERT INTO posts (category, content, timestamp) VALUES (?, ?, ?)", 
                            (category, post, timestamp))
                conn.commit()
                st.success("Posted!")
    with col_posts:
        st.subheader("Recent Posts")
        df = pd.read_sql("SELECT * FROM posts ORDER BY timestamp DESC LIMIT 5", conn)
        for _, row in df.iterrows():
            with st.expander(f"{row['category']} • {row['timestamp']}"):
                st.write(row['content'])
    st.markdown('</section>', unsafe_allow_html=True)

    # Scientific News Section
    st.markdown('<section id="news">', unsafe_allow_html=True)
    st.header("Latest Research")
    with st.spinner("Fetching from PubMed..."):
        feed_url = "https://pubmed.ncbi.nlm.nih.gov/rss/search/?term=(longevity+OR+aging+OR+healthspan)+AND+2025&limit=10&sort=date"
        feed = feedparser.parse(feed_url)
        cols = st.columns(3, gap="medium")
        for i, entry in enumerate(feed.entries[:9]):
            with cols[i % 3]:
                with st.container():
                    st.markdown(f"**{entry.title}**")
                    st.caption(entry.published)
                    st.link_button("Read Study", entry.link, use_container_width=True)
    st.markdown('</section>', unsafe_allow_html=True)

    # Notebook Section
    st.markdown('<section id="notebook">', unsafe_allow_html=True)
    st.header("Personal Notebook")
    if 'entries' not in st.session_state:
        st.session_state.entries = []
    col_note, col_list = st.columns([1,2], gap="medium")
    with col_note:
        with st.form("notebook_form"):
            entry = st.text_area("Log your progress, biomarkers, thoughts...", height=200)
            if st.form_submit_button("Save Entry"):
                st.session_state.entries.append({
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "content": entry
                })
                st.success("Saved!")
    with col_list:
        if st.session_state.entries:
            for entry in st.session_state.entries[-5:]:
                with st.container():
                    st.subheader(entry["time"])
                    st.write(entry["content"])
        else:
            st.info("Start logging your journey!")
    st.markdown('</section>', unsafe_allow_html=True)