from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import xml.etree.ElementTree as ET
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///health_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class HealthRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    record_type = db.Column(db.String(128))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    value = db.Column(db.String(128))

@app.before_first_request
def create_tables():
    db.create_all()

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

    # Parse XML and store in DB
    try:
        tree = ET.parse(temp_path)
        root = tree.getroot()
        records = root.findall('.//Record')
        for record in records:
            record_type = record.get('type')
            start_date = record.get('startDate')
            end_date = record.get('endDate')
            value = record.get('value')
            try:
                start_dt = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S %z')
                end_dt = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S %z') if end_date else None
            except Exception:
                continue
            db_record = HealthRecord(
                record_type=record_type,
                start_date=start_dt,
                end_date=end_dt,
                value=value
            )
            db.session.add(db_record)
        db.session.commit()
        os.remove(temp_path)
        return jsonify({'message': f'Successfully ingested {len(records)} records.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
     with app.app_context():
         db.create_all()
     app.run(debug=True)