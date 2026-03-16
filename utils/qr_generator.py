import qrcode
import os
import uuid
from config import QR_FOLDER

def generate_qr(data):

    filename = f"{uuid.uuid4()}.png"
    path = os.path.join(QR_FOLDER, filename)

    qr = qrcode.make(data)
    qr.save(path)

    return filename
import qrcode
from flask import current_app

def generate_qr(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    
    filename = f"qr_{hash(data) % 1000000}.png"
    filepath = f"static/qr_codes/{filename}"
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filepath)
    return filename