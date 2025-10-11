"""
ResumeCraft - Main Application Entry Point
AI-Powered Resume Management & Candidate Matching System
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def main():
    """
    Main entry point for the ResumeCraft application.
    """
    # Configuration
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    reload = os.getenv("API_RELOAD", "true").lower() == "true"
    log_level = os.getenv("LOG_LEVEL", "info")

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                      ResumeCraft API                         ║
║          AI-Powered Resume Management System                 ║
╚══════════════════════════════════════════════════════════════╝

🚀 Starting server at: http://{host}:{port}
📚 API Documentation: http://{host}:{port}/docs
🔧 ReDoc: http://{host}:{port}/redoc

Configuration:
  - Host: {host}
  - Port: {port}
  - Reload: {reload}
  - Log Level: {log_level}
    """)

    # Run the application
    uvicorn.run(
        "app.services.api:app",
        host=host,
        port=port,
        reload=reload,
        log_level=log_level,
    )


if __name__ == "__main__":
    main()
