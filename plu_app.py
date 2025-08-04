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
    """Load and cache the product data"""
    try:
        # Read CSV with UPC codes as strings to preserve formatting
        df = pd.read_csv('HLA_Prices.csv', dtype={
            'SU-UPC': str, 
            'Each-UPC': str, 
            'Case-UPC': str,
            'Item': str
        })
        
        # Ensure UPC codes are properly formatted as strings and handle NaN values
        for upc_col in ['SU-UPC', 'Each-UPC', 'Case-UPC']:
            if upc_col in df.columns:
                df[upc_col] = df[upc_col].fillna('').astype(str)
        
        # Create search-friendly columns for flexible UPC search
        for upc_col in ['SU-UPC', 'Each-UPC', 'Case-UPC']:
            if upc_col in df.columns:
                search_col = f'{upc_col}_Search'
                df[search_col] = df[upc_col].str.replace(r'^0+', '', regex=True)
        
        return df
    except FileNotFoundError:
        st.error("Please make sure 'HLA_Prices.csv' is in the same directory as this script")
        return pd.DataFrame()

def display_result(product):
    """Display a search result"""
    # Use Item Description as the main product name
    product_name = str(product.get('Item Description', 'N/A'))
    
    st.markdown(f"""
    <div class="result-item">
        <div class="product-name">{product_name}</div>
        <div class="product-info"><strong>Item:</strong> {str(product.get('Item', 'N/A'))}</div>
        <div class="product-info"><strong>Site Number:</strong> {str(product.get('Site Number', 'N/A'))}</div>
        <div class="product-info"><strong>Category:</strong> {str(product.get('Category', 'N/A'))}</div>
        <div class="product-info"><strong>SU-UPC:</strong> {str(product.get('SU-UPC', 'N/A'))}</div>
        <div class="product-info"><strong>Each-UPC:</strong> {str(product.get('Each-UPC', 'N/A'))}</div>
        <div class="product-info"><strong>Case-UPC:</strong> {str(product.get('Case-UPC', 'N/A'))}</div>
        <div class="product-info"><strong>Pack(SU):</strong> {str(product.get('Pack(SU)', 'N/A'))}</div>
        <div class="product-info"><strong>Retail:</strong> <span class="product-price">{str(product.get('Retail', 'N/A'))}</span></div>
        <div class="product-info"><strong>Each Cost:</strong> <span class="product-price">{str(product.get('Each Cost', 'N/A'))}</span></div>
        <div class="product-info"><strong>Total Cost(SU)/Tax:</strong> {str(product.get('Total Cost(SU)/Tax', 'N/A'))}</div>
        <div class="product-info"><strong>Total Cost(SU) W/O Tax:</strong> {str(product.get('Total Cost(SU) W/O Tax', 'N/A'))}</div>
        <div class="product-info"><strong>Eligible for Credit:</strong> {str(product.get('Eligible for Credit', 'N/A'))}</div>
        <div class="product-info"><strong>Item Status:</strong> {str(product.get('Item Status', 'N/A'))}</div>
        <div class="product-info"><strong>As of Date:</strong> {str(product.get('As of Date', 'N/A'))}</div>
    </div>
    """, unsafe_allow_html=True)

def main():
    # Load data
    df = load_data()
    
    if df.empty:
        st.stop()
    
    # Image and Logo
    # Display the image
    try:
        st.image("image.jpeg", width=200, use_column_width=False)
    except FileNotFoundError:
        st.warning("Image file 'image.jpeg' not found. Please make sure it's in the same directory as your script.")
    
    # Logo
    st.markdown('<div class="logo">🔍 Kirmani\'s Product Search App</div>', unsafe_allow_html=True)
    
    # Search container
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    # Search input
    search_term = st.text_input(
        "Search Products",
        placeholder="Enter product name, item number, UPC code, or any keyword...",
        label_visibility="collapsed"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Search and display results
    if search_term:
        # Clean the search term
        search_clean = search_term.strip()
        
        # Create search mask for different fields
        search_mask = pd.Series([False] * len(df))
        
        # Search in text fields
        text_columns = ['Item Description', 'Category', 'Item']
        for col in text_columns:
            if col in df.columns:
                search_mask = search_mask | df[col].astype(str).str.contains(search_clean, case=False, na=False)
        
        # Search in UPC fields (original and search-friendly versions)
        upc_columns = ['SU-UPC', 'Each-UPC', 'Case-UPC']
        for col in upc_columns:
            if col in df.columns:
                # Search original UPC
                search_mask = search_mask | df[col].astype(str).str.contains(search_clean, case=False, na=False)
                # Search cleaned UPC (without leading zeros)
                search_col = f'{col}_Search'
                if search_col in df.columns:
                    search_mask = search_mask | df[search_col].astype(str).str.contains(search_clean, case=False, na=False)
        
        # For numeric searches, also try variations with leading zeros
        if search_clean.isdigit():
            # Add versions with different zero padding
            upc_variants = [
                search_clean.zfill(12),  # 12-digit UPC
                search_clean.zfill(14),  # 14-digit UPC
                search_clean.lstrip('0')  # Remove leading zeros
            ]
            
            for variant in upc_variants:
                for col in upc_columns:
                    if col in df.columns:
                        search_mask = search_mask | df[col].astype(str).str.contains(variant, case=False, na=False)
        
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
        total_products = len(df) if not df.empty else 0
        st.markdown(f"""
        <div class="no-results">
            👋 Welcome to Kirmani's Product Search!<br><br>
            🔍 Search through {total_products:,} products<br>
            📱 Search by product name, item number, UPC code, or category<br>
            💡 Just type in the search box above to get started
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()