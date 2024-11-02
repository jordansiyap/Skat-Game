from flask import Flask, jsonify, request, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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


@app.route('/dishes', methods=['POST'])
def add_dish():
    if not request.json or 'name' not in request.json or 'price' not in request.json:
        abort(400, description="provide a nname and price for the dish.")
    
    new_dish = {
        'name': request.json['name'],
        'price': request.json['price']
    }
    
    dishes.append(new_dish)
    return jsonify(new_dish), 201


@app.route('/dishes/<string:name>', methods=['DELETE'])
def delete_dish(name):
    dish = next((dish for dish in dishes if dish["name"] == name), None)
    
    if dish is None:
        abort(404, description="Dish not found.")
    
    dishes.remove(dish)
    return jsonify({'result': True})


if __name__ == '__main__':
    app.debug = True
    app.name = "SpeiseKarte"
    app.run()
