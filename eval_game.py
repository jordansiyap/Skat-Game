from flask import Flask, request, jsonify
from jsonschema import validate, ValidationError
import json

app = Flask(__name__)


"""with open('schema/eval_game_input.json') as f:
    eval_game_input_schema = json.load(f)"""

@app.route('/eval_game', methods=['POST'])
def eval_game():
    # Eingabedaten validieren
    input_data = request.json

    # Wir püfen ob es in Json-Eingabe ein history und gamemode gibt.
    if 'history' not in input_data or 'gamemode' not in input_data:
        return jsonify({"error": "Invalid input data"}), 400
    
    """try:
        validate(instance=input_data, schema=eval_game_input_schema)
    except ValidationError as e:
        return jsonify({"error": "Invalid input data", "details": str(e)}), 400 """

    history = input_data['history']
    gamemode = input_data['gamemode']
    alleinspieler = gamemode.get('active_player')

    gamemode_name = gamemode.get('name') #Kreuz, Pik, Herz, Karo, Grand, Null
 
    # Bestimmen der Punkten jedes Spielers
    # Nachdem alle Rounds gespielt wurde, hier in dem dict "result" habe ich alle punkten, die jeder Spieler bekommen hat.
    #Im "result" befindet sich nur die Spielers, die mindestens einen Stich gewonnen haben, und mit ihren erreichten Punkten.
    results = {}
    for round in history['rounds']:
        winner = round['winner']
        results[winner] = results.get(winner, {'win': False, 'points': 0})
        results[winner]['points'] += round['score']

    
    # Hier habe ich die Reihenfolge für das nächste Spiel festlegen
    first_Round_Order_List = history.get('rounds')[0].get('order')
    vorhand = first_Round_Order_List.pop(0)
    first_Round_Order_List.append(vorhand) # Der Vorhand wird Hinterhand
    order_next_game = first_Round_Order_List

    #im "Player_results" befindet sich alle Spieler mit ihren erreichten Punkten, die Players, die keinen Stich gewonnen haben, bekommen 0 Punkten
    player_results = {}
    for player in history['betting_order']:
        player_results[player] = {
            "win": False,
            "points": results[player]['points'] if player in results else 0
        }
    
    # ich implementiere hier den Gewinnlogik für den Alleinspieler
    if gamemode_name == "Null":
        # Im Nullspiel gewinnt der Alleinspieler, wenn er keinen Stich macht
        player_results[alleinspieler]['win'] = all(
            not round_data['winner'] == alleinspieler for round_data in history['rounds']
        )
        if(player_results[alleinspieler]['win'] == False):
            # Die Gegenspieler gewinnen, wenn der Alleinspieler nicht gewonnen hat.
            for player in player_results:
                if player != alleinspieler:
                    player_results[player]['win'] = True

    else:
        # In Farbspielen und Grandspielen gewinnt der Alleinspieler, wenn er mindestens 61 Punkte hat
        if player_results[alleinspieler]['points'] >= 61:
            player_results[alleinspieler]['win'] = True
        else:
            # Die Gegenspieler gewinnen, wenn der Alleinspieler weniger als 61 Punkte hat
            for player in player_results:
                if player != alleinspieler:
                    player_results[player]['win'] = True

    # Die Ausgabe
    output = {
        "players": player_results,
        "order_next_game": order_next_game
    }

    return jsonify(output), 200

if __name__ == '__main__':
    app.run(debug=True)