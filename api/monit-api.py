from flask import Flask, request, jsonify, render_template
from bson import ObjectId
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['monit-app']
collection = db['data']

@app.route('/api/data/post', methods=['POST'])
def add_data():
    data = request.json 
    inserted = collection.insert_one(data)
    return jsonify({'message': 'Data added successfully', 'id': str(inserted.inserted_id)}), 201


@app.route('/reports', methods=['GET'])
def get_all_data():
    data = list(collection.find({}))
    for item in data:
        item['_id'] = str(item['_id'])

    return jsonify(data), 200

@app.route('/reports/<id>', methods=['GET'])
def get_data(id):
    try:
        obj_id = ObjectId(id)
        
        data = list(collection.find({'_id': obj_id}))
        
        for item in data:
            item['_id'] = str(item['_id'])

        return jsonify(data), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 404
    
@app.route('/', methods=['GET'])
def get_index():
    return render_template('index.html')
     

if __name__ == '__main__':
    app.run(host="0.0.0.0" , debug=True, port=8085)
