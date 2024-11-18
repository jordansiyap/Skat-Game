from flask import Flask,jsonify,request

app = Flask(__name__)

dishes = [
    {"name": "Wiener Schnitzel","price":"12"},
    {"name": "Pommes","price":"6"},
    {"name": "Rindergulasch","price":"17"},
    {"name": "Pizza","price":"9"},
    {"name": "Salat","price":"7"},
]

@app.route('/dishes',methods=["GET"])
def get_dishes():
    sort = request.args.get("sort")
    if sort == "name":
        dishes.sort(key = lambda dish: dish['name'])
        return jsonify(dishes)
    elif sort =="price":
        dishes.sort(key = lambda dish: int(dish['price']))
        return jsonify(dishes)
    else:
        return jsonify({"error": str(sort)+" is not a parameter to sort the dishes"}),404

if __name__ == '__main__':
    app.run()
