from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

gerichte = [
{"name": "Wiener Schnitzel", "price": "12€"},
{"name": "Pommes", "price": "6€"},
{"name": "Rindergulasch", "price": "17€"},
{"name": "Pizza", "price": "9€"},
{"name": "Salat", "price": "7€"}
]
gerichte_put_args = reqparse.RequestParser()
gerichte_put_args.add_argument("name", type = str, required = True, help="Name of gericht is required")
gerichte_put_args.add_argument("price", type = str, required = True, help="Price of gericht is required")

gerichte_del_args = reqparse.RequestParser()
gerichte_del_args.add_argument("name", type = str, required = True, help="Name of gericht is required")

def checkIfPresent(name):
    for i in gerichte:
        if i["name"] == name:
            return i
    return False

class Gericht(Resource):
    def get(self):
        sort = request.args.get("sort", default="price")
        sorted = gerichte.copy()

        if sort == "price":
            sorted.sort(key=lambda x: float(x['price'].replace('€', '')))
        elif sort == "name":
            sorted.sort(key=lambda x: x['name'])
        return jsonify(sorted)

    def put(self):
        args = gerichte_put_args.parse_args()
        gericht = checkIfPresent(args["name"])
        if gericht:
            abort(403, message ="Name is already in use. Update functionality currently not supported.")

        gerichte.append(args)
        return jsonify(args, 201)

    def delete(self):
        args = gerichte_del_args.parse_args()
        gericht = checkIfPresent(args["name"])
        if not gericht:
            abort(404,message ="Gericht not found in menu")

        gerichte.remove(gericht)
        return jsonify({"message": "Gericht deleted successfully"}, 200)

api.add_resource(Gericht, '/gerichte')

if __name__ == '__main__':
    app.run(debug=True)
