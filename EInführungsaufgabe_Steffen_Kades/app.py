from flask import Flask
import json

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)



"""
erster versuch
class Produkt:
    def __init__(self, name: str, preis: float):
        if not isinstance(name, str):
            raise TypeError(f"json datei fehlerhaft")
        
        if not isinstance(preis, (float, int)):  
            raise TypeError(f"json datei fehlerhaft")
        
        self.name = name
        self.preis = preis

    def __repr__(self):
        return f"Produkt(name='{self.name}', preis={self.preis})"
    
gerichte = []
gerichte.append(Produkt("Wiener Schnitzel",12))
gerichte.append(Produkt("Pommes",6))
gerichte.append(Produkt("Rindergulasch",17))
gerichte.append(Produkt("Pizza",9))
gerichte.append(Produkt("Salat",7))

@app.route('/gerichte', methods=['GET'])
def get_gerichte():
    sortierung = request.args.get('sortierung', 'name')
    if sortierung == 'preis':
        gerichte.sort(key=lambda gericht: gericht['preis'])
    else:
        gerichte.sort(key=lambda gericht: gericht['name'])
    return jsonify(gerichte)


@app.route('/gerichte', methods=['POST'])
def add_gericht():
    with open('request.json', 'r') as file:
        data = json.load(file)
    
        gerichte.append(Produkt(data.get('name'),data.get('price')))
    return jsonify(gerichte[-1]), 201
    


@app.route('/gerichte/<string:name>', methods=['DELETE'])
def delete_gericht(name):
    for produkt in gerichte:
        if produkt['name'] == name:
            gerichte.remove(produkt)

    return jsonify({"message": f"{name} gelöscht."}), 200


"""


"""
mehr python syntax
gerichte2 = [
    {"name": "Wiener Schnitzel", "preis": 12},
    {"name": "Pommes", "preis": 6},
    {"name": "Rindergulasch", "preis": 17},
    {"name": "Pizza", "preis": 9},
    {"name": "Salat", "preis": 7},
]


@app.route('/gerichte', methods=['GET'])
def get_gerichte():
    sortierung = request.args.get('sortierung', 'name')
    if sortierung == 'preis':
        gerichte2.sort(key=lambda gericht: gericht['preis'])
    else:
        gerichte2.sort(key=lambda gericht: gericht['name'])
    return jsonify(gerichte2)


@app.route('/gerichte', methods=['POST'])
def add_gericht():
    new_gericht = request.json
    if 'name' in new_gericht and 'preis' in new_gericht:
        gerichte2.append(new_gericht)
        return jsonify(new_gericht), 201
    return jsonify({"error": "Name und Preis müssen angegeben werden."}), 400


@app.route('/gerichte/<string:name>', methods=['DELETE'])
def delete_gericht(name):
    global gerichte2
    gerichte2 = [gericht for gericht in gerichte2 if gericht['name'] != name]
    return jsonify({"message": f"{name} gelöscht."}), 200


"""
"""
mit db
"""
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Produkte(db.Model):
    gericht = db.Column(db.String(500), primary_key=True) 
    preis = db.Column(db.Integer, nullable=False)

@app.route('/gerichte', methods=['GET'])
def get_gerichte():

    sort_by = request.args.get('sortierung', 'name')

    if sort_by == 'preis':
        produkte = Produkte.query.order_by(Produkte.preis).all()
    else:
        produkte = Produkte.query.order_by(Produkte.gericht).all()
    return jsonify([{'gericht': p.gericht, 'preis': p.preis} for p in produkte])


@app.route('/gerichte', methods=['POST'])
def add_gericht():
    data = request.json  
    if not data or 'name' not in data or 'preis' not in data:
        return jsonify({"ungültige eingabe"}), 400
    
    produkt = Produkte.query.filter_by(gericht=data['name']).first()
    if produkt:
        return jsonify({"message": f"{data['name']} ist bereits vorhanden."}), 400
    
    new_produkt = Produkte(gericht=data['name'], preis=data['preis'])  
    db.session.add(new_produkt)
    db.session.commit()

    return jsonify({'gericht': new_produkt.gericht, 'preis': new_produkt.preis}), 201


@app.route('/gerichte/<string:name>', methods=['DELETE'])
def delete_gericht(name):
    produkt = Produkte.query.filter_by(gericht=name).first()
    if produkt:
        db.session.delete(produkt)
        db.session.commit()
        return jsonify({"message": f"{name} gelöscht."}), 200
    else:
        return jsonify({"message": f"{name} nicht gefunden."}), 404

if __name__ == '__main__':

    app.run(debug=True)