# main.py
import os
from app import create_app

app = create_app()  # required for waitress-serve

# Optional: run with Python directly (not used by waitress)
if __name__ == "__main__":
    from waitress import serve
    port = int(os.getenv("PORT", 5000))
    serve(app, host="0.0.0.0", port=port)
