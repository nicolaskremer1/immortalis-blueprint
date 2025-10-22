import streamlit as st
import pandas as pd
import sqlite3
import feedparser
from datetime import datetime

# Custom CSS for improved design
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
body, .stApp { background-color: #001F3F; color: #FFFFFF; font-family: 'Orbitron', sans-serif; font-weight: 400; font-size: 1.1rem; line-height: 1.6; }
h1, h2, h3 { font-weight: 700; color: #00BFFF; text-shadow: 0 0 5px #00BFFF; font-size: 2rem; }
.stButton > button { background-color: #00BFFF; color: #001F3F; border: none; border-radius: 10px; padding: 10px 20px; box-shadow: 0 0 10px #00BFFF; transition: box-shadow 0.3s; }
.stButton > button:hover { box-shadow: 0 0 15px #00BFFF; }
.stTextInput > div > div > input, .stNumberInput > div > div > input, .stSelectbox > div > div > select, textarea { background-color: #003366; color: #FFFFFF; border: 1px solid #00BFFF; border-radius: 10px; padding: 10px; box-shadow: inset 0 0 5px #00BFFF; }
.stExpander { background-color: #003366; border: 1px solid #00BFFF; border-radius: 10px; }
.stTabs > div > button { color: #FFFFFF; border-bottom: 2px solid transparent; transition: border 0.3s; }
.stTabs > div > button:hover { border-bottom: 2px solid #00BFFF; }
.header-nav { display: flex; justify-content: center; list-style: none; padding: 0; }
.header-nav li { margin: 0 15px; }
.header-nav a { color: #FFFFFF; text-decoration: none; transition: color 0.3s; }
.header-nav a:hover { color: #00BFFF; }
.logo { border-radius: 50%; box-shadow: 0 0 10px #00BFFF; }
@media (max-width: 768px) { .header-nav { flex-direction: column; } }
</style>
""", unsafe_allow_html=True)

# Background video
st.markdown("""
<video autoplay muted loop playsinline style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1; opacity: 0.3;">
  <source src="https://static.videezy.com/system/resources/previews/000/051/033/original/Looped_Dark_Blue_Background.mp4" type="video/mp4">
</video>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Homo Immortalis", layout="wide")

# Header with logo and nav
col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://pbs.twimg.com/profile_images/1946373662589751296/I9F-1tT9.jpg", width=50, use_column_width=False, output_format="auto")  # Logo
with col2:
    st.markdown("""
    <ul class="header-nav">
        <li><a href="?page=Biological Age">Biological Age</a></li>
        <li><a href="?page=Community">Community</a></li>
        <li><a href="?page=Scientific News">Scientific News</a></li>
        <li><a href="?page=Notebook">Notebook</a></li>
    </ul>
    """, unsafe_allow_html=True)

# Get page from query params
query_params = st.experimental_get_query_params()
page = query_params.get("page", ["Biological Age"])[0]

# Rest of the code remains similar, but wrap content in st.container for centering
with st.container():
    st.title("Homo Immortalis")

    # SQLite setup (unchanged)
    conn = sqlite3.connect('community.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, category TEXT, content TEXT, timestamp TEXT)''')
    conn.commit()

    if page == "Biological Age":
        st.header("Calculate Your Biological Age")
        col_quick, col_detailed = st.columns(2)
        with col_quick:
            st.subheader("Quick Calculation")
            with st.form("quick_form"):
                age = st.number_input("Chronological Age", 18, 120)
                gender = st.selectbox("Gender", ["Male", "Female"])
                bmi = st.number_input("BMI", 10.0, 50.0)
                sleep = st.number_input("Avg Sleep Hours", 0.0, 24.0)
                exercise = st.number_input("Weekly Exercise Hours", 0.0, 168.0)
                submitted = st.form_submit_button("Calculate")
                if submitted:
                    gender_adjust = 1 if gender == "Male" else 0
                    bio_age = age + (bmi - 22) * 0.5 - sleep * 0.3 - exercise * 0.2 + gender_adjust
                    st.write(f"Biological Age: {bio_age:.1f} years")
                    if bio_age < age:
                        st.success("Evolving toward immortality!")
        with col_detailed:
            st.subheader("Detailed Deep Dive")
            with st.expander("Sleep Metrics"):
                sleep_hours = st.number_input("Sleep Hours", 0.0, 24.0)
                sleep_quality = st.slider("Sleep Quality (1-10)", 1, 10)
            with st.expander("Exercise Metrics"):
                exercise_hours = st.number_input("Exercise Hours/Week", 0.0, 168.0)
                exercise_intensity = st.slider("Intensity (1-10)", 1, 10)
            with st.expander("Nutrition Metrics"):
                calories = st.number_input("Daily Calories", 500, 5000)
                veggie_servings = st.number_input("Daily Veggie Servings", 0, 20)
            with st.expander("Health Biomarkers"):
                systolic_bp = st.number_input("Systolic Blood Pressure", 80, 200)
                cholesterol = st.number_input("Cholesterol (mg/dL)", 100, 300)
            if st.button("Deep Dive Calculation"):
                bio_age = age + systolic_bp * 0.1 + (cholesterol - 200) * 0.05 - (veggie_servings * 0.2) - (sleep_quality * 0.1) - (exercise_intensity * 0.15)
                st.write(f"Detailed Biological Age: {bio_age:.1f} years")
                df = pd.DataFrame({"Metric": ["Chronological", "Biological"], "Age": [age, bio_age]})
                st.bar_chart(df.set_index("Metric"))
            st.info("Inspired by UK Biobank and biomarker models—consult professionals.")

    elif page == "Community":
        st.header("Community Discussions")
        col_form, col_posts = st.columns(2)
        with col_form:
            categories = ["Sleep", "Exercise", "Nutrition"]
            with st.form("new_post"):
                category = st.selectbox("Category", categories)
                content = st.text_area("Your Post")
                submitted = st.form_submit_button("Post")
                if submitted:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                    conn.execute("INSERT INTO posts (category, content, timestamp) VALUES (?, ?, ?)", (category, content, timestamp))
                    conn.commit()
                    st.success("Posted!")
        with col_posts:
            df = pd.read_sql("SELECT * FROM posts ORDER BY timestamp DESC", conn)
            for cat in categories:
                with st.expander(cat):
                    cat_posts = df[df['category'] == cat]
                    for _, post in cat_posts.iterrows():
                        st.write(f"[{post['timestamp']}] {post['content']}")
                        with st.form(key=f"reply_{post['id']}"):
                            reply = st.text_input("Reply")
                            if st.form_submit_button("Reply"):
                                new_content = post['content'] + f"\nReply: {reply}"
                                conn.execute("UPDATE posts SET content = ? WHERE id = ?", (new_content, post['id']))
                                conn.commit()
                                st.success("Replied!")

    elif page == "Scientific News":
        st.header("Latest Longevity Research")
        feed_url = "https://pubmed.ncbi.nlm.nih.gov/rss/search/?term=longevity+OR+aging+OR+healthspan&limit=10"
        feed = feedparser.parse(feed_url)
        cols = st.columns(3)  # 3-column grid for articles
        for i, entry in enumerate(feed.entries):
            with cols[i % 3]:
                with st.expander(entry.title):
                    st.write(entry.summary)
                    st.link_button("Read Study", entry.link)
                    st.write(f"Published: {entry.published}")

    elif page == "Notebook":
        st.header("Personal Notebook")
        if 'notebook' not in st.session_state:
            st.session_state.notebook = []
        
        with st.form("new_entry"):
            content = st.text_area("Log Your Progress/Thoughts")
            submitted = st.form_submit_button("Add Entry")
            if submitted:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                st.session_state.notebook.append({"timestamp": timestamp, "content": content})
                st.success("Entry added!")
        
        for entry in reversed(st.session_state.notebook):
            with st.expander(entry['timestamp']):
                st.write(entry['content'])