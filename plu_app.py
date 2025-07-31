import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import re

# Configure page
st.set_page_config(
    page_title="PLU Product Catalog",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for mobile-friendly UI
st.markdown("""
<style>
    /* Mobile-first responsive design */
    .main > div {
        padding-top: 1rem;
        padding-left: 0.5rem;
        padding-right: 0.5rem;
    }
    
    /* Mobile-optimized inputs */
    .stSelectbox > div > div {
        background-color: #f8f9fa;
        border-radius: 8px;
        min-height: 44px; /* Touch-friendly height */
    }
    
    .stTextInput > div > div > input {
        font-size: 16px; /* Prevents zoom on iOS */
        padding: 12px;
        border-radius: 8px;
    }
    
    .stSlider > div > div {
        padding: 10px 0;
    }
    
    /* Mobile-optimized product cards */
    .product-card {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border: 1px solid #e9ecef;
        margin-bottom: 1rem;
        transition: transform 0.2s;
        cursor: pointer;
        touch-action: manipulation;
    }
    
    .product-card:hover, .product-card:active {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .category-header {
        color: #6c5ce7;
        font-weight: 600;
        font-size: 1.1rem;
        margin: 1.5rem 0 0.8rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #6c5ce7;
        text-align: center;
    }
    
    .product-name {
        font-weight: 600;
        color: #2d3436;
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
        line-height: 1.3;
        word-wrap: break-word;
    }
    
    .product-price {
        color: #00b894;
        font-size: 1.3rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .product-department {
        color: #636e72;
        font-size: 0.85rem;
        margin-bottom: 0.3rem;
    }
    
    .product-upc {
        color: #74b9ff;
        font-size: 0.75rem;
        font-family: monospace;
        background: #f8f9fa;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        display: inline-block;
    }
    
    .age-restricted {
        background: #ff6b6b;
        color: white;
        padding: 0.3rem 0.6rem;
        border-radius: 6px;
        font-size: 0.7rem;
        font-weight: bold;
        display: inline-block;
        margin-top: 0.5rem;
    }
    
    .stock-status {
        background: #00b894;
        color: white;
        padding: 0.3rem 0.6rem;
        border-radius: 6px;
        font-size: 0.7rem;
        margin-left: 0.5rem;
        display: inline-block;
    }
    
    /* Mobile-optimized stats cards */
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin-bottom: 0.5rem;
    }
    
    .stats-number {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 0.3rem;
    }
    
    .stats-label {
        font-size: 0.8rem;
        opacity: 0.9;
    }
    
    .sidebar-header {
        background: #6c5ce7;
        color: white;
        padding: 0.8rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        text-align: center;
        font-weight: bold;
        font-size: 0.9rem;
    }
    
    /* Mobile navigation buttons */
    .nav-button {
        background: #6c5ce7;
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        border: none;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0.2rem;
        cursor: pointer;
        touch-action: manipulation;
        transition: all 0.2s;
    }
    
    .nav-button:hover, .nav-button:active {
        background: #5a4fcf;
        transform: scale(1.05);
    }
    
    .nav-button.active {
        background: #341f97;
    }
    
    /* Search bar mobile optimization */
    .search-container {
        background: white;
        border-radius: 25px;
        padding: 0.5rem 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border: 2px solid #e9ecef;
    }
    
    .search-container:focus-within {
        border-color: #6c5ce7;
        box-shadow: 0 2px 10px rgba(108, 92, 231, 0.2);
    }
    
    /* Quick filter buttons */
    .filter-chip {
        background: #f1f3f4;
        color: #5f6368;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        margin: 0.2rem;
        cursor: pointer;
        border: 1px solid #dadce0;
        display: inline-block;
        touch-action: manipulation;
    }
    
    .filter-chip.active {
        background: #6c5ce7;
        color: white;
        border-color: #6c5ce7;
    }
    
    /* Mobile table improvements */
    .dataframe {
        font-size: 0.8rem;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .stats-card {
            padding: 0.8rem;
        }
        
        .stats-number {
            font-size: 1.3rem;
        }
        
        .product-card {
            padding: 0.8rem;
        }
        
        .product-name {
            font-size: 0.9rem;
        }
        
        .product-price {
            font-size: 1.1rem;
        }
        
        .category-header {
            font-size: 1rem;
            margin: 1rem 0 0.5rem 0;
        }
    }
    
    /* Hide sidebar toggle on mobile for cleaner look */
    @media (max-width: 640px) {
        .css-1d391kg {
            padding: 1rem 0.5rem;
        }
    }
    
    /* Bottom sheet style for mobile filters */
    .mobile-filters {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        border-radius: 20px 20px 0 0;
        box-shadow: 0 -4px 20px rgba(0,0,0,0.15);
        padding: 1rem;
        z-index: 1000;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache the PLU data"""
    try:
        # Load the CSV file
        df = pd.read_csv('glide_products.csv')
        return df
    except FileNotFoundError:
        st.error("Please make sure 'glide_products.csv' is in the same directory as this script")
        return pd.DataFrame()

def display_product_card(product):
    """Display a product card with modern styling"""
    with st.container():
        st.markdown(f"""
        <div class="product-card">
            <div class="product-name">{product['Product_Name']}</div>
            <div class="product-department">📁 {product['Department_Name']}</div>
            <div class="product-price">{product['Display_Price']}</div>
            <div class="product-upc">UPC: {product['UPC_Code']}</div>
            <div style="margin-top: 0.5rem;">
                {'<span class="age-restricted">🔞 Age Restricted</span>' if product['Age_Restricted'] == 'Yes' else ''}
                <span class="stock-status">📦 {product['Stock_Status']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

def main():
    # Load data
    df = load_data()
    
    if df.empty:
        st.stop()
    
    # Mobile-friendly header
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 1rem;">
        <h1 style="color: #6c5ce7; margin-bottom: 0.5rem;">🛍️ PLU Product Catalog</h1>
        <p style="color: #636e72; font-size: 0.9rem;">Managing {len(df):,} products across {df['Department_Name'].nunique()} departments</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mobile stats row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">{len(df):,}</div>
            <div class="stats-label">Products</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        age_restricted_count = len(df[df['Age_Restricted'] == 'Yes'])
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">{age_restricted_count}</div>
            <div class="stats-label">Restricted</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        dept_count = df['Department_Name'].nunique()
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">{dept_count}</div>
            <div class="stats-label">Categories</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Mobile-optimized search and quick filters
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    search_term = st.text_input("🔍 Search Products", placeholder="Enter product name or UPC...", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick filter chips for mobile
    st.markdown("**Quick Filters:**")
    quick_filters = st.columns(4)
    with quick_filters[0]:
        show_tobacco = st.checkbox("🚬 Tobacco", key="tobacco_filter")
    with quick_filters[1]:
        show_candy = st.checkbox("🍭 Candy", key="candy_filter")
    with quick_filters[2]:
        show_drinks = st.checkbox("🥤 Drinks", key="drinks_filter")
    with quick_filters[3]:
        show_restricted = st.checkbox("🔞 Restricted", key="restricted_filter")
    
    # Mobile-optimized sidebar filters
    with st.sidebar:
        st.markdown('<div class="sidebar-header">🔍 Advanced Filters</div>', unsafe_allow_html=True)
        
        # Collapsible sections for mobile
        with st.expander("📂 Department & Category", expanded=False):
            # Department filter
            departments = ['All Departments'] + sorted(df['Department_Name'].unique().tolist())
            selected_department = st.selectbox("Department", departments)
            
            # Category filter
            categories = ['All Categories'] + sorted(df['Category'].unique().tolist())
            selected_category = st.selectbox("Category", categories)
        
        with st.expander("💰 Price & Stock", expanded=False):
            # Price range filter
            min_price, max_price = st.slider(
                "Price Range",
                min_value=float(df['Price_Numeric'].min()),
                max_value=float(df['Price_Numeric'].max()),
                value=(float(df['Price_Numeric'].min()), float(df['Price_Numeric'].max())),
                format="$%.2f"
            )
            
            # Stock status filter
            stock_filter = st.selectbox("Stock Status", ['All Status'] + df['Stock_Status'].unique().tolist())
        
        with st.expander("🔞 Age Restrictions", expanded=False):
            # Age restriction filter
            age_filter = st.selectbox("Age Restriction", ['All Products', 'Age Restricted Only', 'No Age Restriction'])
        
        st.markdown("---")
        
        # Mobile-friendly quick stats
        st.markdown("### 📊 Top Departments")
        dept_counts = df['Department_Name'].value_counts().head(3)
        for dept, count in dept_counts.items():
            st.markdown(f"**{dept[:20]}{'...' if len(dept) > 20 else ''}**: {count}")
    
    # Apply quick filters
    filtered_df = df.copy()
    
    if show_tobacco:
        filtered_df = filtered_df[filtered_df['Category'].str.contains('Tobacco', case=False, na=False)]
    if show_candy:
        filtered_df = filtered_df[filtered_df['Department_Name'].str.contains('Candy', case=False, na=False)]
    if show_drinks:
        filtered_df = filtered_df[filtered_df['Department_Name'].str.contains('Beverage|Drink', case=False, na=False)]
    if show_restricted:
        filtered_df = filtered_df[filtered_df['Age_Restricted'] == 'Yes']
    
    # Search filter
    if search_term:
        search_mask = (
            filtered_df['Product_Name'].str.contains(search_term, case=False, na=False) |
            filtered_df['UPC_Code'].astype(str).str.contains(search_term, na=False) |
            filtered_df['Search_Terms'].str.contains(search_term, case=False, na=False)
        )
        filtered_df = filtered_df[search_mask]
    
    # Department filter
    if selected_department != 'All Departments':
        filtered_df = filtered_df[filtered_df['Department_Name'] == selected_department]
    
    # Category filter
    if selected_category != 'All Categories':
        filtered_df = filtered_df[filtered_df['Category'] == selected_category]
    
    # Price filter
    filtered_df = filtered_df[
        (filtered_df['Price_Numeric'] >= min_price) & 
        (filtered_df['Price_Numeric'] <= max_price)
    ]
    
    # Age restriction filter
    if age_filter == 'Age Restricted Only':
        filtered_df = filtered_df[filtered_df['Age_Restricted'] == 'Yes']
    elif age_filter == 'No Age Restriction':
        filtered_df = filtered_df[filtered_df['Age_Restricted'] == 'No']
    
    # Stock status filter
    if stock_filter != 'All Status':
        filtered_df = filtered_df[filtered_df['Stock_Status'] == stock_filter]
    
    # Display results count with mobile-friendly layout
    st.markdown(f"### 📦 Products ({len(filtered_df):,} found)")
    
    # Mobile-optimized view and sort options
    col1, col2 = st.columns(2)
    with col1:
        # View options with mobile-friendly names
        view_mode = st.selectbox("View", ['🃏 Cards', '📋 List', '📂 Categories'], key="view_mode")
    with col2:
        # Sort options
        sort_options = {
            'Name A→Z': ['Product_Name', True],
            'Name Z→A': ['Product_Name', False],
            'Price ↑': ['Price_Numeric', True],
            'Price ↓': ['Price_Numeric', False],
            'Department': ['Department_Name', True]
        }
        sort_choice = st.selectbox("Sort", list(sort_options.keys()), key="sort_choice")
        sort_col, sort_asc = sort_options[sort_choice]
        filtered_df = filtered_df.sort_values(sort_col, ascending=sort_asc)
    
    # Display products based on view mode
    if len(filtered_df) == 0:
        st.warning("No products found matching your criteria. Try adjusting your filters.")
    else:
        if view_mode == '🃏 Cards':
            # Mobile-optimized card view - 2 columns on mobile, 3 on desktop
            cols = st.columns(2)  # Better for mobile
            
            display_limit = 20  # Reduced for mobile performance
            for idx, (_, product) in enumerate(filtered_df.head(display_limit).iterrows()):
                with cols[idx % len(cols)]:
                    display_product_card(product)
            
            if len(filtered_df) > display_limit:
                if st.button(f"📱 Load More ({len(filtered_df) - display_limit} remaining)", use_container_width=True):
                    st.rerun()
        
        elif view_mode == '📋 List':
            # Mobile-optimized table view
            display_cols = ['Product_Name', 'Display_Price', 'Department_Name', 'Age_Restricted']
            mobile_df = filtered_df[display_cols].head(50)
            mobile_df.columns = ['Product', 'Price', 'Department', 'Age Check']
            st.dataframe(
                mobile_df,
                use_container_width=True,
                hide_index=True,
                height=400
            )
        
        elif view_mode == '📂 Categories':
            # Mobile-optimized category view
            departments = filtered_df['Department_Name'].unique()
            for dept in sorted(departments):
                dept_products = filtered_df[filtered_df['Department_Name'] == dept]
                
                st.markdown(f'<div class="category-header">{dept} ({len(dept_products)})</div>', 
                           unsafe_allow_html=True)
                
                # Show fewer products per category on mobile
                cols = st.columns(2)  # Mobile-friendly 2 columns
                for idx, (_, product) in enumerate(dept_products.head(4).iterrows()):
                    with cols[idx % 2]:
                        display_product_card(product)
                
                if len(dept_products) > 4:
                    with st.expander(f"📱 Show all {len(dept_products)} in {dept}"):
                        remaining_cols = st.columns(2)
                        for idx, (_, product) in enumerate(dept_products.iloc[4:12].iterrows()):  # Limit for performance
                            with remaining_cols[idx % 2]:
                                display_product_card(product)
                        if len(dept_products) > 12:
                            st.info(f"💡 {len(dept_products) - 12} more products available. Use search to find specific items.")
    
    # Mobile-optimized analytics section
    if not filtered_df.empty and len(filtered_df) > 10:  # Only show analytics if enough data
        with st.expander("📈 Analytics Dashboard", expanded=False):
            
            # Single column layout for mobile
            # Department distribution - horizontal bar for mobile readability
            dept_counts = filtered_df['Department_Name'].value_counts().head(8)
            fig_dept = px.bar(
                x=dept_counts.values,
                y=[name[:20] + '...' if len(name) > 20 else name for name in dept_counts.index],
                orientation='h',
                title="Top Departments",
                labels={'x': 'Products', 'y': 'Department'},
                height=300
            )
            fig_dept.update_layout(
                font_size=10,
                title_font_size=14,
                margin=dict(l=10, r=10, t=30, b=10)
            )
            st.plotly_chart(fig_dept, use_container_width=True)
            
            # Price distribution - simplified
            fig_price = px.histogram(
                filtered_df,
                x='Price_Numeric',
                nbins=15,
                title="Price Distribution",
                labels={'Price_Numeric': 'Price ($)', 'count': 'Products'},
                height=250
            )
            fig_price.update_layout(
                font_size=10,
                title_font_size=14,
                margin=dict(l=10, r=10, t=30, b=10)
            )
            st.plotly_chart(fig_price, use_container_width=True)
            
            # Quick stats in mobile-friendly format
            col1, col2 = st.columns(2)
            with col1:
                avg_price = filtered_df['Price_Numeric'].mean()
                st.metric("Avg Price", f"${avg_price:.2f}")
            with col2:
                max_price = filtered_df['Price_Numeric'].max()
                st.metric("Max Price", f"${max_price:.2f}")
            
            # Age restriction pie chart - smaller for mobile
            if 'Age_Restricted' in filtered_df.columns:
                age_dist = filtered_df['Age_Restricted'].value_counts()
                if len(age_dist) > 1:
                    fig_age = px.pie(
                        values=age_dist.values,
                        names=age_dist.index,
                        title="Age Restrictions",
                        height=250
                    )
                    fig_age.update_layout(
                        font_size=10,
                        title_font_size=14,
                        margin=dict(l=10, r=10, t=30, b=10)
                    )
                    st.plotly_chart(fig_age, use_container_width=True)

if __name__ == "__main__":
    main()