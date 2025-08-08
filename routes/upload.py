from flask import Blueprint, request, jsonify
import os
import xml.etree.ElementTree as ET
from datetime import datetime
from models.db import db
from models.record import Record, RecordMetadata

upload_bp = Blueprint("upload", __name__)


@upload_bp.route("/upload", methods=["POST"])
def upload_xml():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    temp_path = os.path.join("temp", file.filename)
    os.makedirs("temp", exist_ok=True)
    file.save(temp_path)

    try:
        tree = ET.parse(temp_path)
        root = tree.getroot()
        records = root.findall(".//Record")
        count = 0

        for record in records:
            record_type = record.get("type")
            start_date = record.get("startDate")
            end_date = record.get("endDate")
            value = record.get("value")
            unit = record.get("unit")
            source_name = record.get("sourceName")
            source_version = record.get("sourceVersion")
            device = record.get("device")
            creation_date = record.get("creationDate")

            try:
                start_dt = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S %z")
                end_dt = (
                    datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S %z")
                    if end_date
                    else None
                )
                creation_dt = (
                    datetime.strptime(creation_date, "%Y-%m-%d %H:%M:%S %z")
                    if creation_date
                    else None
                )
            except Exception:
                continue

            db_record = Record(
                type=record_type,
                start_date=start_dt,
                end_date=end_dt,
                value=value,
                unit=unit,
                source_name=source_name,
                source_version=source_version,
                device=device,
                creation_date=creation_dt,
            )
            db.session.add(db_record)
            db.session.flush()

            for meta in record.findall("MetadataEntry"):
                key = meta.get("key")
                val = meta.get("value")
                if key and val:
                    db.session.add(
                        RecordMetadata(record_id=db_record.id, key=key, value=val)
                    )
            count += 1

        db.session.commit()
        os.remove(temp_path)
        return jsonify({"message": f"Successfully ingested {count} records."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
