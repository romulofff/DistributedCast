from application import db

class Data(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True, unique=True)
    ep_title = db.Column(db.String(255), unique=True)
    author = db.Column(db.String(128), unique=False)
    length = db.Column(db.Integer)
    bucket_url = db.Column(db.String(255), unique=True)
