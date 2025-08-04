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
    import os
    
    # Debug: Show current directory and files
    current_dir = os.getcwd()
    files_in_dir = os.listdir(current_dir)
    
    st.sidebar.write("🔍 **Debug Info:**")
    st.sidebar.write(f"Current directory: {current_dir}")
    st.sidebar.write("Files found:")
    for file in files_in_dir:
        st.sidebar.write(f"- {file}")
    
    try:
        # Try to read the CSV file with different encodings and options
        try:
            df = pd.read_csv('HLA_Prices.csv', dtype={
                'SU-UPC': str, 
                'Each-UPC': str, 
                'Case-UPC': str,
                'Item': str
            }, encoding='utf-8')
        except UnicodeDecodeError:
            # Try with different encoding
            df = pd.read_csv('HLA_Prices.csv', dtype={
                'SU-UPC': str, 
                'Each-UPC': str, 
                'Case-UPC': str,
                'Item': str
            }, encoding='latin-1')
        except:
            # Try without dtype specification
            df = pd.read_csv('HLA_Prices.csv')
        
        st.sidebar.success(f"✅ CSV loaded successfully! Rows: {len(df)}")
        st.sidebar.write("📋 **Columns found:**")
        for col in df.columns:
            st.sidebar.write(f"- '{col}'")
        
        # Show first few rows for debugging
        st.sidebar.write("📊 **Sample data:**")
        st.sidebar.dataframe(df.head(2))
        
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
        
    except FileNotFoundError as e:
        st.sidebar.error(f"❌ File not found: {e}")
        st.error("❌ **HLA_Prices.csv not found!** Please check:")
        st.error("1. File name is exactly 'HLA_Prices.csv' (case sensitive)")
        st.error("2. File is in the root directory of your repository")
        st.error("3. File was properly uploaded to GitHub")
        return pd.DataFrame()
    except Exception as e:
        st.sidebar.error(f"❌ Error loading file: {e}")
        st.error(f"Error loading CSV: {str(e)}")
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
    
    # Search options
    search_method = st.radio(
        "Choose search method:",
        ["🔍 Text Search", "📷 Barcode Scanner"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    search_term = ""
    
    if search_method == "🔍 Text Search":
        # Text search input
        search_term = st.text_input(
            "Search Products",
            placeholder="Enter product name, item number, UPC code, or any keyword...",
            label_visibility="collapsed"
        )
    
    elif search_method == "📷 Barcode Scanner":
        st.markdown("📱 **Take a photo of the barcode with your phone camera:**")
        
        # Camera input for barcode scanning
        camera_image = st.camera_input("Scan Barcode", label_visibility="collapsed")
        
        if camera_image is not None:
            try:
                # You'll need to install: pip install pyzbar pillow
                from pyzbar import pyzbar
                from PIL import Image
                import numpy as np
                
                # Convert the uploaded image to PIL format
                image = Image.open(camera_image)
                
                # Decode barcodes from the image
                barcodes = pyzbar.decode(image)
                
                if barcodes:
                    # Get the first barcode found
                    barcode_data = barcodes[0].data.decode('utf-8')
                    search_term = barcode_data
                    st.success(f"✅ Barcode detected: {barcode_data}")
                    
                    # Show the image with detected barcode highlighted
                    st.image(image, caption=f"Detected barcode: {barcode_data}", width=300)
                    
                else:
                    st.error("❌ No barcode detected in the image. Please try again with a clearer photo.")
                    
            except ImportError:
                st.error("📦 Barcode scanning requires additional packages. Please install: `pip install pyzbar pillow`")
            except Exception as e:
                st.error(f"❌ Error processing image: {str(e)}")
        
        # Also provide manual UPC input as backup
        st.markdown("**Or enter UPC manually:**")
        manual_upc = st.text_input(
            "Manual UPC Entry",
            placeholder="Enter UPC code manually...",
            label_visibility="collapsed"
        )
        if manual_upc:
            search_term = manual_upc
    
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