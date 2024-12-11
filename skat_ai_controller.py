from flask import Flask, jsonify

from makeaigamemodebet import MakeAIGamemodeBet
from makeaigamemodedecision import MakeAIGaemodeDecision
from getgamemodes import GetGamemodes

app = Flask(__name__)



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