from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/get_ai_options', methods=['GET'])
def get_models():
    # Definiere die Modelle direkt hier als Liste von Dictionaries
    models = [
        {
            "name": "Easy Rule-based Bot",
            "difficulty": 1,
            "description": "Reizen nur einmal den niedrigsten Wert, spielt zufällige valide Karte"
        },
        {
            "name": "Average Rule-based Bot",
            "difficulty": 2,
            "description": "Spielt bis der Reizwert einen bestimmten Abstand zum maximalen Wert hat, versucht jede Runde möglichst billig zu übertrumpfen/unterbieten (Nullspiel)"
        },
        {
            "name": "Hardest Rule-based Bot",
            "difficulty": 3,
            "description": "Komplexere Spiellogik"
        },
        {
            "name": "RL Bot (Weakest)",
            "difficulty": 2,
            "description": "Komplexere Spiellogik"
        },
        {
            "name": "RL Bot (Average)",
            "difficulty": 3,
            "description": "Komplexere Spiellogik"
        },
        {
            "name": "RL Bot (Hardest)",
            "difficulty": 5,
            "description": "Komplexere Spiellogik"
        }
    ]
   
    return jsonify(models), 200

if __name__ == '__main__':
    app.run(debug=True)