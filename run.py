#!/usr/bin/env python3
"""
Clean, simple FastAPI to-do application startup script.
"""
import sys
import os

# Add src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
sys.path.insert(0, src_dir)

try:
    import uvicorn
    from app import app

    print("🚀 Starting Taskion - Simple FastAPI To-Do Application")
    print("📍 http://localhost:8930")
    print("📚 http://localhost:8930/docs")
    print("💚 http://localhost:8930/health")

    uvicorn.run(app, host="0.0.0.0", port=8930, reload=True)

except ImportError as e:
    print(f"❌ {e}")
    print("Run: poetry install && poetry shell")
    sys.exit(1)
