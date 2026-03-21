import streamlit as st
import requests
import math

# This is a separate file from main.py which contains only the frontend streamlit app code and the FastAPI backend is written in main.py


# ======================== CONFIG ========================
BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="LearnHub - Online Course Platform",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ======================== CUSTOM CSS ========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');


:root {
    --primary: #6C63FF;
    --primary-dark: #5A52D5;
    --accent: #FF6584;
    --bg-dark: #0F0E17;
    --bg-card: #1A1A2E;
    --bg-card-hover: #222244;
    --text-primary: #FFFFFE;
    --text-secondary: #A7A9BE;
    --success: #2CB67D;
    --warning: #FF8906;
    --danger: #E53170;
    --gradient-1: linear-gradient(135deg, #6C63FF 0%, #E44EC6 100%);
    --gradient-2: linear-gradient(135deg, #2CB67D 0%, #6C63FF 100%);
}

html, body, [class*="st-"] {
    font-family: 'Inter', sans-serif;
}

.main .block-container {
    padding-top: 2rem;
    max-width: 1200px;
}

/* Hide sidebar toggle buttons */
header[data-testid="stHeader"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
[data-testid="stSidebarCollapseButton"] { display: none !important; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F0E17 0%, #1A1A2E 100%);
    border-right: 1px solid rgba(108,99,255,0.2);
}

section[data-testid="stSidebar"] .stRadio > label {
    color: #FFFFFE !important;
    font-weight: 600;
}

/* Hero Banner */
.hero-banner {
    background: linear-gradient(135deg, #6C63FF 0%, #E44EC6 50%, #FF6584 100%);
    border-radius: 20px;
    padding: 3rem 2.5rem;
    margin-bottom: 2rem;
    color: white;
    position: relative;
    overflow: hidden;
}
.hero-banner h1 {
    font-size: 2.4rem;
    font-weight: 800;
    margin: 0 0 0.5rem 0;
    letter-spacing: -0.5px;
}
.hero-banner p {
    font-size: 1.1rem;
    opacity: 0.92;
    margin: 0;
    max-width: 600px;
}

/* Metric Cards */
.metric-card {
    background: linear-gradient(145deg, #1A1A2E, #222244);
    border: 1px solid rgba(108,99,255,0.25);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    transition: transform 0.2s, box-shadow 0.2s;
}
.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 30px rgba(108,99,255,0.2);
}
.metric-value {
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #6C63FF, #E44EC6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.metric-label {
    font-size: 0.85rem;
    color: #A7A9BE;
    margin-top: 0.3rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Course Card */
.course-card {
    background: linear-gradient(145deg, #1A1A2E, #16213E);
    border: 1px solid rgba(108,99,255,0.15);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}
.course-card:hover {
    border-color: rgba(108,99,255,0.5);
    box-shadow: 0 4px 20px rgba(108,99,255,0.15);
}
.course-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #FFFFFE;
    margin-bottom: 0.4rem;
}
.course-instructor {
    color: #A7A9BE;
    font-size: 0.9rem;
    margin-bottom: 0.6rem;
}
.course-meta {
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;
    margin-bottom: 0.6rem;
}
.badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
}
.badge-category {
    background: rgba(108,99,255,0.2);
    color: #6C63FF;
}
.badge-level {
    background: rgba(44,182,125,0.2);
    color: #2CB67D;
}
.badge-free {
    background: rgba(255,137,6,0.2);
    color: #FF8906;
}
.price-tag {
    font-size: 1.4rem;
    font-weight: 800;
    color: #2CB67D;
}
.seats-tag {
    font-size: 0.85rem;
    color: #A7A9BE;
}
.seats-low {
    color: #E53170;
    font-weight: 600;
}

/* Section Headers */
.section-header {
    font-size: 1.6rem;
    font-weight: 800;
    margin-bottom: 1.5rem;
    padding-bottom: 0.5rem;
    border-bottom: 3px solid;
    border-image: linear-gradient(135deg, #6C63FF, #E44EC6) 1;
    display: inline-block;
}

/* Enrollment Card */
.enrollment-card {
    background: linear-gradient(145deg, #1A1A2E, #16213E);
    border: 1px solid rgba(44,182,125,0.2);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.enrollment-id {
    color: #6C63FF;
    font-weight: 700;
    font-size: 0.85rem;
}

/* Wishlist */
.wishlist-card {
    background: linear-gradient(145deg, #1A1A2E, #16213E);
    border: 1px solid rgba(255,101,132,0.2);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

/* Success/Error Messages */
.success-box {
    background: rgba(44,182,125,0.1);
    border: 1px solid rgba(44,182,125,0.3);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    color: #2CB67D;
    font-weight: 500;
}
.error-box {
    background: rgba(229,49,112,0.1);
    border: 1px solid rgba(229,49,112,0.3);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    color: #E53170;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)


# ======================== API HELPER FUNCTIONS ========================
def api_get(endpoint, params=None):
    try:
        res = requests.get(f"{BASE_URL}{endpoint}", params=params, timeout=10)
        res.raise_for_status()
        return res.json(), None
    except requests.exceptions.ConnectionError:
        return None, "❌ Cannot connect to backend. Ensure it is running on port 8000."
    except requests.exceptions.HTTPError as e:
        try:
            return None, res.json().get("detail", str(e))
        except Exception:
            return None, str(e)
    except Exception as e:
        return None, str(e)

def api_post(endpoint, json_data=None, params=None):
    try:
        res = requests.post(f"{BASE_URL}{endpoint}", json=json_data, params=params, timeout=10)
        if res.status_code in [200, 201]:
            return res.json(), None
        try:
            detail = res.json().get("detail", res.text)
        except Exception:
            detail = res.text
        return None, detail
    except requests.exceptions.ConnectionError:
        return None, "❌ Cannot connect to backend."
    except Exception as e:
        return None, str(e)

def api_put(endpoint, params=None):
    try:
        res = requests.put(f"{BASE_URL}{endpoint}", params=params, timeout=10)
        res.raise_for_status()
        return res.json(), None
    except requests.exceptions.ConnectionError:
        return None, "❌ Cannot connect to backend."
    except requests.exceptions.HTTPError:
        try:
            return None, res.json().get("detail", res.text)
        except Exception:
            return None, res.text
    except Exception as e:
        return None, str(e)

def api_delete(endpoint):
    try:
        res = requests.delete(f"{BASE_URL}{endpoint}", timeout=10)
        res.raise_for_status()
        return res.json(), None
    except requests.exceptions.ConnectionError:
        return None, "❌ Cannot connect to backend."
    except requests.exceptions.HTTPError:
        try:
            return None, res.json().get("detail", res.text)
        except Exception:
            return None, res.text
    except Exception as e:
        return None, str(e)


# ======================== UI HELPER FUNCTIONS ========================
def render_course_card(c, show_actions=True, card_class="course-card"):
    price_display = "FREE" if c['price'] == 0 else f"₹{c['price']:,}"
    seats_class = "seats-low" if c['seats_left'] <= 5 else "seats-tag"
    free_badge = '<span class="badge badge-free">FREE</span>' if c['price'] == 0 else ""

    st.markdown(f"""
<div class="{card_class}">
<div class="course-title">📘 {c['title']}</div>
<div class="course-instructor">👤 {c['instructor']}</div>
<div class="course-meta">
<span class="badge badge-category">{c['category']}</span>
<span class="badge badge-level">{c['level']}</span>
{free_badge}
</div>
<div style="display:flex; justify-content:space-between; align-items:center; margin-top:0.8rem;">
<span class="price-tag">{price_display}</span>
<span class="{seats_class}">🪑 {c['seats_left']} seats left</span>
</div>
<div style="color:#555; font-size:0.8rem; margin-top:0.3rem;">ID: {c['id']}</div>
</div>
""", unsafe_allow_html=True)

    if show_actions:
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button(f"💖 Wishlist", key=f"wish_{card_class}_{c['id']}"):
                data, err = api_post("/wishlist/add", params={"course_id": c['id']})
                if err:
                    st.error(err)
                else:
                    st.success(data.get("message", "Added!"))
        with col_b:
            if st.button(f"📝 Enroll", key=f"enroll_{card_class}_{c['id']}"):
                st.session_state["enroll_course_id"] = c['id']
                st.session_state["page"] = "📝 Enroll"
                st.rerun()


def render_metric(label, value, emoji=""):
    st.markdown(f"""
<div class="metric-card">
<div class="metric-value">{emoji} {value}</div>
<div class="metric-label">{label}</div>
</div>
""", unsafe_allow_html=True)


# ======================== SIDEBAR NAVIGATION ========================
st.sidebar.markdown("""
<div style="text-align:center; padding: 1rem 0 1.5rem 0;">
<span style="font-size:2.5rem;">🎓</span>
<h2 style="margin:0.3rem 0 0 0; font-weight:800; background: linear-gradient(135deg, #6C63FF, #E44EC6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
LearnHub
</h2>
<p style="color:#A7A9BE; font-size:0.8rem; margin:0;">Online Course Platform</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.divider()

pages = [
    "🏠 Home",
    "📚 Browse Courses",
    "🔍 Filter Courses",
    "🔎 Search Courses",
    "📄 Course Details",
    "📝 Enroll",
    "🎒 My Enrollments",
    "💖 Wishlist",
    "➕ Add Course",
    "✏️ Update Course",
    "🗑️ Delete Course",
]

if "page" not in st.session_state:
    st.session_state["page"] = "🏠 Home"

selected = st.sidebar.radio("Navigation", pages, index=pages.index(st.session_state["page"]) if st.session_state["page"] in pages else 0, label_visibility="collapsed")
st.session_state["page"] = selected

st.sidebar.divider()
st.sidebar.markdown("""
<div style="text-align:center; padding:0.5rem; color:#A7A9BE; font-size:0.75rem;">
    <p>Coupons: <b>STUDENT20</b> · <b>FLAT500</b></p>
    <p style="margin-top:0.5rem;"> © 2026 LearnHub - Shravan Shidruk (All Rights Reserved)</p>
</div>
""", unsafe_allow_html=True)


# ======================== PAGE: HOME ========================
if selected == "🏠 Home":
    # Hero
    st.markdown("""
<div class="hero-banner">
<h1>Welcome to LearnHub 🚀</h1>
<p>Discover world-class courses from expert instructors. Learn at your own pace, earn certificates, and advance your career.</p>
</div>
""", unsafe_allow_html=True)

    # Summary Metrics
    summary, err = api_get("/courses/summary")
    if err:
        st.error(err)
    else:
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            render_metric("Total Courses", summary["total_courses"], "📚")
        with c2:
            render_metric("Free Courses", summary["free_courses"], "🆓")
        with c3:
            render_metric("Total Seats", summary["total_seats"], "🪑")
        with c4:
            exp = summary.get("most_expensive_course")
            render_metric("Top Price", f"₹{exp['price']:,}" if exp else "N/A", "💎")

        st.markdown("---")

        # Category breakdown
        st.markdown('<div class="section-header">📊 Courses by Category</div>', unsafe_allow_html=True)
        cat_count = summary.get("category_count", {})
        cols = st.columns(len(cat_count)) if cat_count else []
        for i, (cat, count) in enumerate(cat_count.items()):
            with cols[i]:
                render_metric(cat, count, "📁")

    st.markdown("---")

    # Featured courses (first 4)
    st.markdown('<div class="section-header">🌟 Featured Courses</div>', unsafe_allow_html=True)
    data, err = api_get("/courses/page", params={"page": 1, "limit": 4})
    if err:
        st.error(err)
    elif data:
        cols = st.columns(2)
        for i, c in enumerate(data):
            with cols[i % 2]:
                render_course_card(c, show_actions=True, card_class="course-card")


# ======================== PAGE: BROWSE COURSES ========================
elif selected == "📚 Browse Courses":
    st.markdown('<div class="section-header">📚 Browse Courses</div>', unsafe_allow_html=True)

    with st.expander("🔧 Filters & Sorting", expanded=True):
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            keyword = st.text_input("🔎 Keyword", placeholder="e.g. Machine Learning")
            category = st.selectbox("📁 Category", ["All", "Data Science", "Web Dev", "Design", "DevOps"])
        with fc2:
            level = st.selectbox("📊 Level", ["All", "Beginner", "Intermediate", "Advanced"])
            max_price = st.slider("💰 Max Price (₹)", 0, 10000, 10000, step=100)
        with fc3:
            sort_by = st.selectbox("📈 Sort By", ["price", "title", "seats_left"])
            order = st.selectbox("🔃 Order", ["asc", "desc"])

        fc4, fc5 = st.columns(2)
        with fc4:
            page_num = st.number_input("Page", min_value=1, value=1, step=1)
        with fc5:
            limit = st.selectbox("Per Page", [3, 5, 10], index=1)

    params = {"sort_by": sort_by, "order": order, "page": page_num, "limit": limit}
    if keyword:
        params["keyword"] = keyword
    if category != "All":
        params["category"] = category
    if level != "All":
        params["level"] = level
    if max_price < 10000:
        params["max_price"] = max_price

    data, err = api_get("/courses/browse", params=params)
    if err:
        st.error(err)
    elif data:
        pag = data.get("pagination", {})
        st.info(f"Showing page **{pag.get('current_page',1)}** of **{pag.get('total_pages',1)}** — **{pag.get('total_results',0)}** results found")

        courses_list = data.get("data", [])
        if not courses_list:
            st.warning("No courses found with the selected filters.")
        else:
            cols = st.columns(2)
            for i, c in enumerate(courses_list):
                with cols[i % 2]:
                    render_course_card(c)


# ======================== PAGE: FILTER COURSES ========================
elif selected == "🔍 Filter Courses":
    st.markdown('<div class="section-header">🔍 Filter Courses</div>', unsafe_allow_html=True)

    fc1, fc2 = st.columns(2)
    with fc1:
        cat = st.selectbox("Category", ["", "Data Science", "Web Dev", "Design", "DevOps"])
        lvl = st.selectbox("Level", ["", "Beginner", "Intermediate", "Advanced"])
    with fc2:
        mp = st.number_input("Max Price (₹)", min_value=0, value=0, step=100)
        hs = st.checkbox("Only available courses (has seats)")

    if st.button("🔍 Apply Filter", use_container_width=True):
        params = {}
        if cat:
            params["category"] = cat
        if lvl:
            params["level"] = lvl
        if mp > 0:
            params["max_price"] = mp
        if hs:
            params["has_seats"] = True

        data, err = api_get("/courses/filter", params=params)
        if err:
            st.error(err)
        else:
            st.success(f"✅ Found **{data['total']}** courses")
            for c in data["courses"]:
                render_course_card(c)


# ======================== PAGE: SEARCH COURSES ========================
elif selected == "🔎 Search Courses":
    st.markdown('<div class="section-header">🔎 Search Courses</div>', unsafe_allow_html=True)

    keyword = st.text_input("Enter keyword (title, instructor, or category)", placeholder="e.g. React, Andrew, DevOps")

    if st.button("🔎 Search", use_container_width=True) and keyword:
        data, err = api_get("/courses/search", params={"keyword": keyword})
        if err:
            st.error(err)
        else:
            st.info(f"Found **{data['total']}** results for _\"{keyword}\"_")
            if data["data"]:
                cols = st.columns(2)
                for i, c in enumerate(data["data"]):
                    with cols[i % 2]:
                        render_course_card(c)
            else:
                st.warning("No courses match your search.")


# ======================== PAGE: COURSE DETAILS ========================
elif selected == "📄 Course Details":
    st.markdown('<div class="section-header">📄 Course Details</div>', unsafe_allow_html=True)

    cid = st.number_input("Enter Course ID", min_value=1, value=1, step=1)

    if st.button("🔍 Fetch Course", use_container_width=True):
        data, err = api_get(f"/courses/{cid}")
        if err:
            st.error(f"Course not found: {err}")
        else:
            render_course_card(data)


# ======================== PAGE: ENROLL ========================
elif selected == "📝 Enroll":
    st.markdown('<div class="section-header">📝 Enroll in a Course</div>', unsafe_allow_html=True)

    with st.form("enroll_form"):
        ec1, ec2 = st.columns(2)
        with ec1:
            student_name = st.text_input("👤 Your Name *", placeholder="John Doe")
            email = st.text_input("📧 Email *", placeholder="john@example.com")
            course_id = st.number_input("🆔 Course ID *", min_value=1, value=st.session_state.get("enroll_course_id", 1), step=1)
        with ec2:
            payment = st.selectbox("💳 Payment Method", ["card", "upi", "netbanking", "wallet"])
            coupon = st.text_input("🎟️ Coupon Code", placeholder="STUDENT20 or FLAT500")
            gift = st.checkbox("🎁 Gift Enrollment")

        recipient = ""
        if gift:
            recipient = st.text_input("🎁 Recipient Name *", placeholder="Recipient's full name")

        submitted = st.form_submit_button("🚀 Enroll Now", use_container_width=True)

    if submitted:
        if not student_name or not email:
            st.error("Please fill in all required fields.")
        else:
            payload = {
                "student_name": student_name,
                "course_id": int(course_id),
                "email": email,
                "payment_method": payment,
                "coupon_code": coupon,
                "gift_enrollment": gift,
                "recipient_name": recipient,
            }
            data, err = api_post("/enrollments", json_data=payload)
            if err:
                st.error(f"❌ Enrollment failed: {err}")
            else:
                st.balloons()
                st.markdown(f"""
<div class="success-box">
✅ <b>Enrollment Successful!</b><br>
📋 Enrollment ID: <b>#{data['enrollment_id']}</b><br>
📚 Course: <b>{data['course']}</b><br>
💰 Original: ₹{data['original_course_price']:,} → Final: <b>₹{data['final_fee']:,}</b><br>
🎟️ Early Bird Discount: ₹{data['discounts']['early_bird']:,} | Coupon: ₹{data['discounts']['coupon']:,}
</div>
""", unsafe_allow_html=True)


# ======================== PAGE: MY ENROLLMENTS ========================
elif selected == "🎒 My Enrollments":
    st.markdown('<div class="section-header">🎒 My Enrollments</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📋 All Enrollments", "🔎 Search", "📈 Sort"])

    with tab1:
        # Paginated view
        ep1, ep2 = st.columns(2)
        with ep1:
            e_page = st.number_input("Page", min_value=1, value=1, step=1, key="ep")
        with ep2:
            e_limit = st.selectbox("Per Page", [3, 5, 10], index=1, key="el")

        data, err = api_get("/enrollments/page", params={"page": e_page, "limit": e_limit})
        if err:
            st.error(err)
        elif data:
            st.info(f"Page **{data['page']}** — Total enrollments: **{data['total']}**")
            if not data["data"]:
                st.warning("No enrollments yet. Go enroll in a course!")
            for e in data["data"]:
                st.markdown(f"""
<div class="enrollment-card">
<div class="enrollment-id">Enrollment #{e['enrollment_id']}</div>
<div class="course-title">{e['course']}</div>
<div class="course-instructor">👤 Student: {e['student']} | 👨‍🏫 Instructor: {e['course_instructor']}</div>
<div style="margin-top:0.5rem;">
💰 Original: ₹{e['original_course_price']:,} → Final: <b style="color:#2CB67D;">₹{e['final_fee']:,}</b><br>
🎟️ Early Bird: -₹{e['discounts']['early_bird']:,} | Coupon: -₹{e['discounts']['coupon']:,}<br>
💳 Payment: {e['payment_method']}
{"<br>🎁 Gift for: " + e['recipient'] if e.get('gift') and e.get('recipient') else ""}
</div>
</div>
""", unsafe_allow_html=True)

    with tab2:
        search_name = st.text_input("Search by student name", key="en_search")
        if st.button("🔎 Search Enrollments") and search_name:
            data, err = api_get("/enrollments/search", params={"name": search_name})
            if err:
                st.error(err)
            elif data:
                st.info(f"Found **{len(data)}** enrollments")
                for e in data:
                    st.markdown(f"""
<div class="enrollment-card">
<div class="enrollment-id">#{e['enrollment_id']}</div>
<b>{e['course']}</b> — {e['student']} — ₹{e['final_fee']:,}
</div>
""", unsafe_allow_html=True)

    with tab3:
        sort_order = st.selectbox("Sort by Final Fee", ["asc", "desc"], key="en_sort")
        if st.button("📈 Sort Enrollments"):
            data, err = api_get("/enrollments/sort", params={"order": sort_order})
            if err:
                st.error(err)
            elif data:
                for e in data.get("data", []):
                    st.markdown(f"""
<div class="enrollment-card">
<div class="enrollment-id">#{e['enrollment_id']}</div>
<b>{e['course']}</b> — {e['student']} — <span style="color:#2CB67D; font-weight:700;">₹{e['final_fee']:,}</span>
</div>
""", unsafe_allow_html=True)


# ======================== PAGE: WISHLIST ========================
elif selected == "💖 Wishlist":
    st.markdown('<div class="section-header">💖 My Wishlist</div>', unsafe_allow_html=True)

    # Add to wishlist
    with st.expander("➕ Add Course to Wishlist", expanded=False):
        add_id = st.number_input("Course ID to add", min_value=1, value=1, step=1, key="w_add")
        if st.button("💖 Add to Wishlist", use_container_width=True):
            data, err = api_post("/wishlist/add", params={"course_id": int(add_id)})
            if err:
                st.error(err)
            else:
                st.success(data.get("message", "Added!"))
                st.rerun()

    # View wishlist
    data, err = api_get("/wishlist")
    if err:
        st.error(err)
    elif data:
        if data["total"] == 0:
            st.info("Your wishlist is empty. Browse courses and add some! 💖")
        else:
            st.markdown(f"""
<div class="metric-card" style="margin-bottom:1.5rem;">
<div class="metric-value">💖 {data['total']} Courses</div>
<div class="metric-label">Total Value: ₹{data['total_price_of_all_wishlisted_items']:,}</div>
</div>
""", unsafe_allow_html=True)

            for c in data["data"]:
                render_course_card(c, show_actions=False, card_class="wishlist-card")
                col_r, col_e = st.columns(2)
                with col_r:
                    if st.button(f"🗑️ Remove", key=f"wr_{c['id']}"):
                        _, err = api_delete(f"/wishlist/{c['id']}")
                        if err:
                            st.error(err)
                        else:
                            st.success("Removed from wishlist!")
                            st.rerun()
                with col_e:
                    if st.button(f"📝 Enroll Now", key=f"we_{c['id']}"):
                        st.session_state["enroll_course_id"] = c['id']
                        st.session_state["page"] = "📝 Enroll"
                        st.rerun()


# ======================== PAGE: ADD COURSE ========================
elif selected == "➕ Add Course":
    st.markdown('<div class="section-header">➕ Add New Course</div>', unsafe_allow_html=True)

    with st.form("add_course_form"):
        ac1, ac2 = st.columns(2)
        with ac1:
            title = st.text_input("📚 Course Title *", placeholder="Machine Learning A-Z")
            instructor = st.text_input("👨‍🏫 Instructor *", placeholder="Dr. Smith")
            category = st.selectbox("📁 Category *", ["Data Science", "Web Dev", "Design", "DevOps"])
        with ac2:
            level = st.selectbox("📊 Level *", ["Beginner", "Intermediate", "Advanced"])
            price = st.number_input("💰 Price (₹) *", min_value=0, value=0, step=100)
            seats = st.number_input("🪑 Seats", min_value=0, value=10, step=1)

        submitted = st.form_submit_button("➕ Add Course", use_container_width=True)

    if submitted:
        if not title or not instructor:
            st.error("Title and Instructor are required!")
        else:
            payload = {
                "title": title,
                "instructor": instructor,
                "category": category,
                "level": level,
                "price": price,
                "seats_left": seats,
            }
            data, err = api_post("/courses", json_data=payload)
            if err:
                st.error(f"❌ {err}")
            else:
                st.success(f"✅ Course **{data['title']}** added with ID **{data['id']}**!")
                render_course_card(data, show_actions=False)


# ======================== PAGE: UPDATE COURSE ========================
elif selected == "✏️ Update Course":
    st.markdown('<div class="section-header">✏️ Update Course</div>', unsafe_allow_html=True)

    cid = st.number_input("🆔 Course ID", min_value=1, value=1, step=1, key="upd_id")

    # Show current info
    if st.button("🔍 Load Course Info"):
        data, err = api_get(f"/courses/{cid}")
        if err:
            st.error(err)
        else:
            st.session_state["update_course_data"] = data

    if "update_course_data" in st.session_state:
        cd = st.session_state["update_course_data"]
        st.info(f"Current: **{cd['title']}** — Price: ₹{cd['price']:,} — Seats: {cd['seats_left']}")

        uc1, uc2 = st.columns(2)
        with uc1:
            new_price = st.number_input("New Price (₹)", min_value=0, value=cd["price"], step=100)
        with uc2:
            new_seats = st.number_input("New Seats", min_value=0, value=cd["seats_left"], step=1)

        if st.button("✏️ Update Course", use_container_width=True):
            params = {}
            if new_price != cd["price"]:
                params["price"] = new_price
            if new_seats != cd["seats_left"]:
                params["seats"] = new_seats

            if not params:
                st.warning("No changes detected.")
            else:
                data, err = api_put(f"/courses/{cid}", params=params)
                if err:
                    st.error(err)
                else:
                    st.success("✅ Course updated successfully!")
                    render_course_card(data, show_actions=False)
                    del st.session_state["update_course_data"]


# ======================== PAGE: DELETE COURSE ========================
elif selected == "🗑️ Delete Course":
    st.markdown('<div class="section-header">🗑️ Delete Course</div>', unsafe_allow_html=True)

    st.warning("⚠️ This action is irreversible. Courses with active enrollments cannot be deleted.")

    cid = st.number_input("🆔 Course ID to delete", min_value=1, value=1, step=1, key="del_id")

    # Preview
    if st.button("🔍 Preview Course"):
        data, err = api_get(f"/courses/{cid}")
        if err:
            st.error(err)
        else:
            render_course_card(data, show_actions=False)
            st.session_state["delete_preview"] = True

    if st.session_state.get("delete_preview"):
        st.markdown("---")
        confirm = st.checkbox("I confirm I want to delete this course", key="del_confirm")
        if confirm:
            if st.button("🗑️ Delete Course", type="primary", use_container_width=True):
                data, err = api_delete(f"/courses/{cid}")
                if err:
                    st.error(err)
                else:
                    msg = data.get("message", "Done")
                    if "Cannot" in msg:
                        st.error(f"❌ {msg}")
                    else:
                        st.success(f"✅ {msg}")
                    st.session_state["delete_preview"] = False