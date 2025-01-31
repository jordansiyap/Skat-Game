from flask import Flask, jsonify
"""
gibt die verfügbaren KI optionen zurück
"""
class GetAIOptions:
    @staticmethod
    def get_models():
        # Definiere die Modelle direkt hier als Liste von Dictionaries
        models = [
            {
                "name": "Easy Rule-based Bot",
                "difficulty": 1,
                "description": "Reizen nur einmal den niedrigsten Wert. Spielrunde: spielt zufällige valide Karte"
            },
            {
                "name": "Average Rule-based Bot",
                "difficulty": 2,
                "description": "Spielt bis der Reizwert einen bestimmten Abstand zum maximalen Wert hat.Spielrunde: versucht jede Runde möglichst billig zu übertrumpfen/unterbieten (Nullspiel)"
            },
            {
                "name": "Hardest Rule-based Bot",
                "difficulty": 3,
                "description": "Komplexere Spiellogik. Spielrunde: versucht für sein team möglichst viele Punkte zu erzielen"
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