import streamlit as st

st.set_page_config(layout="wide", page_title="YouTube-style Gallery")

# ------------------- Sidebar -------------------
st.sidebar.title("📂 Categories")
selected_category = st.sidebar.selectbox(
    "Select a category",
    ["All", "Music", "Business", "News", "Cover Songs"]
)

# ------------------- Data -------------------
videos = [
    {
        "title": "Fastwork ทำกำไรหรือขายฝัน?",
        "creator": "bt bertarid",
        "views": "51K views · 5 days ago",
        "thumb": "https://i.ytimg.com/vi/2FgK_qU5jZ0/hqdefault.jpg",
        "category": "Business"
    },
    {
        "title": "Always On My Mind - Connie Talbot",
        "creator": "ConnieTalbotOfficial",
        "views": "Updated today",
        "thumb": "https://i.ytimg.com/vi_webp/kY6sqZ_W4dc/maxresdefault.webp",
        "category": "Music"
    },
    {
        "title": "BusinessConnection วิเคราะห์ธุรกิจ",
        "creator": "Thinkingradio",
        "views": "174 views · 1 hour ago",
        "thumb": "https://i.ytimg.com/vi/rhqS1Cfh4_8/hqdefault.jpg",
        "category": "Business"
    },
    {
        "title": "Rocketman - Elton John (Cover)",
        "creator": "ConnieTalbotOfficial",
        "views": "1.2M views · 5 years ago",
        "thumb": "https://i.ytimg.com/vi/HU73z5VKoMI/hqdefault.jpg",
        "category": "Cover Songs"
    },
]

# ------------------- Filter -------------------
if selected_category != "All":
    videos = [v for v in videos if v["category"] == selected_category]

# ------------------- Main Header -------------------
st.title(f"📺 YouTube-style Gallery — {selected_category}")

# ------------------- Grid Layout -------------------
for i in range(0, len(videos), 2):
    cols = st.columns(2)
    for j, col in enumerate(cols):
        if i + j < len(videos):
            vid = videos[i + j]
            with col:
                st.image(vid["thumb"], use_column_width=True)
                st.markdown(f"**{vid['title']}**")
                st.caption(f"{vid['creator']} · {vid['views']}")