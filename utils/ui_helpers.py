# utils/ui_helpers.py

import streamlit as st

def apply_custom_styles() -> None:
    """Applies custom CSS styles to enhance the Streamlit UI."""
    st.markdown("""
        <style>
            .title {
                text-align: center;
                font-size: 48px;
                font-weight: bold;
                color: #4A90E2;
                margin-bottom: 10px;
            }
            .subheader {
                font-size: 18px;
                font-weight: bold;
                color: #4A90E2;
                margin-bottom: 5px;
            }
            .footer {
                text-align: center;
                font-size: 14px;
                color: gray;
                margin-top: 50px;
            }
        </style>
    """, unsafe_allow_html=True)

def render_title() -> None:
    """Renders the application title in the UI."""
    st.markdown("<p class='title'>🤖 TMRW QA AI Assistant</p>", unsafe_allow_html=True)

def render_footer() -> None:
    """Renders a footer message at the bottom of the page."""
    st.markdown("<p class='footer'>✨ Built with ❤️ for TMRW's Engineers</p>", unsafe_allow_html=True)
