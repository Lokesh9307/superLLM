from app import create_app
from flask_cors import CORS
from flask_compress import Compress
import os
app = create_app()
Compress(app)

CORS(app)
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", debug=True, port=port)