from models.db import db


class Record(db.Model):
    __tablename__ = "records"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    type = db.Column(db.Text, nullable=False)
    unit = db.Column(db.Text)
    value = db.Column(db.Text)
    source_name = db.Column(db.Text)
    source_version = db.Column(db.Text)
    device = db.Column(db.Text)
    creation_date = db.Column(db.DateTime)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)


class RecordMetadata(db.Model):
    __tablename__ = "record_metadata"

    id = db.Column(db.Integer, primary_key=True)
    record_id = db.Column(db.Integer, db.ForeignKey("records.id", ondelete="CASCADE"))
    key = db.Column(db.Text)
    value = db.Column(db.Text)
