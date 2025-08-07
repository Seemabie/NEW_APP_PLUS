import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Page configuration for mobile
st.set_page_config(
    page_title="Kirmani's Store Reviews",
    page_icon="🏪",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Load custom CSS and HTML
def load_custom_css():
    return """
    <style>
        /* Hide Streamlit default elements */
        .stApp > header {visibility: hidden;}
        .stApp > footer {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        .stDeployButton {display: none;}
        
        /* Custom app styling */
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        .main-container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 25px;
            padding: 30px 20px;
            margin: 20px 10px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .app-header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .store-logo {
            width: 60px;
            height: 60px;
            background: linear-gradient(45deg, #4CAF50, #45a049);
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            margin-bottom: 15px;
            box-shadow: 0 8px 25px rgba(76, 175, 80, 0.3);
        }
        
        .app-title {
            font-size: 2.2rem;
            font-weight: 700;
            color: #2c3e50;
            margin: 10px 0;
            letter-spacing: -0.5px;
        }
        
        .app-subtitle {
            font-size: 1.1rem;
            color: #7f8c8d;
            font-weight: 400;
            line-height: 1.4;
        }
        
        /* Rating buttons */
        .stButton > button {
            width: 100% !important;
            height: 75px !important;
            border: none !important;
            border-radius: 18px !important;
            margin: 8px 0 !important;
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            cursor: pointer !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08) !important;
            border: 2px solid transparent !important;
            position: relative !important;
            overflow: hidden !important;
        }
        
        /* Individual button colors */
        .stButton > button[data-testid*="rating_5"] {
            background: linear-gradient(135deg, #4CAF50, #45a049) !important;
            color: white !important;
        }
        
        .stButton > button[data-testid*="rating_4"] {
            background: linear-gradient(135deg, #8BC34A, #7CB342) !important;
            color: white !important;
        }
        
        .stButton > button[data-testid*="rating_3"] {
            background: linear-gradient(135deg, #FFC107, #FF9800) !important;
            color: white !important;
        }
        
        .stButton > button[data-testid*="rating_2"] {
            background: linear-gradient(135deg, #FF9800, #F57C00) !important;
            color: white !important;
        }
        
        .stButton > button[data-testid*="rating_1"] {
            background: linear-gradient(135deg, #F44336, #D32F2F) !important;
            color: white !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15) !important;
        }
        
        .stButton > button:active {
            transform: translateY(-1px) !important;
        }
        
        /* Thank you screen */
        .thank-you-container {
            text-align: center;
            padding: 40px 20px;
        }
        
        .thank-you-icon {
            width: 80px;
            height: 80px;
            background: linear-gradient(45deg, #4CAF50, #45a049);
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 2.5rem;
            margin-bottom: 20px;
            animation: bounce 0.6s ease-out;
        }
        
        .thank-you-title {
            font-size: 2rem;
            font-weight: 700;
            color: #2c3e50;
            margin: 15px 0;
        }
        
        .rating-display {
            font-size: 1.3rem;
            color: #7f8c8d;
            margin: 15px 0;
            padding: 15px;
            background: rgba(76, 175, 80, 0.1);
            border-radius: 12px;
            border-left: 4px solid #4CAF50;
        }
        
        /* Comment form */
        .comment-container {
            padding: 20px 0;
        }
        
        .stTextArea > div > div > textarea {
            border-radius: 15px !important;
            border: 2px solid #e0e0e0 !important;
            font-size: 1rem !important;
            padding: 15px !important;
            min-height: 120px !important;
            font-family: inherit !important;
        }
        
        .stTextArea > div > div > textarea:focus {
            border-color: #4CAF50 !important;
            box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1) !important;
        }
        
        /* Action buttons */
        .action-buttons {
            display: flex;
            gap: 10px;
            margin-top: 20px;
        }
        
        .stButton > button[data-testid*="secondary"] {
            background: rgba(255, 255, 255, 0.9) !important;
            color: #666 !important;
            border: 2px solid #e0e0e0 !important;
        }
        
        .stButton > button[data-testid*="primary"] {
            background: linear-gradient(135deg, #4CAF50, #45a049) !important;
            color: white !important;
        }
        
        /* Animations */
        @keyframes bounce {
            0%, 20%, 60%, 100% { transform: translateY(0); }
            40% { transform: translateY(-10px); }
            80% { transform: translateY(-5px); }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .main-container {
            animation: fadeIn 0.5s ease-out;
        }
        
        /* Mobile responsive */
        @media (max-width: 480px) {
            .main-container {
                margin: 10px 5px;
                padding: 25px 15px;
            }
            
            .app-title {
                font-size: 1.8rem;
            }
            
            .app-subtitle {
                font-size: 1rem;
            }
            
            .stButton > button {
                height: 70px !important;
                font-size: 1rem !important;
            }
            
            .thank-you-title {
                font-size: 1.6rem;
            }
        }
        
        /* Footer */
        .app-footer {
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid rgba(0, 0, 0, 0.1);
            color: #95a5a6;
            font-size: 0.85rem;
        }
    </style>
    """

# Initialize session state
if 'show_thank_you' not in st.session_state:
    st.session_state.show_thank_you = False
if 'show_comment_option' not in st.session_state:
    st.session_state.show_comment_option = False
if 'current_rating' not in st.session_state:
    st.session_state.current_rating = None

def save_review(rating, comment=""):
    """Save review to CSV file"""
    review_data = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'rating': rating,
        'comment': comment.strip()
    }
    
    filename = "reviews.csv"
    df = pd.DataFrame([review_data])
    
    if os.path.exists(filename):
        existing_df = pd.read_csv(filename)
        df = pd.concat([existing_df, df], ignore_index=True)
    
    df.to_csv(filename, index=False)

