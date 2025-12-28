import streamlit as st
import logging
import sys
import os
from datetime import datetime, timezone

# Add project root to path if needed
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from core.config import AppConfig
from core.product_service import EnhancedProductReviewService
from core.ui import EnhancedStreamlitUI

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main entry point for the ProductIntelligence AI application."""
    
    # Configure page settings - must be the first Streamlit command
    st.set_page_config(
        page_title="ProductIntelligence AI (Nigeria Edition)",
        page_icon="🇳🇬",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    try:
        # Initialize Config (loads environment variables)
        config = AppConfig()
        
        # Initialize the main service orchestrator
        # This will set up all sub-services (Price, Sentiment, AI, etc.)
        service = EnhancedProductReviewService()
        
        # Initialize the User Interface
        ui = EnhancedStreamlitUI(service)
        
        # Render the application
        ui.render()
        
    except Exception as e:
        st.error(f"An critical error occurred: {e}")
        logger.exception("Application launch failed")
        
        # Fallback for missing API keys or configuration issues
        if "API_KEY" in str(e) or "environment variable" in str(e).lower():
            st.warning("Please ensure your .env file is correctly configured with GROQ_API_KEY and RAPIDAPI_KEY.")

if __name__ == "__main__":
    main()
