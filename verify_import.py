
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath("c:/Users/MSI/Desktop/GenAI/taofeek/updated_project_15/updated_project"))

try:
    from core.analyzers import NetPriceAnalyzer
    print("Successfully imported NetPriceAnalyzer")
except ImportError as e:
    print(f"Import failed: {e}")
except Exception as e:
    print(f"Error: {e}")
