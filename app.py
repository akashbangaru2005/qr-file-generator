import os
import uuid
import logging
import secrets
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request, url_for, send_from_directory, jsonify, abort
from werkzeug.utils import secure_filename

from models import db, init_db
from models.qr_model import QRCode

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS

# -----------------------------
# CONFIG
# -----------------------------

UPLOAD_FOLDER = "uploads"
QR_CODES_FOLDER = "static/qr_codes"

ALLOWED_EXTENSIONS = {"png","jpg","jpeg","gif","pdf","doc","docx","txt"}
MAX_FILE_SIZE = 10 * 1024 * 1024

# -----------------------------
# APP
# -----------------------------

app = Flask(__name__)

app.config["SECRET_KEY"] = secrets.token_hex(16)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///qr_codes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# -----------------------------
# INIT DATABASE
# -----------------------------

db.init_app(app)
init_db(app)

# -----------------------------
# MIDDLEWARE
# -----------------------------

csrf = CSRFProtect(app)

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["5000 per day", "1000 per hour"]
)

CORS(app)

# -----------------------------
# LOGGING
# -----------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -----------------------------
# CREATE DIRECTORIES
# -----------------------------

Path(UPLOAD_FOLDER).mkdir(exist_ok=True)
Path(QR_CODES_FOLDER).mkdir(parents=True, exist_ok=True)

# -----------------------------
# HELPERS
# -----------------------------

def allowed_file(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS


# -----------------------------
# ROUTES
# -----------------------------

@app.route("/")
def index():
    return render_template("index.html")


@csrf.exempt
@app.route("/api/generate", methods=["POST"])
def generate():

    try:

        link = request.form.get("link")
        file = request.files.get("file")

        if not link and not file:
            return jsonify({"success":False,"error":"Link or file required"}),400

        data_url = None
        filename = None

        # -------- LINK --------
        if link:

            data_url = link

        # -------- FILE --------
        elif file and allowed_file(file.filename):

            filename = secure_filename(file.filename)

            unique_name = f"{uuid.uuid4().hex}_{filename}"

            filepath = os.path.join(UPLOAD_FOLDER, unique_name)

            file.save(filepath)

            data_url = url_for("download_file", filename=unique_name, _external=True)


        # -------- GENERATE QR --------

        if data_url:

            import qrcode

            qr_filename = f"{uuid.uuid4().hex}.png"

            qr_path = os.path.join(QR_CODES_FOLDER, qr_filename)

            img = qrcode.make(data_url)

            img.save(qr_path)

            qr_url = url_for("static", filename=f"qr_codes/{qr_filename}", _external=True)

            # -------- SAVE DATABASE --------

            qr_record = QRCode(
                original_data=data_url,
                qr_image=qr_filename,
                file_name=filename
            )

            db.session.add(qr_record)
            db.session.commit()

            logger.info("QR created")

            return render_template("result.html", qr_url=qr_url)

        return jsonify({"success":False,"error":"Processing failed"}),500


    except Exception as e:

        logger.error(str(e))

        return jsonify({"success":False,"error":"Internal server error"}),500


# -----------------------------
# DOWNLOAD FILE
# -----------------------------

@app.route("/download/<filename>")
def download_file(filename):

    path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(path):
        abort(404)

    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)


# -----------------------------
# ERROR HANDLERS
# -----------------------------

@app.errorhandler(404)
def not_found(e):
    return jsonify({"success":False,"error":"Not found"}),404


@app.errorhandler(429)
def rate_limit(e):
    return jsonify({"success":False,"error":"Too many requests"}),429


# -----------------------------
# RUN SERVER
# -----------------------------

if __name__ == "__main__":

    print("🚀 QR Generator running")

    app.run(host="0.0.0.0", port=5000, debug=True)