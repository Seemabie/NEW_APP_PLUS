import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, date, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configure page
st.set_page_config(
    page_title="Kirmani's Admin Portal",
    page_icon="👨‍💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# File paths for data storage (same as employee app)
DAILY_REPORTS_FILE = 'daily_reports.json'
REQUESTS_FILE = 'employee_requests.json'
MESSAGES_FILE = 'admin_messages.json'

# Gas Station options (same as employee app)
GAS_STATIONS = [
    "🚗 KSK Auto Group",
    "⛽ ONE STOP INC", 
    "🏢 SYED Empires",
    "🌟 S. Micheal",
    "🏪 Verbank",
    "🛣️ Main Street Station",
    "🏎️ Highway 95 Station", 
    "🏙️ Downtown Station",
    "✈️ Airport Road Station",
    "🛍️ Mall Plaza Station",
    "🏭 Industrial Station",
    "🌊 Westside Station",
    "🌅 Eastside Station",
    "🏔️ Mountain View Station",
    "🌳 Greenwood Station",
    "🏘️ Residential Station",
    "🚌 Transit Hub Station",
    "🏥 Medical Center Station",
    "🎓 University Station",
    "🏖️ Beachfront Station",
    "🎪 Fairground Station",
    "🏟️ Stadium Station",
    "🛒 Shopping Center Station",
    "🏛️ Government Station",
    "🌆 Skyline Station",
    "🌉 Bridge Station",
    "🏞️ Parkway Station",
    "🚢 Harbor Station",
    "🎭 Entertainment Station",
    "🏕️ Campground Station"
]

# Custom CSS for admin portal styling
st.markdown("""
<style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Main container */
    .main > div {
        padding: 0;
        max-width: 100%;
    }
    
    /* Header styling */
    .admin-header {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        color: white;
        padding: 1.5rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .header-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .header-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
    }
    
    .header-info {
        display: flex;
        gap: 2rem;
        align-items: center;
        font-size: 0.9rem;
    }
    
    /* Stats cards */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin-bottom: 3rem;
    }
    
    .stat-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #e9ecef;
        position: relative;
        overflow: hidden;
        transition: transform 0.2s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .stat-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .stat-icon {
        font-size: 2.5rem;
        opacity: 0.8;
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        color: #6c757d;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    .stat-trend {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-top: 1rem;
        font-size: 0.85rem;
    }
    
    .trend-up {
        color: #28a745;
    }
    
    .trend-down {
        color: #dc3545;
    }
    
    /* Section styling */
    .content-section {
        background: white;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #e9ecef;
        margin-bottom: 2rem;
        overflow: hidden;
    }
    
    .section-header {
        padding: 1.5rem 2rem;
        border-bottom: 1px solid #e9ecef;
        background: #f8f9fa;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .section-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #2c3e50;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Status badges */
    .status-badge {
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin: 0.2rem;
    }
    
    .status-pending {
        background: #fff3cd;
        color: #856404;
    }
    
    .status-completed {
        background: #d4edda;
        color: #155724;
    }
    
    .status-urgent {
        background: #f8d7da;
        color: #721c24;
    }
    
    /* Success message */
    .success-message {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: center;
        font-weight: 600;
    }
    
    /* Warning message */
    .warning-message {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: center;
        font-weight: 600;
    }
    
    /* Chart containers */
    .chart-container {
        padding: 1.5rem;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .header-content {
            flex-direction: column;
            gap: 1rem;
            text-align: center;
        }
        
        .stats-container {
            grid-template-columns: 1fr;
        }
    }
</style>
""", unsafe_allow_html=True)

def load_daily_reports():
    """Load daily reports data"""
    if os.path.exists(DAILY_REPORTS_FILE):
        try:
            with open(DAILY_REPORTS_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def load_requests():
    """Load employee requests data"""
    if os.path.exists(REQUESTS_FILE):
        try:
            with open(REQUESTS_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def load_messages():
    """Load admin messages"""
    if os.path.exists(MESSAGES_FILE):
        try:
            with open(MESSAGES_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_message(message_data):
    """Save new admin message"""
    messages = load_messages()
    
    new_message = {
        "id": len(messages) + 1,
        "message": message_data["message"],
        "type": message_data["type"],
        "expiry": message_data["expiry"],
        "sent_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "dismissed": False
    }
    
    messages.append(new_message)
    
    with open(MESSAGES_FILE, 'w') as f:
        json.dump(messages, f, indent=2)
    
    return new_message["id"]

def update_request_status(request_id, status="Completed"):
    """Update request status"""
    requests = load_requests()
    
    for request in requests:
        if request["id"] == request_id:
            request["status"] = status
            request["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            break
    
    with open(REQUESTS_FILE, 'w') as f:
        json.dump(requests, f, indent=2)

def calculate_stats():
    """Calculate dashboard statistics"""
    reports = load_daily_reports()
    requests = load_requests()
    
    # Today's reports
    today = datetime.now().strftime("%Y-%m-%d")
    today_reports = [r for r in reports if r.get('date') == today]
    
    # Total sales today
    total_sales = sum(float(r.get('merch_sales', 0)) for r in today_reports)
    
    # Total gallons today
    total_gallons = sum(int(r.get('gallons_sold', 0)) for r in today_reports)
    
    # Pending requests
    pending_requests = len([r for r in requests if r.get('status') == 'Pending'])
    
    # Active stations (stations that reported today)
    active_stations = len(set(r.get('station') for r in today_reports))
    
    return {
        "active_stations": active_stations,
        "total_sales": total_sales,
        "total_gallons": total_gallons,
        "pending_requests": pending_requests,
        "reports_today": len(today_reports)
    }

def render_admin_header():
    """Render admin portal header"""
    current_date = datetime.now().strftime("%B %d, %Y")
    
    st.markdown(f"""
    <div class="admin-header">
        <div class="header-content">
            <h1 class="header-title">👨‍💼 Kirmani's Admin Portal</h1>
            <div class="header-info">
                <span>📅 {current_date}</span>
                <span>⚙️ Settings</span>
                <span>👤 Admin</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_stats_overview():
    """Render statistics overview cards"""
    stats = calculate_stats()
    
    st.markdown('<div class="stats-container">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-header">
                <div class="stat-icon">🏪</div>
            </div>
            <div class="stat-value">{len(GAS_STATIONS)}</div>
            <div class="stat-label">Total Gas Stations</div>
            <div class="stat-trend trend-up">
                ↗️ {stats['active_stations']} reported today
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-header">
                <div class="stat-icon">📊</div>
            </div>
            <div class="stat-value">${stats['total_sales']:,.0f}</div>
            <div class="stat-label">Today's Total Sales</div>
            <div class="stat-trend trend-up">
                ↗️ {stats['reports_today']} reports submitted
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-header">
                <div class="stat-icon">⛽</div>
            </div>
            <div class="stat-value">{stats['total_gallons']:,}</div>
            <div class="stat-label">Gallons Sold Today</div>
            <div class="stat-trend trend-up">
                ↗️ Across {stats['active_stations']} stations
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-header">
                <div class="stat-icon">📝</div>
            </div>
            <div class="stat-value">{stats['pending_requests']}</div>
            <div class="stat-label">Pending Requests</div>
            <div class="stat-trend {'trend-up' if stats['pending_requests'] > 0 else 'trend-down'}">
                {'⚠️ Needs attention' if stats['pending_requests'] > 0 else '✅ All handled'}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_broadcast_message():
    """Render broadcast message section"""
    st.markdown("""
    <div class="content-section">
        <div class="section-header">
            <div class="section-title">📢 Broadcast Message to All Stations</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### Message Content")
            message_content = st.text_area(
                "Type your message to all gas station employees...",
                height=120,
                placeholder="Example: New safety protocols effective immediately...",
                label_visibility="collapsed"
            )
        
        with col2:
            st.markdown("### Message Settings")
            message_type = st.selectbox(
                "Message Type",
                ["📋 Information", "⚠️ Warning", "🚨 Urgent", "✅ Update"],
                key="msg_type"
            )
            
            message_expiry = st.selectbox(
                "Expires After",
                ["Never", "1 hour", "4 hours", "24 hours", "1 week"],
                key="msg_expiry"
            )
            
            if st.button("📤 Send to All Stations", use_container_width=True, type="primary"):
                if message_content.strip():
                    # Extract type from selection
                    type_map = {
                        "📋 Information": "info",
                        "⚠️ Warning": "warning", 
                        "🚨 Urgent": "urgent",
                        "✅ Update": "success"
                    }
                    
                    message_data = {
                        "message": message_content,
                        "type": type_map[message_type],
                        "expiry": message_expiry
                    }
                    
                    message_id = save_message(message_data)
                    
                    st.markdown(f"""
                    <div class="success-message">
                        ✅ Message sent successfully to all {len(GAS_STATIONS)} gas stations!<br>
                        Message ID: #{message_id}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.rerun()
                else:
                    st.error("Please enter a message before sending.")

def render_daily_reports():
    """Render daily reports section"""
    st.markdown("""
    <div class="content-section">
        <div class="section-header">
            <div class="section-title">📊 Today's Station Reports</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    reports = load_daily_reports()
    today = datetime.now().strftime("%Y-%m-%d")
    today_reports = [r for r in reports if r.get('date') == today]
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        station_filter = st.selectbox(
            "Filter by Station",
            ["All Stations"] + GAS_STATIONS,
            key="station_filter"
        )
    
    with col2:
        date_filter = st.date_input(
            "Date",
            value=date.today(),
            key="date_filter"
        )
    
    with col3:
        sort_filter = st.selectbox(
            "Sort by",
            ["Sales (High to Low)", "Sales (Low to High)", "Gallons Sold", "Station Name", "Time Submitted"],
            key="sort_filter"
        )
    
    with col4:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
    
    # Filter and sort data
    filtered_reports = today_reports.copy()
    
    if station_filter != "All Stations":
        filtered_reports = [r for r in filtered_reports if r.get('station') == station_filter]
    
    # Sort data
    if sort_filter == "Sales (High to Low)":
        filtered_reports.sort(key=lambda x: float(x.get('merch_sales', 0)), reverse=True)
    elif sort_filter == "Sales (Low to High)":
        filtered_reports.sort(key=lambda x: float(x.get('merch_sales', 0)))
    elif sort_filter == "Gallons Sold":
        filtered_reports.sort(key=lambda x: int(x.get('gallons_sold', 0)), reverse=True)
    elif sort_filter == "Station Name":
        filtered_reports.sort(key=lambda x: x.get('station', ''))
    elif sort_filter == "Time Submitted":
        filtered_reports.sort(key=lambda x: x.get('time_submitted', ''), reverse=True)
    
    # Display reports table
    if filtered_reports:
        # Create DataFrame for better display
        df_data = []
        for report in filtered_reports:
            gas_prices = report.get('gas_prices', {})
            df_data.append({
                'Station': report.get('station', 'Unknown').replace('🚗 ', '').replace('⛽ ', '').replace('🏢 ', '').replace('🌟 ', '').replace('🏪 ', ''),
                'Merch Sales': f"${float(report.get('merch_sales', 0)):,.2f}",
                'Gallons Sold': f"{int(report.get('gallons_sold', 0)):,} gal",
                'Gas Prices (R/P/S/D)': f"${gas_prices.get('regular', 0):.2f} / ${gas_prices.get('plus', 0):.2f} / ${gas_prices.get('super', 0):.2f} / ${gas_prices.get('diesel', 0):.2f}",
                'Submitted At': report.get('time_submitted', 'Unknown'),
                'Status': '✅ Complete'
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Export button
        if st.button("📥 Export Data to CSV"):
            csv = df.to_csv(index=False)
            st.download_button(
                label="📄 Download CSV File",
                data=csv,
                file_name=f"daily_reports_{date_filter.strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    else:
        st.warning("No reports found for the selected criteria.")
        
    # Show missing stations
    submitted_stations = [r.get('station') for r in filtered_reports]
    missing_stations = [station for station in GAS_STATIONS if station not in submitted_stations]
    
    if missing_stations:
        st.markdown("### ⏳ Stations Not Yet Reported:")
        for station in missing_stations[:10]:  # Show first 10
            st.markdown(f"- {station}")
        if len(missing_stations) > 10:
            st.markdown(f"... and {len(missing_stations) - 10} more stations")

def render_request_management():
    """Render employee request management section"""
    st.markdown("""
    <div class="content-section">
        <div class="section-header">
            <div class="section-title">📝 Employee Requests Management</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    requests = load_requests()
    
    if requests:
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status_filter = st.selectbox(
                "Filter by Status",
                ["All", "Pending", "Completed"],
                key="request_status_filter"
            )
        
        with col2:
            priority_filter = st.selectbox(
                "Filter by Priority",
                ["All", "Urgent", "Normal", "Low"],
                key="request_priority_filter"
            )
        
        with col3:
            station_request_filter = st.selectbox(
                "Filter by Station",
                ["All Stations"] + GAS_STATIONS,
                key="request_station_filter"
            )
        
        # Filter requests
        filtered_requests = requests.copy()
        
        if status_filter != "All":
            filtered_requests = [r for r in filtered_requests if r.get('status') == status_filter]
        
        if priority_filter != "All":
            filtered_requests = [r for r in filtered_requests if r.get('priority') == priority_filter]
        
        if station_request_filter != "All Stations":
            filtered_requests = [r for r in filtered_requests if r.get('station') == station_request_filter]
        
        # Sort by date (newest first)
        filtered_requests.sort(key=lambda x: x.get('date_submitted', ''), reverse=True)
        
        # Display requests
        for request in filtered_requests[:20]:  # Show first 20 requests
            with st.container():
                col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
                
                with col1:
                    st.write(f"**#{request.get('id')}**")
                    priority = request.get('priority', 'Normal')
                    if priority == 'Urgent':
                        st.markdown('<span class="status-badge status-urgent">🚨 Urgent</span>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<span class="status-badge status-pending">⏳ {priority}</span>', unsafe_allow_html=True)
                
                with col2:
                    st.write(f"**{request.get('employee_name', 'Unknown')}**")
                    st.write(f"{request.get('station', 'Unknown Station')}")
                    st.write(f"Type: {request.get('request_type', 'Unknown')}")
                
                with col3:
                    st.write(f"**{request.get('title', 'No title')}**")
                    st.write(request.get('description', 'No description')[:100] + "..." if len(request.get('description', '')) > 100 else request.get('description', ''))
                    st.write(f"📅 {request.get('date_submitted', 'Unknown date')}")
                
                with col4:
                    if request.get('status') == 'Pending':
                        if st.button(f"✅ Complete", key=f"complete_{request.get('id')}", type="primary"):
                            update_request_status(request.get('id'))
                            st.success(f"Request #{request.get('id')} marked as completed!")
                            st.rerun()
                    else:
                        st.markdown('<span class="status-badge status-completed">✅ Completed</span>', unsafe_allow_html=True)
                
                st.divider()
        
        if len(filtered_requests) > 20:
            st.info(f"Showing first 20 of {len(filtered_requests)} requests. Use filters to narrow down.")
    else:
        st.info("No employee requests found.")

def render_analytics():
    """Render analytics charts"""
    st.markdown("## 📈 Analytics Dashboard")
    
    reports = load_daily_reports()
    
    if reports:
        # Create DataFrame from reports
        df_reports = pd.DataFrame(reports)
        df_reports['date'] = pd.to_datetime(df_reports['date'])
        df_reports['merch_sales'] = pd.to_numeric(df_reports['merch_sales'], errors='coerce')
        df_reports['gallons_sold'] = pd.to_numeric(df_reports['gallons_sold'], errors='coerce')
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Daily sales trend
            daily_sales = df_reports.groupby('date')['merch_sales'].sum().reset_index()
            fig_sales = px.line(
                daily_sales,
                x='date',
                y='merch_sales',
                title='📈 Daily Sales Trend',
                labels={'merch_sales': 'Sales ($)', 'date': 'Date'}
            )
            fig_sales.update_layout(height=400)
            st.plotly_chart(fig_sales, use_container_width=True)
        
        with col2:
            # Sales by station
            station_sales = df_reports.groupby('station')['merch_sales'].sum().reset_index()
            station_sales = station_sales.sort_values('merch_sales', ascending=True).tail(10)
            
            fig_stations = px.bar(
                station_sales,
                x='merch_sales',
                y='station',
                orientation='h',
                title='⛽ Top 10 Stations by Sales',
                labels={'merch_sales': 'Sales ($)', 'station': 'Station'}
            )
            fig_stations.update_layout(height=400)
            st.plotly_chart(fig_stations, use_container_width=True)
        
        # Fuel sales analysis
        col3, col4 = st.columns(2)
        
        with col3:
            # Gallons sold trend
            daily_gallons = df_reports.groupby('date')['gallons_sold'].sum().reset_index()
            fig_gallons = px.area(
                daily_gallons,
                x='date',
                y='gallons_sold',
                title='⛽ Daily Gallons Sold',
                labels={'gallons_sold': 'Gallons', 'date': 'Date'}
            )
            fig_gallons.update_layout(height=400)
            st.plotly_chart(fig_gallons, use_container_width=True)
        
        with col4:
            # Request priority distribution
            requests = load_requests()
            if requests:
                request_df = pd.DataFrame(requests)
                priority_counts = request_df['priority'].value_counts()
                
                fig_requests = px.pie(
                    values=priority_counts.values,
                    names=priority_counts.index,
                    title='📝 Request Priority Distribution'
                )
                fig_requests.update_layout(height=400)
                st.plotly_chart(fig_requests, use_container_width=True)
            else:
                st.info("No request data available for chart")
    else:
        st.warning("No data available for analytics. Daily reports are needed to generate charts.")

def main():
    """Main admin portal application"""
    
    # Render header
    render_admin_header()
    
    # Main content container
    with st.container():
        # Stats overview
        render_stats_overview()
        
        # Broadcast message section
        render_broadcast_message()
        
        # Daily reports section
        render_daily_reports()
        
        # Request management section
        render_request_management()
        
        # Analytics section
        render_analytics()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d; padding: 2rem;">
        👨‍💼 <strong>Kirmani's Admin Portal</strong> - Gas Station Management System<br>
        <small>Real-time monitoring and management of all gas station operations</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()