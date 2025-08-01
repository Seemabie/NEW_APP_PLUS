import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, date
import time

# Configure page
st.set_page_config(
    page_title="Kirmani's Employee App",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# File paths for data storage
DAILY_REPORTS_FILE = 'daily_reports.json'
REQUESTS_FILE = 'employee_requests.json'
MESSAGES_FILE = 'admin_messages.json'

# Gas Station options
GAS_STATIONS = [
    "🚗 KSK Auto Group",
    "⛽ ONE STOP INC", 
    "🏢 SYED Empires",
    "🌟 S. Micheal",
    "🏪 Verbank"
]

# CLEAN CSS - NO GLOBAL BUTTON STYLING
st.markdown("""
<style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* App container styling */
    .main > div {
        padding: 0;
        max-width: 414px;
        margin: 0 auto;
        background: #f8f9fa;
        min-height: 100vh;
    }
    
    /* Header styling */
    .app-header {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        color: white;
        padding: 2rem;
        text-align: center;
        margin-bottom: 0;
    }
    
    .header-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .station-info {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        padding: 0.8rem 1.2rem;
        margin-top: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .station-name {
        font-weight: 600;
    }
    
    /* Status bar */
    .status-bar {
        background: #fff;
        padding: 1rem;
        border-bottom: 1px solid #e9ecef;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .status-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.9rem;
        color: #6c757d;
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #28a745;
    }
    
    /* Alert styling */
    .alert {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        margin: 1rem;
        border-radius: 8px;
        font-size: 0.9rem;
        color: #856404;
    }
    
    .alert-urgent {
        background: #f8d7da;
        border-left-color: #dc3545;
        color: #721c24;
    }
    
    /* Form styling */
    .form-section {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #e9ecef;
    }
    
    .section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 1.5rem;
    }
    
    /* Results styling */
    .result-item {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .product-name {
        font-size: 1.2rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .product-info {
        font-size: 0.95rem;
        color: #555;
        line-height: 1.6;
        margin-bottom: 0.3rem;
    }
    
    .product-price {
        font-size: 1.1rem;
        font-weight: bold;
        color: #27ae60;
    }
    
    .age-restricted {
        background: #e74c3c;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: bold;
        margin-left: 1rem;
    }
    
    /* Success message */
    .success-message {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem;
        text-align: center;
        font-weight: 600;
    }
    
    /* Search input styling */
    .stTextInput > div > div > input {
        border: 3px solid #667eea;
        border-radius: 20px;
        padding: 1.8rem;
        font-size: 1.3rem;
        font-weight: 500;
        background: #f8f9fa;
        text-align: center;
        transition: all 0.3s ease;
        width: 100%;
        margin: 2rem 0;
    }
    
    .stTextInput > div > div > input:focus {
        background: white;
        box-shadow: 0 0 0 5px rgba(102, 126, 234, 0.15);
        transform: translateY(-2px);
        outline: none;
    }
    
    /* Mobile responsive */
    @media (max-width: 480px) {
        .main > div {
            max-width: 100%;
        }
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_product_data():
    """Load and cache the PLU data"""
    try:
        df = pd.read_csv('glide_products.csv', dtype={'UPC_Code': str})
        df['UPC_Code'] = df['UPC_Code'].astype(str)
        df['UPC_Search'] = df['UPC_Code'].str.lstrip('0')
        return df
    except FileNotFoundError:
        st.error("Please make sure 'glide_products.csv' is in the same directory as this script")
        return pd.DataFrame()

def load_messages():
    """Load admin messages"""
    if os.path.exists(MESSAGES_FILE):
        try:
            with open(MESSAGES_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_daily_report(station, data):
    """Save daily report data"""
    reports = []
    if os.path.exists(DAILY_REPORTS_FILE):
        try:
            with open(DAILY_REPORTS_FILE, 'r') as f:
                reports = json.load(f)
        except:
            reports = []
    
    new_report = {
        "id": len(reports) + 1,
        "station": station,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time_submitted": datetime.now().strftime("%H:%M:%S"),
        "merch_sales": data.get("merch_sales", 0),
        "gallons_sold": data.get("gallons_sold", 0),
        "gas_prices": {
            "regular": data.get("regular", 0),
            "plus": data.get("plus", 0),
            "super": data.get("super", 0),
            "diesel": data.get("diesel", 0)
        },
        "submitted_at": datetime.now().isoformat()
    }
    
    reports.append(new_report)
    
    with open(DAILY_REPORTS_FILE, 'w') as f:
        json.dump(reports, f, indent=2)
    
    return new_report["id"]

def save_request(station, data):
    """Save employee request - REMOVED TITLE FIELD"""
    requests = []
    if os.path.exists(REQUESTS_FILE):
        try:
            with open(REQUESTS_FILE, 'r') as f:
                requests = json.load(f)
        except:
            requests = []
    
    new_request = {
        "id": len(requests) + 1,
        "station": station,
        "employee_name": data.get("employee_name", ""),
        "request_type": data.get("request_type", ""),
        "priority": data.get("priority", "Normal"),
        "description": data.get("description", ""),
        "status": "Pending",
        "date_submitted": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "submitted_at": datetime.now().isoformat()
    }
    
    requests.append(new_request)
    
    with open(REQUESTS_FILE, 'w') as f:
        json.dump(requests, f, indent=2)
    
    return new_request["id"]

def display_product_result(product):
    """Display a search result"""
    age_badge = '<span class="age-restricted">🔞 AGE RESTRICTED</span>' if product['Age_Restricted'] == 'Yes' else ''
    
    st.markdown(f"""
    <div class="result-item">
        <div class="product-name">{product['Product_Name']}{age_badge}</div>
        <div class="product-info"><strong>UPC Code:</strong> {product['UPC_Code']}</div>
        <div class="product-info"><strong>Department:</strong> {product['Department_Name']} (Code: {product['Department_Code']})</div>
        <div class="product-info"><strong>Category:</strong> {product['Category']}</div>
        <div class="product-info"><strong>Price:</strong> <span class="product-price">{product['Display_Price']}</span></div>
        <div class="product-info"><strong>Stock Status:</strong> {product['Stock_Status']}</div>
        <div class="product-info"><strong>Tax Rate:</strong> {product['Tax_Rate']}%</div>
    </div>
    """, unsafe_allow_html=True)

def station_selection_page():
    """Station selection page - CLEAN VERSION"""
    
    # Custom CSS for this page only
    st.markdown("""
    <style>
        .main > div {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 2rem;
        }
        
        .stSelectbox > div > div {
            background: rgba(255, 255, 255, 0.15) !important;
            border: 2px solid rgba(255, 255, 255, 0.4) !important;
            border-radius: 15px !important;
            color: white !important;
            padding: 1.2rem !important;
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            backdrop-filter: blur(10px) !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Title
    st.markdown("""
    <div style="text-align: center; color: white; margin-bottom: 3rem;">
        <h1 style="font-size: 3rem; font-weight: 800; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
            Select Your Station
        </h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Center the form using columns
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Station selection
        selected_station = st.selectbox(
            "",
            [""] + GAS_STATIONS,
            key="station_select",
            label_visibility="collapsed"
        )
        
        if selected_station:
            if st.button("Continue to Dashboard", key="continue_btn", use_container_width=True):
                st.session_state.selected_station = selected_station
                st.session_state.current_page = "main_menu"
                st.rerun()
        else:
            st.info("Please select your gas station to continue")
    
    # Small company info at bottom
    st.markdown("""
    <div style="position: fixed; bottom: 2rem; left: 50%; transform: translateX(-50%); 
                text-align: center; color: rgba(255,255,255,0.7); font-size: 0.9rem; z-index: 1001;">
        🏪 Kirmani's Employee Portal
    </div>
    """, unsafe_allow_html=True)

def main_menu_page():
    """Main menu page - SIMPLIFIED SQUARE GRID LAYOUT"""
    station = st.session_state.get('selected_station', 'No Station')
    
    # Header
    st.markdown(f"""
    <div class="app-header">
        <div class="header-title">🏪 Kirmani's Gas Station</div>
        <p>Employee Dashboard</p>
        <div class="station-info">
            <div class="station-name">{station}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Status bar
    st.markdown("""
    <div class="status-bar">
        <div class="status-item">
            <div class="status-dot"></div>
            <span>Online</span>
        </div>
        <div class="status-item">
            <span>📅 Today</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Alert messages
    messages = load_messages()
    active_messages = [msg for msg in messages if not msg.get('dismissed', False)]
    
    for msg in active_messages[-2:]:  # Show last 2 messages
        msg_type = msg.get('type', 'info')
        if msg_type == 'urgent':
            st.markdown(f'<div class="alert alert-urgent">🚨 <strong>URGENT:</strong> {msg["message"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="alert">ℹ️ <strong>INFO:</strong> {msg["message"]}</div>', unsafe_allow_html=True)
    
    if not active_messages:
        st.markdown('<div class="alert">⚠️ <strong>Reminder:</strong> Submit daily report before shift ends</div>', unsafe_allow_html=True)
    
    # Add CSS for square buttons
    st.markdown("""
    <style>
        .element-container:has(.square-button) .stButton > button {
            background: white !important;
            color: #2c3e50 !important;
            border: 2px solid transparent !important;
            border-radius: 20px !important;
            padding: 2rem 1.5rem !important;
            font-size: 0.9rem !important;
            font-weight: 600 !important;
            min-height: 150px !important;
            box-shadow: 0 6px 25px rgba(0,0,0,0.1) !important;
            transition: all 0.3s ease !important;
            text-align: center !important;
            line-height: 1.4 !important;
            white-space: pre-line !important;
            width: 100% !important;
        }
        
        .element-container:has(.square-button) .stButton > button:hover {
            transform: translateY(-8px) !important;
            box-shadow: 0 15px 45px rgba(0,0,0,0.2) !important;
            border-color: #667eea !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # SIMPLE SQUARE GRID MENU LAYOUT
    col1, col2 = st.columns(2)
    
    with col1:
        # Daily Data Entry - LARGE SQUARE BUTTON
        st.markdown('<div class="square-button"></div>', unsafe_allow_html=True)
        if st.button("📊\n\nDaily Data Entry\n\nEnter sales, gallons, and gas prices", key="daily_entry_main", use_container_width=True):
            st.session_state.current_page = "daily_entry"
            st.rerun()
        
        # Submit Request - LARGE SQUARE BUTTON
        st.markdown('<div class="square-button"></div>', unsafe_allow_html=True)
        if st.button("📝\n\nSubmit Request\n\nRequest supplies or report issues", key="request_main", use_container_width=True):
            st.session_state.current_page = "submit_request"
            st.rerun()
    
    with col2:
        # Product Search - LARGE SQUARE BUTTON
        st.markdown('<div class="square-button"></div>', unsafe_allow_html=True)
        if st.button("🔍\n\nProduct Search\n\nScan barcodes and search products", key="search_main", use_container_width=True):
            st.session_state.current_page = "product_search"
            st.rerun()
        
        # Messages - LARGE SQUARE BUTTON
        st.markdown('<div class="square-button"></div>', unsafe_allow_html=True)
        if st.button("💬\n\nMessages\n\nView company announcements", key="messages_main", use_container_width=True):
            st.session_state.current_page = "messages"
            st.rerun()
    
    # Change station button - normal styling
    st.markdown("---")
    if st.button("🔄 Change Station", key="change_station"):
        st.session_state.current_page = "station_selection"
        st.rerun()

def daily_entry_page():
    """Daily data entry page"""
    st.markdown("## 📊 Daily Data Entry")
    
    if st.button("← Back to Menu", key="back_daily"):
        st.session_state.current_page = "main_menu"
        st.rerun()
    
    station = st.session_state.get('selected_station', 'Unknown')
    
    with st.form("daily_report_form"):
        st.markdown("### 📊 Merchandise Sales")
        merch_sales = st.number_input("Total Merchandise Sales ($)", min_value=0.0, step=0.01, format="%.2f")
        
        st.markdown("### ⛽ Fuel Data")
        gallons_sold = st.number_input("Total Gallons Sold", min_value=0, step=1)
        
        st.markdown("### 💵 Gas Prices")
        col1, col2 = st.columns(2)
        with col1:
            regular_price = st.number_input("Regular ($)", min_value=0.0, step=0.01, format="%.2f")
            super_price = st.number_input("Super ($)", min_value=0.0, step=0.01, format="%.2f")
        with col2:
            plus_price = st.number_input("Plus ($)", min_value=0.0, step=0.01, format="%.2f")
            diesel_price = st.number_input("Diesel ($)", min_value=0.0, step=0.01, format="%.2f")
        
        submitted = st.form_submit_button("📊 Submit Daily Report", use_container_width=True)
        
        if submitted:
            if merch_sales > 0 or gallons_sold > 0:
                report_data = {
                    "merch_sales": merch_sales,
                    "gallons_sold": gallons_sold,
                    "regular": regular_price,
                    "plus": plus_price,
                    "super": super_price,
                    "diesel": diesel_price
                }
                
                report_id = save_daily_report(station, report_data)
                
                st.markdown(f"""
                <div class="success-message">
                    ✅ Daily report submitted successfully!<br>
                    Report ID: #{report_id}<br>
                    Station: {station}
                </div>
                """, unsafe_allow_html=True)
                
                time.sleep(2)
                st.session_state.current_page = "main_menu"
                st.rerun()
            else:
                st.error("Please enter at least merchandise sales or gallons sold data")

def product_search_page():
    """Product search page - AUTO SEARCH WITH SINGLE BAR"""
    st.markdown("## 🔍 Product Search")
    
    if st.button("← Back to Menu", key="back_search"):
        st.session_state.current_page = "main_menu"
        st.rerun()
    
    # SINGLE SEARCH BAR - AUTO SEARCH
    search_term = st.text_input("🔍 Search products by name or UPC code...", key="search_input", placeholder="Start typing to search...")
    
    # AUTO SEARCH - triggers when user types
    if search_term and search_term.strip():
        df = load_product_data()
        if not df.empty:
            # Search logic
            search_clean = search_term.strip()
            
            upc_search_variants = [search_clean]
            if search_clean.isdigit():
                upc_search_variants.append(search_clean.lstrip('0'))
                if len(search_clean) < 12:
                    upc_search_variants.append(search_clean.zfill(12))
                if len(search_clean) < 14:
                    upc_search_variants.append(search_clean.zfill(14))
            
            search_mask = (
                df['Product_Name'].str.contains(search_clean, case=False, na=False) |
                df['Department_Name'].str.contains(search_clean, case=False, na=False) |
                df['Category'].str.contains(search_clean, case=False, na=False) |
                df['Search_Terms'].str.contains(search_clean, case=False, na=False)
            )
            
            for variant in upc_search_variants:
                search_mask = search_mask | (
                    df['UPC_Code'].str.contains(variant, case=False, na=False) |
                    df['UPC_Search'].str.contains(variant, case=False, na=False)
                )
            
            filtered_df = df[search_mask]
            
            if len(filtered_df) > 0:
                st.success(f"Found {len(filtered_df)} product(s) matching '{search_term}'")
                
                for _, product in filtered_df.head(10).iterrows():
                    display_product_result(product)
                
                if len(filtered_df) > 10:
                    st.info(f"Showing first 10 results. {len(filtered_df) - 10} more available.")
            else:
                st.warning(f"No products found matching '{search_term}'. Try different keywords.")
    elif search_term == "":
        st.info("Start typing in the search bar to find products...")
    else:
        st.info("Enter at least one character to start searching...")

def submit_request_page():
    """Submit request page - NO REQUEST TITLE"""
    st.markdown("## 📝 Submit Request")
    
    if st.button("← Back to Menu", key="back_request"):
        st.session_state.current_page = "main_menu"
        st.rerun()
    
    station = st.session_state.get('selected_station', 'Unknown')
    
    with st.form("request_form"):
        st.markdown("### 📝 Request Details")
        
        employee_name = st.text_input("👤 Your Name", placeholder="Enter your full name")
        
        col1, col2 = st.columns(2)
        with col1:
            request_type = st.selectbox("📋 Request Type", [
                "Business Checks", "Office Supplies", "Maintenance Issue", 
                "Equipment Repair", "Safety Concern", "Other"
            ])
        with col2:
            priority = st.selectbox("⚡ Priority", ["Normal", "Urgent", "Low"])
        
        # NO REQUEST TITLE FIELD
        description = st.text_area("📄 Description", placeholder="Detailed information...", height=100)
        
        submitted = st.form_submit_button("🚀 Submit Request", use_container_width=True)
        
        if submitted:
            if employee_name and description:  # Removed title requirement
                request_data = {
                    "employee_name": employee_name,
                    "request_type": request_type,
                    "priority": priority,
                    "description": description
                }
                
                request_id = save_request(station, request_data)
                
                st.markdown(f"""
                <div class="success-message">
                    ✅ Request submitted successfully!<br>
                    Request ID: #{request_id}<br>
                    Station: {station}<br>
                    Priority: {priority}
                </div>
                """, unsafe_allow_html=True)
                
                time.sleep(2)
                st.session_state.current_page = "main_menu"
                st.rerun()
            else:
                st.error("Please fill in all required fields")

def messages_page():
    """Messages page"""
    st.markdown("## 💬 Company Messages")
    
    if st.button("← Back to Menu", key="back_messages"):
        st.session_state.current_page = "main_menu"
        st.rerun()
    
    messages = load_messages()
    active_messages = [msg for msg in messages if not msg.get('dismissed', False)]
    
    if active_messages:
        for msg in reversed(active_messages[-10:]):  # Show last 10 messages
            msg_type = msg.get('type', 'info')
            sent_time = msg.get('sent_at', 'Unknown time')
            
            if msg_type == 'urgent':
                st.error(f"🚨 **URGENT:** {msg['message']}")
            elif msg_type == 'warning':
                st.warning(f"⚠️ **NOTICE:** {msg['message']}")
            elif msg_type == 'success':
                st.success(f"✅ **UPDATE:** {msg['message']}")
            else:
                st.info(f"ℹ️ **INFO:** {msg['message']}")
            
            st.caption(f"Sent: {sent_time}")
            st.markdown("---")
    else:
        st.markdown("""
        <div style="text-align: center; color: #6c757d; padding: 3rem;">
            📬 <strong>All messages up to date</strong><br><br>
            Check back regularly for company updates and announcements
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main application"""
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'station_selection'
    if 'selected_station' not in st.session_state:
        st.session_state.selected_station = None
    
    # Route to appropriate page
    if st.session_state.current_page == 'station_selection':
        station_selection_page()
    elif st.session_state.current_page == 'main_menu':
        main_menu_page()
    elif st.session_state.current_page == 'daily_entry':
        daily_entry_page()
    elif st.session_state.current_page == 'product_search':
        product_search_page()
    elif st.session_state.current_page == 'submit_request':
        submit_request_page()
    elif st.session_state.current_page == 'messages':
        messages_page()

if __name__ == "__main__":
    main()