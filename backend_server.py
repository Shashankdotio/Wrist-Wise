from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import xml.etree.ElementTree as ET
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://appleuser:applepass@localhost:5432/appledb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 600 * 1024 * 1024  # 600 MB limit
db = SQLAlchemy(app)

# ---------------- Models ---------------- #

class Record(db.Model):
    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)  # Optional, for future user tracking
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
    __tablename__ = 'record_metadata'

    id = db.Column(db.Integer, primary_key=True)
    record_id = db.Column(db.Integer, db.ForeignKey('records.id', ondelete='CASCADE'))
    key = db.Column(db.Text)
    value = db.Column(db.Text)

# ---------------- Routes ---------------- #

@app.route('/')
def healthcheck():
    return jsonify({'status': 'ok', 'message': 'Apple Health backend server is running.'}), 200


@app.route('/upload', methods=['POST'])
def upload_xml():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save file temporarily
    temp_path = os.path.join('temp', file.filename)
    os.makedirs('temp', exist_ok=True)
    file.save(temp_path)

    try:
        tree = ET.parse(temp_path)
        root = tree.getroot()
        records = root.findall('.//Record')
        count = 0

        for record in records:
            record_type = record.get('type')
            start_date = record.get('startDate')
            end_date = record.get('endDate')
            value = record.get('value')
            unit = record.get('unit')
            source_name = record.get('sourceName')
            source_version = record.get('sourceVersion')
            device = record.get('device')
            creation_date = record.get('creationDate')

            try:
                start_dt = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S %z')
                end_dt = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S %z') if end_date else None
                creation_dt = datetime.strptime(creation_date, '%Y-%m-%d %H:%M:%S %z') if creation_date else None
            except Exception:
                continue  # skip malformed dates

            db_record = Record(
                type=record_type,
                start_date=start_dt,
                end_date=end_dt,
                value=value,
                unit=unit,
                source_name=source_name,
                source_version=source_version,
                device=device,
                creation_date=creation_dt
            )
            db.session.add(db_record)
            db.session.flush()  # Get db_record.id before commit

            for meta in record.findall('MetadataEntry'):
                key = meta.get('key')
                val = meta.get('value')
                if key and val:
                    db.session.add(RecordMetadata(
                        record_id=db_record.id,
                        key=key,
                        value=val
                    ))
            count += 1

        db.session.commit()
        os.remove(temp_path)
        return jsonify({'message': f'Successfully ingested {count} records.'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# temporary route to count records and metadata entries
@app.route('/count')
def count_records():
    rec_count = Record.query.count()
    meta_count = RecordMetadata.query.count()
    return jsonify({
        'records': rec_count,
        'metadata_entries': meta_count
    })


# ---------------- Main ---------------- #

if __name__ == '__main__':
    # Uncomment only if you're initializing the DB for the first time
    # with app.app_context():
    #     db.create_all()

    app.run(debug=True)
