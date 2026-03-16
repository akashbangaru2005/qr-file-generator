
import os

# Security & Configuration
SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-super-secret-key-change-me'
UPLOAD_FOLDER = 'uploads'
QR_CODES_FOLDER = 'static/qr_codes'
MAX_FILE_SIZE = 200 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {
    'pdf', 'png', 'jpg', 'jpeg', 'gif', 
    'doc', 'docx', 'txt', 'zip'
}
UPLOAD_FOLDER = "uploads"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "static/uploads")
QR_CODES_FOLDER = os.path.join(BASE_DIR, "static/qr_codes")

MAX_FILE_SIZE = 10 * 1024 * 1024

ALLOWED_EXTENSIONS = {
"png","jpg","jpeg","gif",
"pdf","ppt","pptx",
"doc","docx",
"txt"
}

SECRET_KEY = "super-secret-key"

SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
