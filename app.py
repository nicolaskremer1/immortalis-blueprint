import streamlit as st
import pandas as pd
import sqlite3
import feedparser
from datetime import datetime

# Custom CSS (Picus-inspired)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
body, .stApp { background-color: #001F3F; color: #FFFFFF; font-family: 'Orbitron', sans-serif; font-weight: 400; font-size: 1.1rem; line-height: 1.6; }
.st-emotion-cache-1d391kg, .css-1d391kg { background-color: #001F3F !important; color: #FFFFFF !important; } /* Fix Streamlit white bg */
h1, h2, h3 { font-weight: 700; color: #00BFFF; text-shadow: 0 0 5px #00BFFF; font-size: 2rem; margin-bottom: 20px; }
.stButton > button { background-color: #00BFFF; color: #001F3F; border: none; border-radius: 15px; padding: 12px 24px; box-shadow: 0 2px 8px rgba(0, 191, 255, 0.5); transition: box-shadow 0.3s; }
.stButton > button:hover { box-shadow: 0 4px 12px rgba(0, 191, 255, 0.7); }
.stTextInput > div > div > input, .stNumberInput > div > div > input, .stSelectbox > div > div > select, textarea { background-color: #003366; color: #FFFFFF; border: none; border-radius: 15px; padding: 12px; box-shadow: inset 0 2px 5px rgba(0, 191, 255, 0.3); }
.stContainer, .stExpander { background-color: #003366; border: none; border-radius: 15px; box-shadow: 0 2px 8px rgba(0, 191, 255, 0.3); padding: 20px; margin-bottom: 20px; }
.header { display: flex; align-items: center; justify-content: space-between; padding: 10px 20px; background-color: #001F3F; }
.header img { border-radius: 50%; width: 60px; height: 60px; box-shadow: 0 0 10px #00BFFF; }
.header-nav { display: flex; list-style: none; padding: 0; margin: 0; }
.header-nav li { margin: 0 20px; }
.header-nav a { color: #FFFFFF; text-decoration: none; font-size: 1.2rem; transition: color 0.3s; }
.header-nav a:hover { color: #00BFFF; }
section { padding: 40px 0; }
@media (max-width: 768px) { .header-nav { flex-wrap: wrap; justify-content: center; } .header-nav li { margin: 10px; } }
</style>
<img src="https://images.unsplash.com/photo-1698959239601-cb2f9f8f57dc" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1; opacity: 0.3;">
""", unsafe_allow_html=True)

st.set_page_config(page_title="Homo Immortalis", layout="wide")

# Header with logo and nav
st.markdown("""
<header>
    <img src="https://pbs.twimg.com/profile_images/1946373662589751296/I9F-1tT9.jpg" alt="Homo Immortalis Logo">
    <ul class="header-nav">
        <li><a href="#bio-age">Biological Age</a></li>
        <li><a href="#community">Community</a></li>
        <li><a href="#news">Scientific News</a></li>
        <li><a href="#notebook">Notebook</a></li>
    </ul>
</header>
""", unsafe_allow_html=True)

# Scroll to section based on nav click (JavaScript)
page = st.query_params.get("page", ["home"])[0]
if page != "home":
    st.markdown(f"""
    <script>
        window.location.hash = "{page}";
    </script>
    """, unsafe_allow_html=True)

# Main content
with st.container():
    st.title("Homo Immortalis")
    st.markdown("Your journey to optimal longevity starts here.")

    # SQLite setup
    conn = sqlite3.connect('community.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, category TEXT, content TEXT, timestamp TEXT)''')
    conn.commit()

    # Biological Age Section
    with st.container():
        st.markdown('<section id="bio-age">', unsafe_allow_html=True)
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
                        st.success("You're defying time!")
        with col_detailed:
            st.subheader("Detailed Deep Dive")
            with st.expander("Sleep Metrics"):
                sleep_hours = st.number_input("Sleep Hours", 0.0, 24.0, key="sleep_detailed")
                sleep_quality = st.slider("Sleep Quality (1-10)", 1, 10)
            with st.expander("Exercise Metrics"):
                exercise_hours = st.number_input("Exercise Hours/Week", 0.0, 168.0, key="exercise_detailed")
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
            st.info("Based on UK Biobank and biomarker models—consult professionals.")
        st.markdown('</section>', unsafe_allow_html=True)

    # Community Section
    with st.container():
        st.markdown('<section id="community">', unsafe_allow_html=True)
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
        st.markdown('</section>', unsafe_allow_html=True)

    # Scientific News Section
    with st.container():
        st.markdown('<section id="news">', unsafe_allow_html=True)
        st.header("Latest Longevity Research")
        feed_url = "https://pubmed.ncbi.nlm.nih.gov/rss/search/?term=longevity+OR+aging+OR+healthspan&limit=10"
        feed = feedparser.parse(feed_url)
        cols = st.columns(3)
        for i, entry in enumerate(feed.entries):
            with cols[i % 3]:
                with st.container():
                    st.subheader(entry.title)
                    st.write(entry.summary)
                    st.link_button("Read Study", entry.link)
                    st.write(f"Published: {entry.published}")
        st.markdown('</section>', unsafe_allow_html=True)

    # Notebook Section
    with st.container():
        st.markdown('<section id="notebook">', unsafe_allow_html=True)
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
            with st.container():
                st.subheader(entry['timestamp'])
                st.write(entry['content'])
        st.markdown('</section>', unsafe_allow_html=True)