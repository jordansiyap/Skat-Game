from flask import Flask,jsonify,request

app = Flask(__name__)

dishes = [
    {"name": "Wiener Schnitzel","price":"12"},
    {"name": "Pommes","price":"6"},
    {"name": "Rindergulasch","price":"17"},
    {"name": "Pizza","price":"9"},
    {"name": "Salat","price":"7"},
]

@app.route('/dishes',methods=["POST"])
def add_dish():
    dish =request.json

    if "name" not in dish:
        return jsonify({"error": "no name for the dish"}),404
    elif "price" not in dish:
        return jsonify({"error": "no price for the dish"}),404
    else:
        new_dish = {
            "name": str(dish.get("name")), "price": str(dish.get("price"))
        }
        dishes.append(new_dish)
        return dishes,201

if __name__ == '__main__':
    app.run()