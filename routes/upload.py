from flask import Blueprint, request, jsonify
import os
from lxml import etree
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
        count = 0
        batch_size = 1000  # Process in batches to manage memory
        
        # Use streaming XML parser to avoid loading entire file into memory
        context = etree.iterparse(temp_path, events=('end',), tag='Record')
        
        for event, record in context:
            try:
                record_type = record.get("type")
                start_date = record.get("startDate")
                end_date = record.get("endDate")
                value = record.get("value")
                unit = record.get("unit")
                source_name = record.get("sourceName")
                source_version = record.get("sourceVersion")
                device = record.get("device")
                creation_date = record.get("creationDate")

                # Parse dates
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

                # Create record
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

                # Process metadata
                for meta in record.findall("MetadataEntry"):
                    key = meta.get("key")
                    val = meta.get("value")
                    if key and val:
                        db.session.add(
                            RecordMetadata(record_id=db_record.id, key=key, value=val)
                        )
                
                count += 1
                
                # Commit in batches to manage memory
                if count % batch_size == 0:
                    db.session.commit()
                    print(f"Processed {count} records...")
                
                # Clear the element to free memory
                record.clear()
                
            except Exception as e:
                print(f"Error processing record: {e}")
                continue
        
        # Final commit for remaining records
        try:
            db.session.commit()
            print(f"Final commit successful. Total records processed: {count}")
        except Exception as commit_error:
            print(f"Final commit failed: {commit_error}")
            db.session.rollback()
            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return jsonify({"error": f"Database commit failed: {str(commit_error)}"}), 500
        
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        return jsonify({"message": f"Successfully ingested {count} records."}), 200

    except Exception as e:
        print(f"Upload error: {e}")
        # Clean up on error
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500