def reset_form():
    """Reset the form after submission"""
    st.session_state.show_thank_you = False
    st.session_state.show_comment_option = False
    st.session_state.current_rating = None

def main():
    # Load custom CSS
    st.markdown(load_custom_css(), unsafe_allow_html=True)
    
    # Main container
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # App header
    st.markdown("""
    <div class="app-header">
        <div class="store-logo">🏪</div>
        <div class="app-title">Kirmani's Store</div>
        <div class="app-subtitle">We value your feedback</div>
    </div>
    """, unsafe_allow_html=True)
    
    emojis = ["😞", "😟", "😐", "😊", "😄"]
    labels = ["Very Poor", "Poor", "Average", "Good", "Excellent"]
    
    # Main rating screen
    if not st.session_state.show_thank_you and not st.session_state.show_comment_option:
        st.markdown('<div style="text-align: center; margin: 20px 0; font-size: 1.2rem; color: #555;">How was your experience today?</div>', unsafe_allow_html=True)
        
        # Rating buttons with emojis
        if st.button("😄 Excellent", key="rating_5"):
            save_review(5)
            st.session_state.current_rating = 5
            st.session_state.show_thank_you = True
            st.rerun()
            
        if st.button("😊 Good", key="rating_4"):
            save_review(4)
            st.session_state.current_rating = 4
            st.session_state.show_thank_you = True
            st.rerun()
            
        if st.button("😐 Average", key="rating_3"):
            save_review(3)
            st.session_state.current_rating = 3
            st.session_state.show_thank_you = True
            st.rerun()
            
        if st.button("😟 Poor", key="rating_2"):
            save_review(2)
            st.session_state.current_rating = 2
            st.session_state.show_thank_you = True
            st.rerun()
            
        if st.button("😞 Very Poor", key="rating_1"):
            save_review(1)
            st.session_state.current_rating = 1
            st.session_state.show_thank_you = True
            st.rerun()
    
    # Comment screen
    elif st.session_state.show_comment_option:
        st.markdown('<div style="text-align: center; margin: 20px 0; font-size: 1.3rem; color: #555;">Tell us more about your experience</div>', unsafe_allow_html=True)
        
        if st.session_state.current_rating:
            selected_idx = st.session_state.current_rating - 1
            st.markdown(f"""
            <div class="rating-display">
                <strong>Your Rating:</strong> {emojis[selected_idx]} {labels[selected_idx]}
            </div>
            """, unsafe_allow_html=True)
        
        comment = st.text_area("", placeholder="What made your experience special? Your feedback helps us improve...", height=120, key="comment_input")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Skip", key="skip_comment", type="secondary"):
                reset_form()
                st.rerun()
        with col2:
            if st.button("Submit Feedback", key="submit_comment", type="primary"):
                if comment.strip():
                    filename = "reviews.csv"
                    if os.path.exists(filename):
                        df = pd.read_csv(filename)
                        if len(df) > 0:
                            df.iloc[-1, df.columns.get_loc('comment')] = comment.strip()
                            df.to_csv(filename, index=False)
                reset_form()
                st.rerun()
    
    # Thank you screen
    else:
        selected_idx = (st.session_state.current_rating - 1) if st.session_state.current_rating else 0
        st.markdown(f"""
        <div class="thank-you-container">
            <div class="thank-you-icon">🙏</div>
            <div class="thank-you-title">Thank You!</div>
            <div class="rating-display">
                You rated us: {emojis[selected_idx]} {labels[selected_idx]}
            </div>
            <p style="color: #7f8c8d; font-size: 1rem;">Your feedback helps us serve you better!</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📝 Add Details", key="add_comment", type="secondary"):
                st.session_state.show_comment_option = True
                st.session_state.show_thank_you = False
                st.rerun()
        
        with col2:
            if st.button("✅ Complete", key="complete", type="primary"):
                reset_form()
                st.rerun()
    
    # Footer
    st.markdown("""
    <div class="app-footer">
        <div>🌟 Powered by Customer Care Technology</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()