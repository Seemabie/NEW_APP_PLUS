import streamlit as st
import pandas as pd

# Configure page
st.set_page_config(
    page_title="Kirmani's Product Search",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Simple CSS for clean design
st.markdown("""
<style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Main container styling */
    .main > div {
        padding-top: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Logo styling */
    .logo {
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Search container */
    .search-container {
        max-width: 600px;
        margin: 0 auto 3rem auto;
    }
    
    /* Results styling */
    .result-item {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
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
    
    .no-results {
        text-align: center;
        color: #7f8c8d;
        font-size: 1.1rem;
        margin-top: 3rem;
    }
    
    .results-count {
        text-align: center;
        color: #7f8c8d;
        font-size: 0.9rem;
        margin-bottom: 2rem;
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

def display_result(product):
    """Display a search result in plain text format"""
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

def main():
    # Load data
    df = load_data()
    
    if df.empty:
        st.stop()
    
    # Logo
    st.markdown('<div class="logo">🔍 Kirmani\'s Product Search App</div>', unsafe_allow_html=True)
    
    # Search container
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    # Search input
    search_term = st.text_input(
        "Search Products",
        placeholder="Enter product name, UPC code, or any keyword...",
        label_visibility="collapsed"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Search and display results
    if search_term:
        # Filter data based on search term
        search_mask = (
            df['Product_Name'].str.contains(search_term, case=False, na=False) |
            df['UPC_Code'].astype(str).str.contains(search_term, na=False) |
            df['Department_Name'].str.contains(search_term, case=False, na=False) |
            df['Category'].str.contains(search_term, case=False, na=False) |
            df['Search_Terms'].str.contains(search_term, case=False, na=False)
        )
        
        filtered_df = df[search_mask]
        
        if len(filtered_df) > 0:
            # Show results count
            st.markdown(f'<div class="results-count">Found {len(filtered_df)} product(s) matching "{search_term}"</div>', unsafe_allow_html=True)
            
            # Display results
            for _, product in filtered_df.head(50).iterrows():  # Limit to 50 results for performance
                display_result(product)
            
            # Show if there are more results
            if len(filtered_df) > 50:
                st.markdown(f'<div class="results-count">Showing first 50 results. {len(filtered_df) - 50} more available.</div>', unsafe_allow_html=True)
        
        else:
            # No results found
            st.markdown(f'<div class="no-results">No products found matching "{search_term}"<br>Try searching with different keywords</div>', unsafe_allow_html=True)
    
    else:
        # Welcome message when no search term
        st.markdown("""
        <div class="no-results">
            👋 Welcome to Kirmani's Product Search!<br><br>
            🔍 Search through 5,123 products<br>
            📱 Search by product name, UPC code, or category<br>
            💡 Just type in the search box above to get started
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()