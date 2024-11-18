from flask import Flask,jsonify

app = Flask(__name__)

dishes = [
    {"name": "Wiener Schnitzel","price":"12"},
    {"name": "Pommes","price":"6"},
    {"name": "Rindergulasch","price":"17"},
    {"name": "Pizza","price":"9"},
    {"name": "Salat","price":"7"},
]

@app.route('/dishes/<string:name>',methods=["DELETE"])
def delete_dish(name):
    for x in dishes:
        if x.get("name")== name:
            dishes.remove(x)
            return jsonify({"success": str(name)+" deleted"})
    return jsonify({"error": str(name)+ " not found"})

if __name__ == '__main__':
    app.run()