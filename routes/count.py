from flask import Blueprint, jsonify
from models.record import Record, RecordMetadata

count_bp = Blueprint("count", __name__)


@count_bp.route("/count")
def count_records():
    rec_count = Record.query.count()
    meta_count = RecordMetadata.query.count()
    return jsonify({"records": rec_count, "metadata_entries": meta_count})
