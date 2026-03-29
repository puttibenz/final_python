import streamlit as st
from utils.auth import auth_manager

class BasePage:
    """Base class for all pages to handle common layout, styling, and auth."""

    def __init__(self, title, subtitle, require_auth=True):
        if require_auth:
            auth_manager.check_auth_required()
        
        self.user = st.session_state.get("user")
        self.user_id = self.user["id"] if self.user else None
        self.title = title
        self.subtitle = subtitle

    def render_common_css(self):
        """Centralized CSS for all pages."""
        st.markdown("""
        <style>
            /* Global Layout */
            .block-container {
                max-width: 1400px !important;
                padding-left: 5rem !important;
                padding-right: 5rem !important;
            }
            
            /* Animations */
            @keyframes slideUp {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            .stApp { animation: slideUp 0.5s ease-out; }

            /* Header Styling */
            .page-header { text-align: center; padding: 2rem 0 3rem; }
            .page-header h1 {
                font-size: 2.8rem;
                font-weight: 800;
                background: linear-gradient(135deg, #66BB6A, #2E7D32);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 0.5rem;
            }
            .page-header p { color: #888; font-size: 1.1rem; }
        </style>
        """, unsafe_allow_html=True)

    def render_header(self):
        """Displays the consistent header for each page."""
        self.render_common_css()
        st.markdown(f"""
        <div class="page-header">
            <h1>{self.title}</h1>
            <p>{self.subtitle}</p>
        </div>
        """, unsafe_allow_html=True)
        st.divider()
