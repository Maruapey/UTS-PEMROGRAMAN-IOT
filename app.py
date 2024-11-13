from datetime import datetime
from flask import Flask, request, send_file, jsonify, render_template
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Aktifkan CORS jika diperlukan

database = [
    {
        "suhumax": 36,
        "suhumin": 21,
        "suhurata": 28.35,
        "nilai_suhu_max_humid_max": [
            {
                "idx": 101,
                "suhu": 36,
                "humid": 36,
                "kecerahan": 25,
                "timestamp": "2010-09-18T07:23:48"
            },
            {
                "idx": 226,
                "suhu": 36,
                "humid": 36,
                "kecerahan": 27,
                "timestamp": "2011-05-02T12:29:34"
            }
        ],
        "month_year_max": [
            {"month_year": "9-2010"},
            {"month_year": "5-2011"}
        ]
    }
]

@app.route('/')
def index_html():
    return render_template('index.html')

@app.route('/api/post', methods=['POST'])
def post_data():
    json_data = request.get_json()

    if not request.is_json or not json_data:
        return jsonify({'message': 'data is not json'}), 400

    new_id = max([item["idx"] for item in database[0]["nilai_suhu_max_humid_max"]], default=0) + 1
    data = {
        'idx': new_id,
        'suhu': int(json_data['suhu']),
        'humid': int(json_data['kelembaban']),
        'kecerahan': int(json_data['kecerahan']),
        'timestamp': datetime.now().isoformat()
    }

    database[0]["nilai_suhu_max_humid_max"].append(data)

    return jsonify({'message': 'success'}), 200

@app.route('/api/get', methods=['GET'])
def get_data():
    data_suhu = [item['suhu'] for item in database[0]["nilai_suhu_max_humid_max"]]
    month_year_max = [
        {
            'month_year': datetime.fromisoformat(item['timestamp']).strftime('%m-%Y')
        } for item in database[0]["nilai_suhu_max_humid_max"]
    ]

    suhumax = max(data_suhu)
    suhumin = min(data_suhu)
    suhurata = sum(data_suhu) / len(data_suhu)

    data = {
        'suhumax': suhumax,
        'suhumin': suhumin,
        'suhurata': suhurata,
        'nilai_suhu_max_humid_max': database[0]["nilai_suhu_max_humid_max"],
        'month_year_max': month_year_max
    }

    return jsonify(data)

@app.route('/api/download', methods=['GET'])
def download_json():
    # Membuat file JSON dari database
    file_path = "data.json"
    with open(file_path, 'w') as f:
        json.dump(database, f, indent=4)

    return send_file(file_path, as_attachment=True, download_name="data.json", mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9990, debug=True)
