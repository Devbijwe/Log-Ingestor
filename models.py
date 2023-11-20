from app import app,db
class LogMySQL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(50))
    message = db.Column(db.String(255))
    resourceId = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime)
    traceId = db.Column(db.String(50))
    spanId = db.Column(db.String(50))
    commit = db.Column(db.String(50))
    parentResourceId = db.Column(db.String(50))

