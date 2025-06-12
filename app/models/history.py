from datetime import datetime
from ..extensions import db

class History(db.Model):
    __tablename__ = 'history'

    id = db.Column(db.Integer, primary_key=True)
    folder = db.Column(db.String(100))
    viewed_at = db.Column(db.DateTime, default=datetime.utcnow)