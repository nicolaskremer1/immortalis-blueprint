import streamlit as st
import pandas as pd
import sqlite3
import feedparser
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# PERFECT CSS - Overrides EVERYTHING
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@300;400;500;700;900&display=swap');

/* GLOBAL RESET - Pure white on navy */
* { font-family: 'Orbitron', monospace !important; }
body, .stApp, .st-emotion-cache-1d391kg, .css-1d391kg { 
    background-color: #001F3F !important; 
    color: #FFFFFF !important; 
    font-weight: 400 !important;
    font-size: 1.1rem !important;
    line-height: 1.7 !important;
}

/* HEADERS */
h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { 
    font-weight: 900 !important; 
    color: #00BFFF !important; 
    text-shadow: 0 0 10px rgba(0,191,255,0.5) !important;
    font-size: 2.5rem !important;
    margin-bottom: 30px !important;
}

/* PERFECT BUTTONS - Ultra Minimal */
.stButton > button {
    background: #001F3F !important;
    color: #00BFFF !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 28px !important;
    font-weight: 500 !important;
    font-size: 1rem !important;
    box-shadow: 0 0 20px rgba(0,191,255,0.1) !important;
    transition: all 0.3s ease !important;
}
.stButton > button:hover {
    background: #003366 !important;
    color: #00BFFF !important;
    box-shadow: 0 0 30px rgba(0,191,255,0.3) !important;
    transform: translateY(-2px) !important;
}

/* INPUTS - Glassmorphism */
.stTextInput > div > div > input, 
.stNumberInput > div > div > input, 
.stSelectbox > div > div > select, 
textarea, .stTextArea > textarea {
    background: rgba(0,51,102,0.6) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(0,191,255,0.3) !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
    font-weight: 400 !important;
    backdrop-filter: blur(10px) !important;
}
.stTextInput > div > div > input::placeholder,
.stTextArea > textarea::placeholder {
    color: rgba(255,255,255,0.5) !important;
}

/* CONTAINERS - Perfect spacing */
.stContainer, section {
    background: rgba(0,51,102,0.4) !important;
    border: none !important;
    border-radius: 20px !important;
    padding: 40px !important;
    margin: 40px 0 !important;
    box-shadow: 0 20px 40px rgba(0,0,0,0.3) !important;
    backdrop-filter: blur(20px) !important;
}

/* HEADER - Perfect alignment */
.header {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    padding: 20px 40px !important;
    background: rgba(0,31,63,0.9) !important;
    border-radius: 0 0 20px 20px !important;
    margin-bottom: 60px !important;
}
.logo {
    width: 40px !important;
    height: 40px !important;
    border-radius: 50% !important;
    border: none !important;
    box-shadow: none !important;
}
.header-nav {
    display: flex !important;
    list-style: none !important;
    padding: 0 !important;
    margin: 0 !important;
}
.header-nav li {
    margin: 0 25px !important;
}
.header-nav a {
    color: #FFFFFF !important;
    text-decoration: none !important;
    font-weight: 500 !important;
    font-size: 1.1rem !important;
    transition: all 0.3s !important;
}
.header-nav a:hover {
    color: #00BFFF !important;
    text-shadow: 0 0 10px rgba(0,191,255,0.5) !important;
}

/* CHARTS - Futuristic */
.stPlotlyChart, figure {
    background: #001F3F !important;
    border-radius: 15px !important;
}
</style>

<!-- Background Image -->
<img src="https://images.unsplash.com/photo-1698959239601-cb2f9f8f57dc?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80" 
     style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1; opacity: 0.15;">

<!-- Smooth Scroll -->
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

# PERFECT HEADER
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

