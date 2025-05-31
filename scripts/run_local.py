#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

def setup_local_env():
    """Set up local development environment."""
    # Create necessary directories
    Path("data").mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    
    # Set environment variables for local development
    os.environ["STREAMLIT_CLOUD"] = "0"
    os.environ["DATABASE_URL"] = "postgresql+asyncpg://localhost:5432/jarvis"
    os.environ["DEBUG"] = "1"

def run_local():
    """Run the application locally."""
    setup_local_env()
    
    # Start the FastAPI backend
    backend_cmd = ["uvicorn", "app.main:app", "--reload", "--host", "127.0.0.1", "--port", "8000"]
    backend_process = subprocess.Popen(backend_cmd)
    
    # Start the Streamlit frontend
    frontend_cmd = ["streamlit", "run", "app/frontend/main.py"]
    frontend_process = subprocess.Popen(frontend_cmd)
    
    try:
        # Wait for both processes
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        # Clean up on Ctrl+C
        backend_process.terminate()
        frontend_process.terminate()
        print("\nShutting down...")

if __name__ == "__main__":
    run_local() 