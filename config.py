from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

# Upload settings
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'pdf', 'pptx', 'docx', 'txt'}
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50 MB
