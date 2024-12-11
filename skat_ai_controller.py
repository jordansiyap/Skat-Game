from flask import Flask, jsonify

from deal import Deal

from makeaigamemodebet import MakeAIGamemodeBet
from makeaigamemodedecision import MakeAIGaemodeDecision
from getgamemodes import GetGamemodes

app = Flask(__name__)

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
    
    return jsonify(deal(players))



@app.route('/get_gamemodes',methods=["GET"])
def get_gamemodes():
    return jsonify(GetGamemodes.get_gamemodes())

@app.route('/make_ai_gamemode_bet',methods=["GET"])
def make_ai_gamemode_bet():
    return jsonify(MakeAIGamemodeBet.make_ai_gamemode_bet())

@app.route('/make_ai_gamemode_decision',methods=["GET"])
def make_ai_gamemode_decision():
    return jsonify(MakeAIGaemodeDecision.get_gamemode_decision())

if __name__ == '__main__':
    app.run()