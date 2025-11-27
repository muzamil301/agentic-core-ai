#!/usr/bin/env python3
"""
Launcher script for the Streamlit web UI.

This script launches the Streamlit web interface for the RAG chat application.
"""

import subprocess
import sys
from pathlib import Path


def main():
    """Launch the Streamlit app."""
    # Get the path to the streamlit app
    ui_path = Path(__file__).parent / "ui" / "streamlit_app.py"
    
    if not ui_path.exists():
        print(f"❌ Streamlit app not found at: {ui_path}")
        sys.exit(1)
    
    print("🚀 Launching RAG Chat Web UI...")
    print("📱 The app will open in your browser automatically")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Launch streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", str(ui_path),
            "--server.headless", "false",
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Shutting down the web UI...")
    except Exception as e:
        print(f"❌ Error launching Streamlit: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

