"""
Professional QR Code Database Model
===================================
Clean, production-ready SQLAlchemy model with proper relationships and indexes
"""

from datetime import datetime,timedelta
from sqlalchemy import Index
from pathlib import Path
from . import db

# Initialize database

class QRCode(db.Model):
    """
    QR Code model with scan tracking and file management.
    
    Fields:
        id: Primary key
        original_data: URL/link or file reference
        qr_image: Path to generated QR image
        file_name: Original uploaded filename (if any)
        created_at: Timestamp of creation
        scans: Number of times QR was scanned
        is_active: Soft delete flag
    """
    
    __tablename__ = 'qr_codes'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Data fields
    original_data = db.Column(db.Text, nullable=False, index=True)
    qr_image = db.Column(db.String(300), nullable=False, index=True)
    file_name = db.Column(db.String(255), nullable=True)
    
    # Timestamps
    created_at = db.Column(
        db.DateTime, 
        default=datetime.utcnow,
        nullable=False,
        index=True
    )
    updated_at = db.Column(
        db.DateTime, 
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # Tracking
    scans = db.Column(db.Integer, default=0, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Relationships (optional)
    # scans_history = db.relationship('QRScan', backref='qr_code', lazy=True)
    
    def __repr__(self):
        return f'<QRCode {self.id}: {self.original_data[:50]}...>'
    
    def to_dict(self) -> dict:
        """Convert model to JSON-serializable dict."""
        return {
            'id': self.id,
            'original_data': self.original_data,
            'qr_image': self.qr_image,
            'file_name': self.file_name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'scans': self.scans,
            'is_active': self.is_active
        }
    
    def increment_scans(self):
        """Increment scan counter."""
        self.scans += 1
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    @classmethod
    def cleanup_old(cls, days: int = 30):
        """Soft-delete old QR codes."""
        cutoff = datetime.utcnow() - timedelta(days=days)
        count = cls.query.filter(
            cls.created_at < cutoff,
            cls.is_active == True
        ).update({
            cls.is_active: False
        }, synchronize_session=False)
        db.session.commit()
        return count
    
    @classmethod
    def recent(cls, limit: int = 50):
        """Get recent active QR codes."""
        return cls.query.filter_by(is_active=True)\
                       .order_by(cls.created_at.desc())\
                       .limit(limit).all()

# Indexes for performance
Index('idx_qr_created_scans', QRCode.created_at, QRCode.scans)
Index('idx_qr_active', QRCode.is_active, QRCode.created_at)

# Optional: Scan history model
class QRScan(db.Model):
    """
    QR Code scan tracking (optional).
    """
    __tablename__ = 'qr_scans'
    
    id = db.Column(db.Integer, primary_key=True)
    qr_code_id = db.Column(db.Integer, db.ForeignKey('qr_codes.id'), nullable=False)
    scanned_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_agent = db.Column(db.String(500))
    ip_address = db.Column(db.String(45))
    
    qr_code = db.relationship('QRCode', backref=db.backref('scans_history', lazy=True))
    
    __table_args__ = (
        Index('idx_scan_qr_time', 'qr_code_id', 'scanned_at'),
    )

# Usage example:
"""
# In your main app.py:
from flask import Flask
from models import db, init_db, QRCode

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qr_codes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
init_db(app)

@app.route('/create_qr')
def create_qr():
    qr = QRCode(
        original_data='https://example.com',
        qr_image='static/qr_codes/qr_123.png',
        file_name='document.pdf'
    )
    db.session.add(qr)
    db.session.commit()
    return qr.to_dict()
"""