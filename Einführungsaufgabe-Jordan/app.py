from flask import Flask, jsonify, request, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initial list of dishes (they only last while the app is running)
dishes = [
    {"name": "Wiener Schnitzel", "price": 12},
    {"name": "Pommes", "price": 6},
    {"name": "Rindergulasch", "price": 17},
    {"name": "Pizza", "price": 9},
    {"name": "Salat", "price": 7}
]

@app.route('/dishes', methods=['GET'])
def get_dishes():
    sort_by = request.args.get('sort_by')
    
    if sort_by == 'name':
        sorted_dishes = sorted(dishes, key=lambda x: x['name'])
    elif sort_by == 'price':
        sorted_dishes = sorted(dishes, key=lambda x: x['price'])
    else:
        sorted_dishes = dishes
    
    return jsonify(sorted_dishes)



if __name__ == '__main__':
    app.debug = True
    app.name = "SpeiseKarte"
    app.run(host="localhost", port=8081)
