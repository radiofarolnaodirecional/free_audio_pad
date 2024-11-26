from extensions import db
from datetime import datetime, timezone

class Tracks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    tag = db.Column(db.String(120), nullable=False)
    url = db.Column(db.String(120), nullable=False)
    img_url = db.Column(db.String(120), nullable=True)
    date_added = db.Column(db.DateTime, default=lambda: datetime.now(tz=timezone.utc))

    def __repr__(self):
        return '<Name %r>' % self.name

class Usercfg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    in_device = db.Column(db.String(120), default='select')
    out_device = db.Column(db.String(120), default='select')
    show_img = db.Column(db.Boolean(), default=True)
    show_track_details = db.Column(db.Boolean(), default=True)
    mic_on = db.Column(db.Boolean(), default=False)
    vol_in = db.Column(db.Integer(), default=100)
    vol_out = db.Column(db.Integer(), default=50)
