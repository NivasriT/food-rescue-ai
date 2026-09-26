import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
from datetime import datetime, timedelta
import io

# Import local helper modules
import database as db
import ml_models as ml

# Page Configuration
st.set_page_config(
    page_title="Food Rescue AI - Hackathon MVP",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize data folders and seed data
db.init_db()

# --- CUSTOM CSS FOR PREMIUM HACKATHON AESTHETICS ---
st.markdown("""
<style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    /* Font styling overrides */
    h1, h2, h3, h4, h5, h6, p, span, div, .stHeading {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    .main-title {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700;
        color: #064E3B; /* Deep Forest Green */
        background: linear-gradient(135deg, #059669 0%, #10B981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    /* Custom KPI Cards */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid rgba(16, 185, 129, 0.15);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
        transition: all 0.3s ease;
        border-left: 5px solid #10B981; /* Emerald Green */
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 24px rgba(16, 185, 129, 0.1);
    }
    
    .kpi-title {
        font-size: 0.9rem;
        color: #6B7280;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .kpi-value {
        font-size: 2rem;
        font-weight: 700;
        color: #0F172A;
        margin: 0.25rem 0;
    }
    
    .kpi-icon {
        float: right;
        font-size: 2.2rem;
        opacity: 0.8;
    }
    
    /* Styled Sections and Glass Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.85);
        border: 1px solid rgba(16, 185, 129, 0.15);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.04);
        margin-bottom: 1.5rem;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #F0FDF4; /* Light Mint Green */
        border-right: 1px solid #D1FAE5;
    }
    
    /* Badge styling */
    .priority-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .badge-critical {
        background-color: #FEE2E2;
        color: #EF4444;
        border: 1px solid #FCA5A5;
    }
    .badge-high {
        background-color: #FEF3C7;
        color: #D97706;
        border: 1px solid #FCD34D;
    }
    .badge-medium {
        background-color: #EFF6FF;
        color: #2563EB;
        border: 1px solid #93C5FD;
    }
    .badge-low {
        background-color: #D1FAE5;
        color: #059669;
        border: 1px solid #6EE7B7;
    }
    
    /* Step Cards for Home */
    .step-card {
        background: #FFFFFF;
        border: 1px solid rgba(16, 185, 129, 0.1);
        border-radius: 10px;
        padding: 1.25rem;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.02);
    }
    
    .step-number {
        width: 35px;
        height: 35px;
        line-height: 35px;
        background: #10B981;
        color: white;
        border-radius: 50%;
        margin: 0 auto 0.75rem auto;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# Define Sidebar Menu
st.sidebar.markdown("<div style='text-align: center; padding-bottom: 10px;'><h2 style='color:#059669; margin-bottom:2px;'>🥗 RescueAI</h2><p style='color: #6B7280; font-size:0.9rem; margin-top:2px;'>Zero Waste Logistics</p></div>", unsafe_allow_html=True)
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigation System",
    [
        "🏠 Home & Overview",
        "🏢 Partner Registration",
        "📤 Food Donation Upload",
        "🤖 AI Food Detection",
        "🍏 Freshness Predictor",
        "🤝 NGO Matching Tool",
        "📊 Impact Analytics",
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """🔋 Local Database Active  
    🌱 **Eco-Carbon Saver** Enabled"""
)

# Helper function to get status badge HTML
def get_priority_badge(priority_str):
    if "CRITICAL" in priority_str:
        return f'<span class="priority-badge badge-critical">{priority_str}</span>'
    elif "HIGH" in priority_str:
        return f'<span class="priority-badge badge-high">{priority_str}</span>'
    elif "MEDIUM" in priority_str:
        return f'<span class="priority-badge badge-medium">{priority_str}</span>'
    else:
        return f'<span class="priority-badge badge-low">{priority_str}</span>'

# ==========================================
# PAGE 1: HOME & OVERVIEW
# ==========================================
if menu == "🏠 Home & Overview":
    st.markdown("<h1 class='main-title'>Food Rescue AI Platform</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='color: #4B5563; margin-top: -10px;'>Intelligent Redistribution & Safe Conservation Network</h4>", unsafe_allow_html=True)
    st.markdown("---")

    # Load stats
    restaurants = db.load_restaurants()
    ngos = db.load_ngos()
    donations = db.load_donations()
    
    total_food_rescued = sum(d["quantity_kg"] for d in donations)
    total_carbon_saved = sum(d["carbon_saved_kg"] for d in donations)
    active_partners = len(restaurants) + len(ngos)

    # Metric Banner (HTML/CSS layout)
    st.markdown(
        f"""
        <div class="kpi-container">
            <div class="kpi-card">
                <span class="kpi-icon">🍲</span>
                <div class="kpi-title">Rescued Food</div>
                <div class="kpi-value">{total_food_rescued:,.1f} kg</div>
                <div style="font-size:0.8rem; color:#059669; font-weight:600;">↑ 12% this week</div>
            </div>
            <div class="kpi-card">
                <span class="kpi-icon">🏢</span>
                <div class="kpi-title">Active Restaurants</div>
                <div class="kpi-value">{len(restaurants)} Partners</div>
                <div style="font-size:0.8rem; color:#6B7280;">B2B Supply Nodes</div>
            </div>
            <div class="kpi-card">
                <span class="kpi-icon">🤝</span>
                <div class="kpi-title">Registered NGOs</div>
                <div class="kpi-value">{len(ngos)} Outlets</div>
                <div style="font-size:0.8rem; color:#6B7280;">Distribution Outlets</div>
            </div>
            <div class="kpi-card">
                <span class="kpi-icon">🌱</span>
                <div class="kpi-title">CO2 Emissions Saved</div>
                <div class="kpi-value">{total_carbon_saved:,.1f} kg</div>
                <div style="font-size:0.8rem; color:#059669; font-weight:600;">Net Positive Action</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Core Presentation layout
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("💡 Key Strategic Objectives")
        st.markdown(
            """
            * **Real-time Surveillance**: AI Food Detection simulates photo-scans of surplus ingredients to class-identify waste categories instantly.
            * **Safety Prioritization**: Rule-based Freshness calculations use ambient refrigerator variables to lock down strict timelines.
            * **Proximity Logistics**: Euclidean coordinate mapping connects donating restaurants with localized NGOs in seconds, minimizing fuel burn.
            * **Impact Tracking**: Transparent monitoring of food weights and carbon equivalent offsets.
            """
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Step-by-Step Flow Chart
        st.subheader("🏁 Redistribution Pipeline Flow")
        step_cols = st.columns(4)
        headings = ["1. Register", "2. Upload Photo & Info", "3. AI Scan & Score", "4. Match & Collect"]
        descs = ["Sign up restaurants and local NGOs.", "Supply weight, hours since prep, storage temp.", "RescueAI computes safe shelf-life hours & priority.", "Nearest helper matches via shortest distances."]
        for i, sc in enumerate(step_cols):
            with sc:
                st.markdown(
                    f"""
                    <div class="step-card">
                        <div class="step-number">{i+1}</div>
                        <h4 style="margin: 5px 0;">{headings[i]}</h4>
                        <p style="font-size: 0.8rem; color: #6B7280; margin: 0;">{descs[i]}</p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
    with col2:
        st.subheader("🔔 Urgent Donation Bulletins")
        pending_donations = [d for d in donations if d["status"] != "Collected"]
        
        if pending_donations:
            for d in pending_donations[:3]:
                priority_html = get_priority_badge(d["priority"])
                st.markdown(
                    f"""
                    <div style="background: rgba(255,255,255,0.7); border: 1px solid rgba(16, 185, 129, 0.15); border-radius:10px; padding:1rem; margin-bottom:0.75rem; box-shadow: 0 2px 8px rgba(0,0,0,0.01);">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <strong>{d["detected_food"]}</strong>
                            {priority_html}
                        </div>
                        <div style="font-size:0.85rem; color:#4B5563; margin-top:0.4rem;">
                            🏢 From: {d["restaurant_name"]} ({d["quantity_kg"]} kg)<br>
                            🕰️ Shelf life remaining: <strong>{d["safe_hours_remaining"]} hrs</strong><br>
                            🤝 Matched NGO: <strong>{d["nearest_ngo_name"]}</strong> ({d["nearest_ngo_distance"]} km)
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info("All donations have been collected. Outstanding active bulletins will show here.")



# ==========================================
# PAGE 2: PARTNER REGISTRATION
# ==========================================
elif menu == "🏢 Partner Registration":
    st.markdown("<h1 class='main-title'>Partner Registration Node</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#555;'>Register new supplier establishments and distribution NGO warehouses to extend our rescue density grid.</p>", unsafe_allow_html=True)
    st.markdown("---")

    reg_tabs = st.tabs(["🏗️ Register Restaurant", "🏥 Register NGO", "📖 Active Partner Registry"])
    
    with reg_tabs[0]:
        st.subheader("New Restaurant Supplier Form")
        with st.form("restaurant_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                res_name = st.text_input("Restaurant Name*", placeholder="e.g., Gourmet Kitchen")
                cuisine = st.text_input("Cuisine Profile*", placeholder="e.g., Asian Fusion, Bakery, Indian")
                phone = st.text_input("Contact Info*", placeholder="e.g., +91 99000 00001")
            with col2:
                st.info("📍 Coordinates: Use Bengaluru defaults or mock values to maintain active matching proximity.")
                lat = st.number_input("Latitude Coords*", min_value=-90.0, max_value=90.0, value=12.9716, format="%.6f")
                lon = st.number_input("Longitude Coords*", min_value=-180.0, max_value=180.0, value=77.5946, format="%.6f")
            
            submit_res = st.form_submit_button("Register Restaurant Partner")
            if submit_res:
                if not res_name or not cuisine or not phone:
                    st.error("Please fill in all mandatory (*) fields.")
                else:
                    new_id = f"R{len(db.load_restaurants()) + 1}"
                    new_res = {
                        "id": new_id,
                        "name": res_name,
                        "cuisine": cuisine,
                        "phone": phone,
                        "latitude": lat,
                        "longitude": lon,
                        "joined_date": datetime.now().strftime("%Y-%m-%d")
                    }
                    db.add_restaurant(new_res)
                    st.success(f"🎉 Restaurant '{res_name}' successfully added to the database under ID [{new_id}].")

    with reg_tabs[1]:
        st.subheader("New NGO Warehouse Form")
        with st.form("ngo_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                ngo_name = st.text_input("NGO Name*", placeholder="e.g., Save Clean Food Foundation")
                focus_area = st.text_input("Food Focus Focus Area*", placeholder="e.g., Excess Cooked Meals, Bread & Produce")
                ngo_phone = st.text_input("Contact Info*", placeholder="e.g., +91 99000 00009")
                capacity = st.number_input("Storage Capacity (kg)*", min_value=10, max_value=10000, value=200)
            with col2:
                st.info("📍 Coordinates: Enter spatial coordinates (must be in close proximity to the restaurants to show short distances).")
                ngo_lat = st.number_input("NGO Latitude*", min_value=-90.0, max_value=90.0, value=12.9780, format="%.6f")
                ngo_lon = st.number_input("NGO Longitude*", min_value=-180.0, max_value=180.0, value=77.6030, format="%.6f")
            
            submit_ngo = st.form_submit_button("Register NGO Partner")
            if submit_ngo:
                if not ngo_name or not focus_area or not ngo_phone:
                    st.error("Please fill in all mandatory (*) fields.")
                else:
                    new_id = f"N{len(db.load_ngos()) + 1}"
                    new_ngo = {
                        "id": new_id,
                        "name": ngo_name,
                        "focus_area": focus_area,
                        "phone": ngo_phone,
                        "latitude": ngo_lat,
                        "longitude": ngo_lon,
                        "capacity_kg": capacity,
                        "joined_date": datetime.now().strftime("%Y-%m-%d")
                    }
                    db.add_ngo(new_ngo)
                    st.success(f"🎉 NGO Warehouse '{ngo_name}' successfully saved under ID [{new_id}].")

    with reg_tabs[2]:
        st.subheader("Registered Active Partners")
        
        # Load tables
        res_list = db.load_restaurants()
        ngo_list = db.load_ngos()
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Supplier Restaurants")
            if res_list:
                df_res = pd.DataFrame(res_list)
                st.dataframe(df_res[["id", "name", "cuisine", "latitude", "longitude", "phone"]], use_container_width=True)
            else:
                st.warning("No restaurants registered.")
        with c2:
            st.markdown("#### Distribution NGOs")
            if ngo_list:
                df_ngo = pd.DataFrame(ngo_list)
                st.dataframe(df_ngo[["id", "name", "focus_area", "capacity_kg", "latitude", "longitude", "phone"]], use_container_width=True)
            else:
                st.warning("No NGOs registered.")

# ==========================================
# PAGE 3: FOOD DONATION UPLOAD (CORE WORKFLOW)
# ==========================================
elif menu == "📤 Food Donation Upload":
    st.markdown("<h1 class='main-title'>Food Donation Dispatch Wizard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#555;'>Perform a complete food rescue flow: upload package details or photos. The AI logic will automatically detect categories, calculate freshness indices, and determine shortest route NGO warehouse delivery coordinates.</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Load datasets
    restaurants = db.load_restaurants()
    ngos = db.load_ngos()
    
    if not restaurants or not ngos:
        st.warning("⚠️ Critical dependency missing to run flow: You must have at least one Restaurant and one NGO registered. Go to 'Partner Registration' first.")
    else:
        # Step 1: Input details
        st.subheader("Step 1: Donation Metadata and Photo Upload")
        
        # We store temporary simulation states in Streamlit session state
        if 'scan_run' not in st.session_state:
            st.session_state.scan_run = False
            st.session_state.detected_data = None
            st.session_state.freshness_data = None
            st.session_state.match_data = None
            
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                # Select Restaurant
                res_names = [f"{r['name']} ({r['id']})" for r in restaurants]
                selected_res_str = st.selectbox("Select Donating Restaurant*", res_names)
                # Map back to restaurant object
                res_id = selected_res_str.split("(")[-1].replace(")", "")
                restaurant_obj = next(r for r in restaurants if r["id"] == res_id)
                
                # Basic attributes
                food_cat = st.selectbox("General Category* (will verify with AI)", ["Cooked Meals", "Produce", "Bakery", "Dairy", "Meat/Seafood"])
                quantity = st.number_input("Food Weight (kg)*", min_value=0.5, max_value=500.0, value=10.0, step=0.5)
                
                # Prep time and storage
                prep_hours = st.slider("Hours Elapsed since Preparation*", min_value=0, max_value=72, value=4, help="How many hours ago was this food prepared/harvested?")
                storage_cond = st.selectbox("Storage Condition*", ["Ambient", "Refrigerated", "Frozen"])
                
            with col2:
                # Image Upload
                st.markdown("**Simulate AI Scan Camera**")
                uploaded_file = st.file_uploader("Food Photo", type=["jpg", "jpeg", "png"])
                
                st.markdown("💡 *OR use a Hackathon Quick Preset image if you don't have a photo:*")
                preset_selected = st.radio("Choose Photo Demo Preset", ["None (Use uploaded file)", "🍕 Pizza", "🥗 Salad/Produce", "🍞 Sourdough Bread", "🍛 Paneer Curry"], index=0)
                
                # Category Hint
                cat_hint = st.text_input("AI Detection Hint (Optional)", placeholder="e.g. Tomato Pizza, Garden Salad")

        # Process button
        st.markdown("<br>", unsafe_allow_html=True)
        btn_col1, btn_col2 = st.columns([1, 4])
        with btn_col1:
            process_btn = st.button("🔍 Run Rescue AI Analysis", use_container_width=True)
            
        if process_btn:
            # Check inputs
            filename = ""
            if uploaded_file:
                filename = uploaded_file.name
            elif preset_selected != "None (Use uploaded file)":
                filename = preset_selected.lower() + ".jpg"
            
            # Fetch AI food classification
            detection = ml.detect_food(filename, cat_hint if cat_hint else (preset_selected if preset_selected != "None" else ""))
            
            # Calculate freshness using formula
            freshness = ml.predict_freshness(detection["food_category"], prep_hours, storage_cond)
            
            # Calculate NGO proximity
            nearest_ngo, sorted_ngos = ml.match_nearest_ngo(restaurant_obj["latitude"], restaurant_obj["longitude"], ngos)
            
            # Save results to session state
            st.session_state.detected_data = {
                "restaurant_id": restaurant_obj["id"],
                "restaurant_name": restaurant_obj["name"],
                "restaurant_lat": restaurant_obj["latitude"],
                "restaurant_lon": restaurant_obj["longitude"],
                "food_category": detection["food_category"],
                "qty": quantity,
                "prep_hours": prep_hours,
                "storage": storage_cond,
                "detected_food": detection["detected_food"],
                "confidence": detection["confidence_score"]
            }
            st.session_state.freshness_data = freshness
            st.session_state.match_data = {
                "nearest_ngo": nearest_ngo,
                "sorted_ngos": sorted_ngos
            }
            st.session_state.scan_run = True

        # Render analysis result card
        if st.session_state.scan_run and st.session_state.detected_data:
            st.markdown("---")
            st.subheader("Step 2: AI Analytics Output & Routing Metrics")
            
            det = st.session_state.detected_data
            fr = st.session_state.freshness_data
            ma = st.session_state.match_data
            carbon_saved = ml.calculate_carbon_saved(det["qty"])
            
            out_col1, out_col2 = st.columns([1, 2])
            with out_col1:
                # Render Image
                st.markdown("**Simulated Captured Input**")
                if uploaded_file:
                    st.image(uploaded_file, caption="Uploaded Package Photo", use_container_width=True)
                else:
                    # Provide customized local SVG/Placeholder for quick demo aesthetics
                    theme_color = "#10B981"
                    if "pizza" in det["detected_food"].lower():
                         emoji = "🍕"
                         detail_name = "Hot Pizza Rescued"
                    elif "salad" in det["detected_food"].lower():
                         emoji = "🥗"
                         detail_name = "Fresh Salad Rescued"
                    elif "bread" in det["detected_food"].lower():
                         emoji = "🍞"
                         detail_name = "Bakery Goods Rescued"
                    elif "curry" in det["detected_food"].lower() or "paneer" in det["detected_food"].lower():
                         emoji = "🍛"
                         detail_name = "Cooked Curries Rescued"
                    else:
                         emoji = "🍲"
                         detail_name = "Fresh Rescued Food"
                         
                    st.markdown(
                        f"""
                        <div style="height:250px; background:linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%); border-radius:12px; display:flex; flex-direction:column; align-items:center; justify-content:center; border:2px dashed #10B981;">
                            <span style="font-size:5rem;">{emoji}</span>
                            <span style="color:#065F46; font-weight:700; margin-top:10px;">{detail_name}</span>
                            <span style="font-size:0.8rem; color:#6B7280;">(Demo Simulation Preset)</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            with out_col2:
                # Metrics layout
                st.markdown(
                    f"""
                    <div style="background:#FFFFFF; border:1px solid rgba(16,185,129,0.2); border-radius:12px; padding:1.5rem; box-shadow:0 4px 15px rgba(0,0,0,0.03);">
                        <h4 style="color:#059669; margin-top:0;">🤖 RescueAI Analysis Summary</h4>
                        <table style="width:100%; border-collapse: collapse; font-size:0.95rem;">
                            <tr style="border-bottom:1px solid #E5E7EB; height:35px;">
                                <td style="font-weight:600; color:#4B5563;">Detected Category:</td>
                                <td style="text-align:right; font-weight:700; color:#111827;">{det["food_category"]}</td>
                            </tr>
                            <tr style="border-bottom:1px solid #E5E7EB; height:35px;">
                                <td style="font-weight:600; color:#4B5563;">Detected Food Item:</td>
                                <td style="text-align:right; font-weight:700; color:#059669;">{det["detected_food"]}</td>
                            </tr>
                            <tr style="border-bottom:1px solid #E5E7EB; height:35px;">
                                <td style="font-weight:600; color:#4B5563;">Scan Confidence Score:</td>
                                <td style="text-align:right;"><span style="background:#D1FAE5; color:#065F46; font-weight:700; padding:2px 8px; border-radius:4px;">{det["confidence"]}%</span></td>
                            </tr>
                            <tr style="border-bottom:1px solid #E5E7EB; height:35px;">
                                <td style="font-weight:600; color:#4B5563;">Freshness Score Index:</td>
                                <td style="text-align:right; font-weight:700; color:#10B981;">{fr["freshness_score"]}%</td>
                            </tr>
                            <tr style="border-bottom:1px solid #E5E7EB; height:35px;">
                                <td style="font-weight:600; color:#4B5563;">Remaining Safe Shelf Life:</td>
                                <td style="text-align:right; font-weight:700; color:#D97706;">{fr["safe_hours_remaining"]} hours left</td>
                            </tr>
                            <tr style="border-bottom:1px solid #E5E7EB; height:35px;">
                                <td style="font-weight:600; color:#4B5563;">Redistribution Priority:</td>
                                <td style="text-align:right;">{get_priority_badge(fr["priority"])}</td>
                            </tr>
                            <tr style="border-bottom:1px solid #E5E7EB; height:35px;">
                                <td style="font-weight:600; color:#4B5563;">CO2 Footprint Prevented:</td>
                                <td style="text-align:right; font-weight:700; color:#059669;">{carbon_saved} kg CO2e</td>
                            </tr>
                            <tr style="height:35px;">
                                <td style="font-weight:600; color:#2563EB;">Closest Matched NGO:</td>
                                <td style="text-align:right; font-weight:700; color:#2563EB;">{ma["nearest_ngo"]["name"]} ({ma["nearest_ngo"]["distance_km"]} km)</td>
                            </tr>
                        </table>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            # Confirm & Broadcast Form
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### Step 3: Broadcast Dispatch Code Details")
            
            with st.form("broadcast_donation_form"):
                st.write(f"This donation of **{det['qty']} kg** of **{det['detected_food']}** will be dispatched immediately to **{ma['nearest_ngo']['name']}**. Location routes have been mapped.")
                
                # Checkbox to bypass manual routing
                bypass_driver = st.checkbox("Automated Dispatch Rider allocation", value=True)
                
                confirm_save = st.form_submit_button("📢 Confirm, Broadcast & Dispatch Donation")
                if confirm_save:
                    new_don_id = f"D{len(db.load_donations()) + 1}"
                    new_donation_record = {
                        "id": new_don_id,
                        "restaurant_id": det["restaurant_id"],
                        "restaurant_name": det["restaurant_name"],
                        "food_category": det["food_category"],
                        "quantity_kg": det["qty"],
                        "prep_time": (datetime.now() - timedelta(hours=det["prep_hours"])).strftime("%Y-%m-%d %H:%M"),
                        "storage_condition": det["storage"],
                        "detected_food": det["detected_food"],
                        "confidence_score": det["confidence"],
                        "freshness_score": fr["freshness_score"],
                        "safe_hours_remaining": fr["safe_hours_remaining"],
                        "priority": fr["priority"],
                        "nearest_ngo_id": ma["nearest_ngo"]["id"],
                        "nearest_ngo_name": ma["nearest_ngo"]["name"],
                        "nearest_ngo_distance": ma["nearest_ngo"]["distance_km"],
                        "carbon_saved_kg": carbon_saved,
                        "status": "Pending",
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                    db.add_donation(new_donation_record)
                    
                    st.balloons()
                    st.success(f"🚀 Success! Donation [{new_don_id}] broadcasted. Notification dispatched to {ma['nearest_ngo']['name']} ({ma['nearest_ngo']['phone']}).")
                    
                    # Reset States
                    st.session_state.scan_run = False
                    st.session_state.detected_data = None
                    st.session_state.freshness_data = None
                    st.session_state.match_data = None

# ==========================================
# PAGE 4: AI Food Detection
# ==========================================
elif menu == "🤖 AI Food Detection":
    st.markdown("<h1 class='main-title'>AI Food Detection Playground</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#555;'>Analyze raw product images to identify food groupings. Features full class-probability outputs based on rule-based processing.</p>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📷 Test Image Input Node")
        uploaded_img = st.file_uploader("Image File", type=["jpg", "png", "jpeg"], key="det_page_uploader")
        
        st.markdown("---")
        preset_det = st.selectbox(
            "Select Camera Presets", 
            ["Manual Upload", "Delicious Cheese Pizza", "Mediterranean Salad Bowl", "Crispy Baguette Bread", "Spicy Vegetable Curry"]
        )
        
        manual_hint = st.text_input("Enter Item Name Descriptor (Optional Hint)", placeholder="Help the AI classification engine...")
        
        analyze_btn = st.button("Start Camera Scanner & Run Classification")
        
    with col2:
        st.subheader("📊 Classified Class Probabilities")
        
        if analyze_btn:
            # Translate selections into files
            name_check = ""
            if preset_det == "Delicious Cheese Pizza":
                name_check = "pizza.jpg"
            elif preset_det == "Mediterranean Salad Bowl":
                name_check = "salad.jpg"
            elif preset_det == "Crispy Baguette Bread":
                name_check = "bread.jpg"
            elif preset_det == "Spicy Vegetable Curry":
                name_check = "curry.jpg"
            elif uploaded_img:
                name_check = uploaded_img.name
                
            if not name_check and not manual_hint:
                st.warning("Please upload an image, select a preset, or write a classifier hint to process.")
            else:
                result = ml.detect_food(name_check, manual_hint)
                
                # Display output cards
                con = result["confidence_score"]
                st.markdown(
                    f"""
                    <div style="background: rgba(16, 185, 129, 0.05); border: 2px solid #10B981; border-radius:10px; padding:1.2rem; margin-bottom:1rem;">
                        <h4 style="color:#065F46; margin:0 0 5px 0;">🎯 Top Match detected:</h4>
                        <h2 style="margin:5px 0; color:#111827;">{result["detected_food"]}</h2>
                        <strong style="color: #6B7280; font-size:0.95rem;">Group Category:</strong> <span style="font-weight:600; color:#059669;">{result["food_category"]}</span>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
                # Show confidence meter
                st.write(f"**Detector Confidence Score: {con}%**")
                st.progress(con / 100.0)
                
                # Mock details
                st.markdown("### 🔍 Model Properties & Classification Log")
                
                # Generates some helper mock probabilities
                other_opts = ["Mixed Fruits", "Pasta Cooked", "Baked Bread", "White Rice", "Green Salads"]
                shuffled_other = [o for o in other_opts if o not in result["detected_food"]]
                
                probs = [
                    {"Class": result["detected_food"], "Probability": con},
                    {"Class": shuffled_other[0], "Probability": round((100 - con) * 0.6, 1)},
                    {"Class": shuffled_other[1], "Probability": round((100 - con) * 0.3, 1)},
                    {"Class": "Other items", "Probability": round((100 - con) * 0.1, 1)}
                ]
                
                df_p = pd.DataFrame(probs)
                fig = px.bar(df_p, x="Probability", y="Class", orientation='h', color="Probability",
                             color_continuous_scale="greens", title="Softmax Probability Distribution (%)")
                fig.update_layout(yaxis={'categoryorder':'total ascending'}, height=250, coloraxis_showscale=False)
                st.plotly_chart(fig, use_container_width=True)

# ==========================================
# PAGE 5: FRESHNESS PREDICTOR
# ==========================================
elif menu == "🍏 Freshness Predictor":
    st.markdown("<h1 class='main-title'>Freshness & Degradation Predictor</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#555;'>Calculate safe holding periods. Modifies decay curve math depending on category, preparation time offsets, and ambient temperature exposure.</p>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.subheader("🎛️ Simulation Parameters")
        
        category = st.selectbox("Food Category Type", ["Produce", "Bakery", "Cooked Meals", "Dairy", "Meat/Seafood"])
        prep_hours = st.slider("Hours Ago Prepared (T-0 Offset)", min_value=0, max_value=120, value=6, step=1)
        storage = st.selectbox("Storage Environmental Condition", ["Ambient", "Refrigerated", "Frozen"])
        
        # Calculate
        pred = ml.predict_freshness(category, prep_hours, storage)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("📝 Preservation Rules Used:")
        rules_df = pd.DataFrame([
            {"Food Type": k, "Base Lifespan (Ambient)": f"{v} hours", "Refrigerated (3x)": f"{v*3} hours", "Frozen (10x)": f"{v*10} hours"}
            for k, v in ml.BASELINE_SHELF_LIFE.items()
        ])
        st.dataframe(rules_df, use_container_width=True)
        
    with col2:
        st.subheader("💡 Predictive Output Analysis")
        
        score = pred["freshness_score"]
        safe_h = pred["safe_hours_remaining"]
        prio = pred["priority"]
        
        # Dial layout chart
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Predicted Freshness Index (%)", 'font': {'size': 20}},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkgreen"},
                'bar': {'color': "#10B981"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "#E5E7EB",
                'steps': [
                    {'range': [0, 30], 'color': '#FEE2E2'},
                    {'range': [30, 70], 'color': '#FEF3C7'},
                    {'range': [70, 100], 'color': '#D1FAE5'}
                ]
            }
        ))
        
        fig.update_layout(height=260, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)
        
        # Text details
        st.markdown(
            f"""
            <div style="background:#FFFFFF; border:1px solid #E5E7EB; border-radius:10px; padding:1.2rem; margin-top:-10px; box-shadow:0 2px 10px rgba(0,0,0,0.01);">
                <table style="width:100%; border-collapse:collapse; font-size:0.95rem;">
                    <tr>
                        <td style="font-weight:600; padding:8px 0; color:#555;">Redistribution Priority:</td>
                        <td style="text-align:right; font-weight:700;">{get_priority_badge(prio)}</td>
                    </tr>
                    <tr>
                        <td style="font-weight:600; padding:8px 0; color:#555;">Estimated Useful Shelf Life:</td>
                        <td style="text-align:right; font-weight:700; color:#059669;">{safe_h} hours remaining</td>
                    </tr>
                    <tr>
                        <td style="font-weight:600; padding:8px 0; color:#555;">Spoilage Risk Profile:</td>
                        <td style="text-align:right; font-weight:700; color:{'#EF4444' if safe_h < 12 else '#D97706' if safe_h < 36 else '#059669'};">
                            {"Extremely Critical (Spoils soon)" if safe_h < 12 else "Moderate (REDISTRIBUTE FAST)" if safe_h < 36 else "Safe / Stable Shelf Life"}
                        </td>
                    </tr>
                </table>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Recommendations
        st.markdown("### 🛡️ Storage Safety Advisories")
        if prio == "UNSAFE 🛑":
            st.error("❌ **CRITICAL DANGER**: Food is expired and unsafe for donation! Avoid redistribution and compost if possible.")
        elif prio == "CRITICAL 🚨":
            st.warning("⚠️ **IMMEDIATE DISPATCH**: Less than 4 hours remaining. Distribute locally to nearby communities IMMEDIATELY. Avoid long transit times.")
        elif prio == "HIGH ⚠️":
            st.warning("⏰ **EXPEDITED DISPATCH**: Target consumption within 12 hours. Deliver to immediate local storage facilities.")
        else:
            st.success("🟢 **STABLE STOCKS**: Suitable for standard shipping. Safe storage thresholds are preserved.")

# ==========================================
# PAGE 6: NGO MATCHING TOOL
# ==========================================
elif menu == "🤝 NGO Matching Tool":
    st.markdown("<h1 class='main-title'>Location Proximity Matched NGOs</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#555;'>Calculate coordinate routing distances. Uses 2D Euclidean spatial distance math scaled to kilometers to identify nearby recipient warehouses.</p>", unsafe_allow_html=True)
    st.markdown("---")

    restaurants = db.load_restaurants()
    ngos = db.load_ngos()

    if not restaurants or not ngos:
        st.warning("⚠️ Register Restaurants and NGOs under 'Partner Registration' to execute route checks.")
    else:
        # Inputs Selector
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Select Supplier Origin")
            res_opt = [f"{r['name']} (ID: {r['id']})" for r in restaurants]
            selected_res_index = st.selectbox("Select Restaurant", res_opt)
            
            res_id = selected_res_index.split("ID: ")[-1].replace(")", "")
            chosen_res = next(r for r in restaurants if r["id"] == res_id)
            
            st.info(
                f"""
                **Coordinates Origin:**  
                📌 Lat: `{chosen_res["latitude"]}`  
                📌 Lon: `{chosen_res["longitude"]}`  
                📞 Contact: `{chosen_res["phone"]}`
                """
            )
            
            # Run Match
            nearest_n, sorted_ns = ml.match_nearest_ngo(chosen_res["latitude"], chosen_res["longitude"], ngos)
            
            st.subheader("🎯 Recommendation Summary")
            st.markdown(
                f"""
                <div style="border: 2px solid #2563EB; background: rgba(37, 99, 235, 0.05); border-radius:10px; padding:1rem; box-shadow:0 2px 10px rgba(0,0,0,0.01);">
                    <h4 style="color:#1D4ED8; margin:0 0 5px 0;">Closest Recipient NGO:</h4>
                    <strong style="font-size:1.15rem; color:#1E293B;">{nearest_n["name"]}</strong>
                    <div style="font-size:0.85rem; color:#4B5563; margin-top:5px;">
                        🚙 Proximity Distance: <strong>{nearest_n["distance_km"]} km</strong><br>
                        📦 Warehouse Cap: {nearest_n["capacity_kg"]} kg<br>
                        📞 Contact: {nearest_n["phone"]}
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
        with col2:
            st.subheader("📍 Urban Spatial Map Simulation")
            
            # Map visual using Plotly
            # Add Restaurant and NGOs to dataframe to display
            points = []
            # Restaurant point
            points.append({
                "Label": f"Restaurant: {chosen_res['name']}",
                "Lat": chosen_res["latitude"],
                "Lon": chosen_res["longitude"],
                "Marker": "Origin Restaurant",
                "Size": 15
            })
            # NGO points
            for n in sorted_ns:
                points.append({
                    "Label": f"NGO: {n['name']} ({n['distance_km']} km)",
                    "Lat": n["latitude"],
                    "Lon": n["longitude"],
                    "Marker": "Recipient NGO",
                    "Size": 10 + (n["capacity_kg"] / 50.0) # size represents capacity
                })
                
            df_points = pd.DataFrame(points)
            
            # 2D Grid Plotly Scatter representing layout of the city
            fig = px.scatter(
                df_points, 
                x="Lon", 
                y="Lat", 
                color="Marker", 
                text="Label", 
                size="Size",
                color_discrete_map={"Origin Restaurant": "#D97706", "Recipient NGO": "#10B981"},
                title=f"Bangalore Grid Proximity: {chosen_res['name']} to NGOs"
            )
            
            # Draw line between restaurant and nearest NGO
            fig.add_trace(go.Scatter(
                x=[chosen_res["longitude"], nearest_n["longitude"]],
                y=[chosen_res["latitude"], nearest_n["latitude"]],
                mode="lines+markers",
                name="Delivery Route Match",
                line=dict(color="#2563EB", width=3, dash="dot"),
                hoverinfo="skip"
            ))
            
            fig.update_layout(
                xaxis_title="Longitude Coordinate",
                yaxis_title="Latitude Coordinate",
                legend_title="Grid Entity",
                height=380,
                xaxis=dict(showgrid=True, gridcolor="#E5E7EB"),
                yaxis=dict(showgrid=True, gridcolor="#E5E7EB"),
                plot_bgcolor="white"
            )
            fig.update_traces(textposition='top center')
            st.plotly_chart(fig, use_container_width=True)
            
            # Sorted Proximity list
            st.subheader("📋 Proximity Distance Audit Log")
            df_table = pd.DataFrame(sorted_ns)
            df_table = df_table.rename(columns={
                "name": "NGO Recipient Name",
                "distance_km": "Euclidean Distance (km)",
                "capacity_kg": "Capacity Limit (kg)",
                "focus_area": "Focus Area"
            })
            st.dataframe(
                df_table[["NGO Recipient Name", "Euclidean Distance (km)", "Capacity Limit (kg)", "phone"]], 
                use_container_width=True
            )

# ==========================================
# PAGE 7: IMPACT ANALYTICS
# ==========================================
elif menu == "📊 Impact Analytics":
    st.markdown("<h1 class='main-title'>Food Rescue Sustainability Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#555;'>Visualizing metrics, carbon savings, food rescued per category, and fulfillment status logs in real-time.</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Load data
    donations = db.load_donations()
    restaurants = db.load_restaurants()
    ngos = db.load_ngos()
    
    if not donations:
        st.warning("No donations registered in database yet. Post some food in 'Food Donation Upload' to render charts.")
    else:
        df = pd.DataFrame(donations)
        
        # High level row
        total_kg = df["quantity_kg"].sum()
        total_co2 = df["carbon_saved_kg"].sum()
        avg_fresh = df["freshness_score"].mean()
        
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric("Cumulative Rescued Food", f"{total_kg:,.1f} kg", "🌱 Active Impact")
        col_m2.metric("Total CO2 Emissions Saved", f"{total_co2:,.1f} kg CO2e", "♻️ Eco-Savings")
        col_m3.metric("Average Freshness Index", f"{avg_fresh:,.1f}%", f"{'Stable' if avg_fresh > 75 else 'Warning'}")
        col_m4.metric("Logged Deliveries", len(df), f"+{len(df[df['status']=='Pending'])} Pending")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Charts Row 1
        c1, c2 = st.columns(2)
        
        with c1:
            # 1. Bar: rescued food by category
            st.markdown("#### Weight Rescued by Food Category (kg)")
            df_cat = df.groupby("food_category")["quantity_kg"].sum().reset_index()
            fig_bar = px.bar(
                df_cat, 
                x="food_category", 
                y="quantity_kg", 
                labels={"food_category": "Food Category", "quantity_kg": "Weight Rescued (kg)"},
                color="quantity_kg", 
                color_continuous_scale="emrld"
            )
            fig_bar.update_layout(plot_bgcolor="rgba(0,0,0,0)", height=300, coloraxis_showscale=False)
            st.plotly_chart(fig_bar, use_container_width=True)
            
        with c2:
            st.markdown("#### Distribution of Fulfillment Statuses")
            df_status = df.groupby("status").size().reset_index(name="counts")
            fig_pie = px.pie(
                df_status, 
                values="counts", 
                names="status", 
                hole=0.45,
                color_discrete_sequence=["#10B981", "#3B82F6", "#EF4444"]
            )
            fig_pie.update_layout(height=300)
            st.plotly_chart(fig_pie, use_container_width=True)
            
        # Charts Row 2
        c3, c4 = st.columns(2)
        
        with c3:
            st.markdown("#### Cumulative Rescued Food Trends (kg)")
            # Create cumulative sum sorted by date
            df_time = df.copy()
            df_time["timestamp_dt"] = pd.to_datetime(df_time["timestamp"])
            df_time = df_time.sort_values("timestamp_dt")
            df_time["cul_kg"] = df_time["quantity_kg"].cumsum()
            
            fig_line = px.line(
                df_time, 
                x="timestamp_dt", 
                y="cul_kg", 
                labels={"timestamp_dt": "Date Logged", "cul_kg": "Total Rescued (kg)"},
                markers=True
            )
            fig_line.update_traces(line_color="#059669")
            fig_line.update_layout(plot_bgcolor="rgba(0,0,0,0)", height=300)
            st.plotly_chart(fig_line, use_container_width=True)
            
        with c4:
            st.markdown("#### Top Rescuing Restaurants (kg)")
            df_rest = df.groupby("restaurant_name")["quantity_kg"].sum().reset_index()
            df_rest = df_rest.sort_values(by="quantity_kg", ascending=False)
            
            fig_rest = px.bar(
                df_rest,
                y="restaurant_name",
                x="quantity_kg",
                orientation='h',
                color="quantity_kg",
                color_continuous_scale="greens",
                labels={"restaurant_name": "Supplier Location", "quantity_kg": "Volume Dispatched (kg)"}
            )
            fig_rest.update_layout(plot_bgcolor="rgba(0,0,0,0)", height=300, coloraxis_showscale=False)
            st.plotly_chart(fig_rest, use_container_width=True)

        # Full logs list
        st.markdown("### 📋 Historic Rescue Dispatches Audit Ledger")
        st.dataframe(
            df[["id", "restaurant_name", "detected_food", "food_category", "quantity_kg", "nearest_ngo_name", "priority", "status", "timestamp"]], 
            use_container_width=True
        )
