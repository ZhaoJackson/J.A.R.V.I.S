#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path

def setup_local_env():
    """Set up local development environment."""
    os.environ["STREAMLIT_CLOUD"] = "0"
    os.environ["DEBUG"] = "1"

def run_local():
    """Run the Streamlit frontend locally."""
    setup_local_env()
    
    # Start the Streamlit frontend
    frontend_cmd = ["streamlit", "run", "app/frontend/main.py"]
    frontend_process = subprocess.Popen(frontend_cmd)
    
    try:
        # Wait for the process
        frontend_process.wait()
    except KeyboardInterrupt:
        # Clean up on Ctrl+C
        frontend_process.terminate()
        print("\nShutting down...")

if __name__ == "__main__":
    run_local() 