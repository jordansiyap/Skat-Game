from flask import Flask, jsonify

class GetAIOptions:
    @staticmethod
    def get_models():
        # Definiere die Modelle direkt hier als Liste von Dictionaries
        models = [
            {
                "name": "Easy Rule-based Bot",
                "difficulty": 1,
                "description": "Reizen: Reizt zufällig weiter oder nicht. Spielzüge: spielt zufällige valide Karte"
            },
            {
                "name": "Average Rule-based Bot",
                "difficulty": 2,
                "description": "Reizen: gewichtet nach Hand potenzial. Spielzüge: versucht jede Runde möglichst billig zu übertrumpfen/unterbieten (Nullspiel)"
            },
            {
                "name": "Hardest Rule-based Bot",
                "difficulty": 3,
                "description": "Reizen: gewichtet nach Hand potenzial und vermutung was als sinnvoll ersheint Spielzüge: Versucht Punkte pro Runde für sein Team zu maximieren"
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