import streamlit as st
import pandas as pd
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="PLU Product Catalog",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to match the inventory app design exactly
st.markdown("""
<style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container styling */
    .main > div {
        padding-top: 0rem;
        padding-left: 1rem;
        padding-right: 1rem;
        padding-bottom: 5rem; /* Space for bottom nav */
    }
    
    /* Header styling to match inventory app */
    .app-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
        margin-bottom: 1rem;
    }
    
    .app-title {
        font-size: 2rem;
        font-weight: 700;
        color: #000;
        margin: 0;
    }
    
    .add-button {
        background: #6366f1;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        border: none;
        font-size: 0.9rem;
        font-weight: 600;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Search bar styling */
    .search-container {
        background: #f3f4f6;
        border-radius: 12px;
        padding: 0.75rem 1rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .search-input {
        background: transparent;
        border: none;
        outline: none;
        font-size: 1rem;
        color: #9ca3af;
        width: 100%;
    }
    
    /* Category section styling */
    .category-section {
        margin-bottom: 2rem;
    }
    
    .category-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .category-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #000;
        margin: 0;
    }
    
    .see-all-link {
        color: #6366f1;
        font-size: 0.9rem;
        font-weight: 500;
        text-decoration: none;
        cursor: pointer;
    }
    
    /* Product cards grid */
    .products-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    @media (max-width: 768px) {
        .products-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    
    /* Product card styling */
    .product-card {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #e5e7eb;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .product-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .product-image {
        width: 100%;
        height: 80px;
        background: #1f2937;
        border-radius: 8px;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
    }
    
    .product-dots {
        position: absolute;
        top: 0.5rem;
        right: 0.5rem;
        color: #6b7280;
        font-size: 1rem;
    }
    
    .product-category-label {
        font-size: 0.7rem;
        color: #6366f1;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.25rem;
    }
    
    .product-name {
        font-size: 0.9rem;
        font-weight: 600;
        color: #000;
        line-height: 1.2;
        margin-bottom: 0.5rem;
        min-height: 2.4rem;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    
    .product-price {
        font-size: 0.8rem;
        color: #6b7280;
    }
    
    .product-stock {
        font-size: 0.8rem;
        color: #10b981;
        font-weight: 500;
    }
    
    /* Bottom navigation */
    .bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        border-top: 1px solid #e5e7eb;
        padding: 0.5rem 0;
        z-index: 1000;
    }
    
    .nav-items {
        display: flex;
        justify-content: space-around;
        align-items: center;
        max-width: 600px;
        margin: 0 auto;
    }
    
    .nav-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        cursor: pointer;
        padding: 0.5rem;
        text-decoration: none;
        color: #6b7280;
        transition: color 0.2s;
    }
    
    .nav-item.active {
        color: #6366f1;
    }
    
    .nav-item:hover {
        color: #6366f1;
    }
    
    .nav-icon {
        font-size: 1.2rem;
        margin-bottom: 0.25rem;
    }
    
    .nav-label {
        font-size: 0.7rem;
        font-weight: 500;
    }
    
    /* Category grid for Categories page */
    .category-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .category-card {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #e5e7eb;
        cursor: pointer;
        transition: all 0.2s;
        text-align: center;
    }
    
    .category-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .category-image {
        width: 100%;
        height: 100px;
        background: #1f2937;
        border-radius: 8px;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
    }
    
    .category-name {
        font-size: 1rem;
        font-weight: 600;
        color: #000;
        margin-bottom: 0.25rem;
    }
    
    .category-count {
        font-size: 0.8rem;
        color: #6b7280;
    }
    
    /* Age restriction badge */
    .age-restricted {
        background: #ef4444;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-left: 0.5rem;
    }
    
    /* Stats cards */
    .stats-row {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
    }
    
    .stat-number {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 0.25rem;
    }
    
    .stat-label {
        font-size: 0.8rem;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache the PLU data"""
    try:
        df = pd.read_csv('glide_products.csv')
        return df
    except FileNotFoundError:
        st.error("Please make sure 'glide_products.csv' is in the same directory as this script")
        return pd.DataFrame()

def render_product_card(product, show_category_label=True):
    """Render a product card matching the inventory app style"""
    age_badge = '<span class="age-restricted">🔞</span>' if product['Age_Restricted'] == 'Yes' else ''
    category_label = f'<div class="product-category-label">{product["Category"]}</div>' if show_category_label else ''
    
    return f"""
    <div class="product-card">
        <div class="product-image">
            <div class="product-dots">⋯</div>
            <div style="color: #9ca3af; font-size: 2rem;">📦</div>
        </div>
        {category_label}
        <div class="product-name">{product['Product_Name'][:50]}{'...' if len(product['Product_Name']) > 50 else ''}</div>
        <div class="product-price">{product['Display_Price']}{age_badge}</div>
    </div>
    """

def render_category_card(dept_name, count, icon="📦"):
    """Render a category card for the categories page"""
    return f"""
    <div class="category-card">
        <div class="category-image">
            <div class="product-dots">⋯</div>
            <div style="color: #9ca3af; font-size: 3rem;">{icon}</div>
        </div>
        <div class="category-name">{dept_name}</div>
        <div class="category-count">{count} products</div>
    </div>
    """

def render_bottom_nav(active_page):
    """Render bottom navigation - simplified for Streamlit"""
    nav_items = [
        ("Products", "📦", "products"),
        ("Orders", "🔄", "orders"),
        ("Warehouses", "📍", "warehouses"),
        ("Categories", "📂", "categories"),
        ("Users", "👥", "users")
    ]
    
    nav_html = '<div class="bottom-nav"><div class="nav-items">'
    
    for label, icon, page_key in nav_items:
        active_class = "active" if active_page == page_key else ""
        nav_html += f"""
        <div class="nav-item {active_class}">
            <div class="nav-icon">{icon}</div>
            <div class="nav-label">{label}</div>
        </div>
        """
    
    nav_html += '</div></div>'
    return nav_html

def products_page(df, search_term=""):
    """Main products page matching inventory app layout"""
    
    # Header with title and add button
    st.markdown("""
    <div class="app-header">
        <h1 class="app-title">Products</h1>
        <button class="add-button">+ Add Product</button>
    </div>
    """, unsafe_allow_html=True)
    
    # Search bar
    st.markdown("""
    <div class="search-container">
        <span style="color: #9ca3af;">🔍</span>
        <input class="search-input" placeholder="Search" />
        <span style="color: #9ca3af;">☰</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats row
    age_restricted_count = len(df[df['Age_Restricted'] == 'Yes'])
    dept_count = df['Department_Name'].nunique()
    
    st.markdown(f"""
    <div class="stats-row">
        <div class="stat-card">
            <div class="stat-number">{len(df):,}</div>
            <div class="stat-label">Total Products</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{age_restricted_count}</div>
            <div class="stat-label">Age Restricted</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{dept_count}</div>
            <div class="stat-label">Departments</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Filter data if search term provided
    filtered_df = df
    if search_term:
        mask = (
            df['Product_Name'].str.contains(search_term, case=False, na=False) |
            df['UPC_Code'].astype(str).str.contains(search_term, na=False)
        )
        filtered_df = df[mask]
    
    # Get top departments
    top_departments = filtered_df['Department_Name'].value_counts().head(6)
    
    # Department icons mapping
    dept_icons = {
        'Candy & Snacks': '🍭',
        'Health & Beauty': '💄',
        'Food & Grocery': '🥘',
        'Beverages & Drinks': '🥤',
        'Tobacco Accessories': '🚬',
        'Home & Kitchen': '🏠',
        'Baby & Kids': '👶',
        'Automotive': '🚗',
        'Electronics': '📱',
        'Convenience Items': '🛒'
    }
    
    # Render department sections
    for dept_name, count in top_departments.items():
        dept_products = filtered_df[filtered_df['Department_Name'] == dept_name].head(3)
        
        if len(dept_products) > 0:
            # Section header
            st.markdown(f"""
            <div class="category-section">
                <div class="category-header">
                    <h2 class="category-title">{dept_name}</h2>
                    <a class="see-all-link">See All ›</a>
                </div>
            """, unsafe_allow_html=True)
            
            # Products grid
            products_html = '<div class="products-grid">'
            for _, product in dept_products.iterrows():
                products_html += render_product_card(product, show_category_label=True)
            products_html += '</div></div>'
            
            st.markdown(products_html, unsafe_allow_html=True)

def categories_page(df):
    """Categories page showing department overview"""
    
    # Header
    st.markdown("""
    <div class="app-header">
        <h1 class="app-title">Categories</h1>
        <button class="add-button">+ Add Category</button>
    </div>
    """, unsafe_allow_html=True)
    
    # Search bar
    st.markdown("""
    <div class="search-container">
        <span style="color: #9ca3af;">🔍</span>
        <input class="search-input" placeholder="Search" />
    </div>
    """, unsafe_allow_html=True)
    
    # Get department counts
    dept_counts = df['Department_Name'].value_counts()
    
    # Department icons
    dept_icons = {
        'Candy & Snacks': '🍭',
        'Health & Beauty': '💄',
        'Food & Grocery': '🥘',
        'Beverages & Drinks': '🥤',
        'Tobacco Accessories': '🚬',
        'Home & Kitchen': '🏠',
        'Baby & Kids': '👶',
        'Automotive': '🚗',
        'Electronics': '📱',
        'Convenience Items': '🛒'
    }
    
    # Render category grid
    categories_html = '<div class="category-grid">'
    
    for dept_name, count in dept_counts.head(8).items():
        icon = dept_icons.get(dept_name, '📦')
        categories_html += render_category_card(dept_name, count, icon)
    
    categories_html += '</div>'
    st.markdown(categories_html, unsafe_allow_html=True)

def warehouses_page():
    """Warehouses/Stores page"""
    st.markdown("""
    <div class="app-header">
        <h1 class="app-title">Warehouses</h1>
        <button class="add-button">+ Add Warehouse</button>
    </div>
    """, unsafe_allow_html=True)
    
    # Search bar
    st.markdown("""
    <div class="search-container">
        <span style="color: #9ca3af;">🔍</span>
        <input class="search-input" placeholder="Search" />
    </div>
    """, unsafe_allow_html=True)
    
    # Sample warehouse locations
    warehouses = [
        {"name": "Main Distribution Center", "address": "1234 Commerce St, Dallas, TX 75201"},
        {"name": "North Regional Hub", "address": "5678 Industrial Pkwy, Chicago, IL 60601"},
        {"name": "West Coast Storage", "address": "9101 Logistics Blvd, Los Angeles, CA 90001"},
        {"name": "Southeast Warehouse", "address": "2468 Harbor Dr, Atlanta, GA 30301"}
    ]
    
    for warehouse in warehouses:
        st.markdown(f"""
        <div class="product-card" style="margin-bottom: 1rem;">
            <div class="product-name" style="margin-bottom: 0.5rem;">{warehouse['name']}</div>
            <div class="product-price" style="color: #6b7280;">{warehouse['address']}</div>
            <div style="text-align: right; margin-top: 0.5rem;">
                <span style="color: #6b7280;">⋯</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

def users_page():
    """Users management page"""
    st.markdown("""
    <div class="app-header">
        <h1 class="app-title">Users</h1>
        <button class="add-button">+ Add User</button>
    </div>
    """, unsafe_allow_html=True)
    
    # Search bar
    st.markdown("""
    <div class="search-container">
        <span style="color: #9ca3af;">🔍</span>
        <input class="search-input" placeholder="Search" />
    </div>
    """, unsafe_allow_html=True)
    
    # Sample users
    users = [
        {"name": "Store Manager", "role": "Manager", "email": "manager@store.com"},
        {"name": "Cashier 1", "role": "Cashier", "email": "cashier1@store.com"},
        {"name": "Inventory Clerk", "role": "Inventory", "email": "inventory@store.com"},
        {"name": "Assistant Manager", "role": "Assistant", "email": "assistant@store.com"}
    ]
    
    users_html = '<div class="products-grid">'
    for user in users:
        users_html += f"""
        <div class="product-card" style="text-align: center;">
            <div style="width: 60px; height: 60px; background: #6366f1; border-radius: 50%; margin: 0 auto 0.5rem; display: flex; align-items: center; justify-content: center; color: white; font-size: 1.5rem;">👤</div>
            <div class="product-name" style="margin-bottom: 0.25rem;">{user['name']}</div>
            <div class="product-price">{user['role']}</div>
            <div style="text-align: right; margin-top: 0.5rem;">
                <span style="color: #6b7280;">⋯</span>
            </div>
        </div>
        """
    users_html += '</div>'
    st.markdown(users_html, unsafe_allow_html=True)

def orders_page():
    """Orders management page"""
    st.markdown("""
    <div class="app-header">
        <h1 class="app-title">Orders</h1>
        <button class="add-button">+ Add Order</button>
    </div>
    """, unsafe_allow_html=True)
    
    # Search bar
    st.markdown("""
    <div class="search-container">
        <span style="color: #9ca3af;">🔍</span>
        <input class="search-input" placeholder="Search" />
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; padding: 3rem; color: #6b7280;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">📋</div>
        <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">No orders yet</div>
        <div>Orders will appear here when created</div>
    </div>
    """, unsafe_allow_html=True)

def main():
    # Load data
    df = load_data()
    
    if df.empty:
        st.stop()
    
    # Initialize session state for navigation
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'products'
    
    # Navigation buttons (styled to look like the original nav)
    st.markdown("""
    <style>
    .nav-buttons {
        display: flex;
        gap: 1rem;
        margin-bottom: 2rem;
        padding: 1rem;
        background: #1f2937;
        border-radius: 12px;
        justify-content: center;
        flex-wrap: wrap;
    }
    .nav-btn {
        background: #374151;
        color: white;
        border: 1px solid #4b5563;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        cursor: pointer;
        font-size: 0.9rem;
        min-width: 80px;
        text-align: center;
    }
    .nav-btn.active {
        background: #6366f1;
        border-color: #6366f1;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create navigation
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("📦 Products", key="nav_products", 
                    type="primary" if st.session_state.current_page == 'products' else "secondary"):
            st.session_state.current_page = 'products'
            st.rerun()
    
    with col2:
        if st.button("🔄 Orders", key="nav_orders",
                    type="primary" if st.session_state.current_page == 'orders' else "secondary"):
            st.session_state.current_page = 'orders'
            st.rerun()
    
    with col3:
        if st.button("📍 Warehouses", key="nav_warehouses",
                    type="primary" if st.session_state.current_page == 'warehouses' else "secondary"):
            st.session_state.current_page = 'warehouses'
            st.rerun()
    
    with col4:
        if st.button("📂 Categories", key="nav_categories",
                    type="primary" if st.session_state.current_page == 'categories' else "secondary"):
            st.session_state.current_page = 'categories'
            st.rerun()
    
    with col5:
        if st.button("👥 Users", key="nav_users",
                    type="primary" if st.session_state.current_page == 'users' else "secondary"):
            st.session_state.current_page = 'users'
            st.rerun()
    
    # Add some spacing
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Render the appropriate page
    if st.session_state.current_page == 'products':
        products_page(df)
    elif st.session_state.current_page == 'categories':
        categories_page(df)
    elif st.session_state.current_page == 'warehouses':
        warehouses_page()
    elif st.session_state.current_page == 'users':
        users_page()
    elif st.session_state.current_page == 'orders':
        orders_page()
    
    # Simple footer instead of complex bottom nav
    st.markdown("""
    <div style="position: fixed; bottom: 0; left: 0; right: 0; background: white; 
                border-top: 1px solid #e5e7eb; padding: 0.5rem; text-align: center; 
                font-size: 0.8rem; color: #6b7280; z-index: 1000;">
        PLU Product Catalog - Navigate using buttons above
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()