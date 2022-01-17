from flask import Flask, jsonify, request
import json
import os

from common import logger

app = Flask(__name__)

@app.route('/', methods=['GET'])
def welcome():
    return jsonify({"Message": "hello my dears"})

@app.route('/<eid>', methods=['GET'])
def query_records(eid):
    logger.debug(f"----[{eid}] ----")
    with open('data.json') as f:
        data = f.read()
        records = json.loads(data)
        for record in records:
            if record['eid'] == int(eid):
                return jsonify(record)
        return jsonify({'error': 'data not found'})


@app.route('/', methods=['PUT'])
def create_record():
    record = json.loads(request.data)
    logger.debug(record)
    records = None
    
    if os.path.exists('data.json'):

        with open('data.json') as f:
            data = f.read()
    
        if not data:
            records = [record]
        else:
            records = json.loads(data)
            records.append(record)
    else:
        records = [record]

    with open('data.json', 'w') as f:
        f.write(json.dumps(records, indent=2))
    return jsonify({'status': "Record has been created!"})


@app.route('/', methods=['POST'])
def update_record():
    record = json.loads(request.data)
    new_records = []
    with open('data.json') as f:
        data = f.read()
        records = json.loads(data)

    for r in records:
        if r['eid'] == record['eid']:
            r['name'] = record['name']
            r['salary'] = record['salary']
            r['full_time'] = record['full_time']
            r['age'] = record['age']
            break

    with open('data.json', 'w') as f:
        f.write(json.dumps(records, indent=2))

    return jsonify({'status': "Record has been updated!"})
    
@app.route('/<int:eid>', methods=['DELETE'])
def delete_record(eid):
    new_records = []
    with open('data.json') as f:
        data = f.read()
        records = json.loads(data)

        for idx, r in enumerate(records):
            if r['eid'] == eid:
                break

        records.pop(idx)

    with open('data.json', 'w') as f:
        f.write(json.dumps(records, indent=2))
    return jsonify({'status': "Record has been deleted!"})

if __name__ == '__main__':
    app.run(debug=True)

# [client]   ---->   [NGINX  --> (WSGI <=> APP)]