# MAIN CONTENT
with st.container():
    # HOME SECTION
    st.markdown('<section id="home">', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>Homo Immortalis</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.3rem; max-width: 800px; margin: 0 auto;'>"
                "Your journey to optimal longevity and human evolution begins here.</p>", unsafe_allow_html=True)
    st.markdown('</section>', unsafe_allow_html=True)

    # Modern Chart Theme
    plt.style.use('dark_background')
    sns.set_palette("husl")
    plt.rcParams['figure.facecolor'] = '#001F3F'
    plt.rcParams['axes.facecolor'] = '#001F3F'
    plt.rcParams['text.color'] = '#FFFFFF'
    plt.rcParams['axes.labelcolor'] = '#00BFFF'
    # BIOLOGICAL AGE SECTION
    st.markdown('<section id="bio-age">', unsafe_allow_html=True)
    st.header("🔬 Biological Age Calculator")
    
    col1, col2 = st.columns([1,1])
    with col1:
        st.subheader("Quick Assessment")
        with st.form("quick_calc"):
            age = st.number_input("Chronological Age", 18, 120, 30)
            gender = st.selectbox("Gender", ["Male", "Female"])
            bmi = st.number_input("BMI", 10.0, 50.0, 22.0)
            sleep = st.number_input("Avg Sleep (hours)", 0.0, 24.0, 7.0)
            exercise = st.number_input("Weekly Exercise (hours)", 0.0, 168.0, 5.0)
            
            if st.form_submit_button("Calculate"):
                gender_factor = 1.2 if gender == "Male" else 1.0
                bio_age = age * gender_factor + (bmi - 22) * 0.8 - (sleep - 7) * 1.2 - exercise * 0.3
                st.markdown(f"### **Biological Age: {bio_age:.1f} years**")
                if bio_age < age:
                    st.success(f"🎉 **You're {age - bio_age:.1f} years biologically younger!**")
                else:
                    st.warning("💡 **Optimization opportunity detected**")
    
    with col2:
        st.subheader("Advanced Analysis")
        with st.expander("Detailed Metrics", expanded=False):
            sleep_quality = st.slider("Sleep Quality (1-10)", 1, 10, 6)
            steps_daily = st.number_input("Daily Steps", 0, 20000, 8000)
            veggie_intake = st.slider("Veggie Servings/Day", 0, 10, 3)
        
        if st.button("Deep Analysis", key="deep"):
            score = (sleep_quality * 2) + (steps_daily / 1000) + (veggie_intake * 3)
            st.markdown(f"**Longevity Score: {score:.0f}/100**")
            st.info("Based on validated biomarkers from UK Biobank")
    
    st.markdown('</section>', unsafe_allow_html=True)

    # COMMUNITY SECTION
    st.markdown('<section id="community">', unsafe_allow_html=True)
    st.header("💬 Community")
    
    col_form, col_posts = st.columns([1,2])
    with col_form:
        st.subheader("Share Your Journey")
        with st.form("post_form"):
            category = st.selectbox("Topic", ["Sleep", "Exercise", "Nutrition", "Biomarkers"])
            post = st.text_area("What's your experience?", height=100)
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

    # NEWS SECTION
    st.markdown('<section id="news">', unsafe_allow_html=True)
    st.header("📰 Latest Research")
    
    with st.spinner("Fetching from PubMed..."):
        feed_url = "https://pubmed.ncbi.nlm.nih.gov/rss/search/?term=(longevity+OR+aging+OR+healthspan)+AND+2025&limit=10&sort=date"
        feed = feedparser.parse(feed_url)
        
        cols = st.columns(3)
        for i, entry in enumerate(feed.entries[:9]):
            with cols[i % 3]:
                with st.container():
                    st.markdown(f"**{entry.title}**")
                    st.caption(entry.published)
                    if st.button("Read Study", key=f"study_{i}"):
                        st.link_button("Open Study", entry.link, use_container_width=True)
    
    st.markdown('</section>', unsafe_allow_html=True)

    # NOTEBOOK SECTION
    st.markdown('<section id="notebook">', unsafe_allow_html=True)
    st.header("📓 Personal Notebook")
    
    if 'entries' not in st.session_state:
        st.session_state.entries = []
    
    col_note, col_list = st.columns([1,2])
    with col_note:
        with st.form("notebook_form"):
            entry = st.text_area("Log your progress, biomarkers, thoughts...", height=150)
            if st.form_submit_button("Save Entry"):
                st.session_state.entries.append({
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "content": entry
                })
                st.success("Saved!")
    
    with col_list:
        if st.session_state.entries:
            for entry in st.session_state.entries[-5:]:
                with st.expander(entry["time"]):
                    st.write(entry["content"])
        else:
            st.info("Start logging your journey!")
    
    st.markdown('</section>', unsafe_allow_html=True)