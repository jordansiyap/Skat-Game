from flask import Flask, jsonify, request, abort

from calculategamemodevalue import CalculateGamemodeValue
from deal import Deal
from eval_round import eval_round
from evalgamemode import EvalGamemode
from make_ai_move_medium import make_ai_move_medium

from is_legal_move import process_legal_move_request

from makeaigamemodebet import MakeAIGamemodeBet
from getgamemodes import GetGamemodes
from nextplayerbetting import NextPlayerBetting

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

@app.route('/get_is_legal_move', methods=['POST'])
def get_is_legal_move():
    try:
        data = request.json
        if not data:
            return jsonify(status=False, reason="No JSON body provided"), 400

        result = process_legal_move_request(data)
        return jsonify(result), (200 if result.get("status") else 400)
    except Exception as e:
        return jsonify(status=False, reason=str(e)), 

@app.route('/medium_make_ai_move', methods=['POST'])
def medium_make_ai_move_route():
    data = request.get_json()

    if not data or 'gamemode' not in data or 'round' not in data:
        abort(400, description="gamemode or round missing")

    gamemode = data.get('gamemode')
    round_data = data.get('round')
    hand = data.get('hand')

    if not hand:
        abort(400, description="hand missing")

    if not gamemode or 'name' not in gamemode:
        abort(400, description="gamemode does not contain name")

    if not round_data or 'order' not in round_data or 'cards' not in round_data:
        abort(400, description="round does not contain order or cards")

    gamemode_name = gamemode.get('name')
    order = round_data.get('order')
    cards = round_data.get('cards')

    valid_gamemodes = ["Kreuz", "Pik", "Herz", "Karo", "Grand", "Nullspiel"]
    if gamemode_name not in valid_gamemodes:
        abort(400, description="invalid gamemode")



    return jsonify(make_ai_move_medium(cards, gamemode_name, order, hand))

@app.route('/eval_round', methods=['POST'])
def eval_round_route():
    data = request.get_json()

    if not data or 'gamemode' not in data or 'round' not in data:
        abort(400, description="gamemode or round missing")

    gamemode = data.get('gamemode')
    round_data = data.get('round')

    if not gamemode or 'name' not in gamemode:
        abort(400, description="gamemode does not contain name")

    if not round_data or 'order' not in round_data or 'cards' not in round_data:
        abort(400, description="round does not contain order or cards")

    gamemode_name = gamemode.get('name')
    order = round_data.get('order')
    cards = round_data.get('cards')

    valid_gamemodes = ["Kreuz", "Pik", "Herz", "Karo", "Grand", "Nullspiel"]
    if gamemode_name not in valid_gamemodes:
        abort(400, description="invalid gamemode")



    round_eval = eval_round

    return jsonify(eval_round(round_eval,cards,gamemode_name ,order))

@app.route('/deal', methods=['POST']) 
def deal_route():     
    data = request.get_json()     
    if not data or 'players' not in data :         
        abort(400, description="players missing")     
        
    players_data = data['players']     
    players = []     
        
    for player in players_data:         
        players.append(player)     
    
    return jsonify(Deal.deal(players))



@app.route('/get_gamemodes',methods=["GET","POST"])
def get_gamemodes():
    return jsonify(GetGamemodes.get_gamemodes())

@app.route('/make_ai_gamemode_bet',methods=["GET","POST"])
def make_ai_gamemode_bet():
    return jsonify(MakeAIGamemodeBet.make_ai_gamemode_bet())

@app.route('/eval_gamemode',methods=["GET","POST"])
def eval_gamemode():
    return jsonify(EvalGamemode.eval_gamemode())

@app.route('/next_player_betting',methods=["GET","POST"])
def next_player_betting():
    return jsonify(NextPlayerBetting.next_player_betting())

@app.route('/calculate_gamemode_value',methods=["GET","POST"])
def calculate_gamemode_value():
    return jsonify(CalculateGamemodeValue.calculate_gamemode_value())

if __name__ == '__main__':
    app.run()