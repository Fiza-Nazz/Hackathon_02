import sys
import os

# Ultra-Resilient Entry Point for Hugging Face (v2.3)
print("ENTRY POINT: Starting system initialization...")

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Register paths for all sub-packages
backend_path = os.path.join(current_dir, "backend")
backend_src_path = os.path.join(backend_path, "src")

if backend_path not in sys.path:
    sys.path.append(backend_path)
if backend_src_path not in sys.path:
    sys.path.append(backend_src_path)

print(f"DEBUG: sys.path is {sys.path}")

try:
    print("ENTRY POINT: Attempting to import 'backend.src.main'...")
    from backend.src.main import app
    print("SUCCESS: System link established via backend.src.main")
except ImportError as e:
    print(f"IMPORT ERROR: Primary link failed: {e}")
    try:
        print("ENTRY POINT: Attempting fallback to 'src.main'...")
        from src.main import app
        print("SUCCESS: System link established via fallback src.main")
    except ImportError as e2:
        print(f"FATAL: All system links failed. Primary: {e}, Fallback: {e2}")
        raise e2

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 7860))
    print(f"ENTRY POINT: Launching Uvicorn on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
