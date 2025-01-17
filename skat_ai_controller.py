from flask import Flask, jsonify, request, abort

from Rulebased_Betting.calculategamemodevalue import CalculateGamemodeValue
from Logic.deal import Deal
from Logic.eval_game import EvalGame
from Logic.eval_round import EvalRound
from Rulebased_Betting.evalgamemode import EvalGamemode
from Logic.get_ai_options import GetAIOptions

from Logic.is_legal_move import IsLegalMove

from Rulebased_Betting.makeaigamemodebet import MakeAIGamemodeBet
from Rulebased_Betting.getgamemodes import GetGamemodes
from Rulebased_Playing.makeaimove import MakeAIMove
from Rulebased_Betting.nextplayerbetting import NextPlayerBetting

app = Flask(__name__)

@app.route('/get-ai-options', methods=['GET','POST'])
def get_models():
    return GetAIOptions.get_models()

@app.route('/is-legal-move', methods=['GET','POST'])
def get_is_legal_move():
    try:
        data = request.json
        if not data:
            return jsonify(status=False, reason="No JSON body provided"), 400

        result = IsLegalMove.process_legal_move_request(data)
        return jsonify(result), (200 if result.get("status") else 400)
    except Exception as e:
        return jsonify(status=False, reason=str(e)),

@app.route('/eval-round', methods=['GET','POST'])
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

    valid_gamemodes = ["Kreuz", "Pik", "Herz", "Karo", "Grand", "Null"]
    if gamemode_name not in valid_gamemodes:
        abort(400, description="invalid gamemode")

    return jsonify(EvalRound.eval_round(cards,gamemode_name ,order))

@app.route('/deal', methods=['GET','POST'])
def deal_route():     
    data = request.get_json()     
    if not data or 'players' not in data :         
        abort(400, description="players missing")     
        
    players_data = data['players']     
    players = []     
        
    for player in players_data:         
        players.append(player)     
    
    return jsonify(Deal.deal(players))



@app.route('/get-gamemodes',methods=["GET","POST"])
def get_gamemodes():
    return jsonify(GetGamemodes.get_gamemodes())

@app.route('/make_ai-gamemode-bet',methods=["GET","POST"])
def make_ai_gamemode_bet():
    return jsonify(MakeAIGamemodeBet.make_ai_gamemode_bet())

@app.route('/eval-gamemode',methods=["GET","POST"])
def eval_gamemode():
    return jsonify(EvalGamemode.eval_gamemode())

@app.route('/next-player-betting',methods=["GET","POST"])
def next_player_betting():
    return jsonify(NextPlayerBetting.next_player_betting())

@app.route('/calculate-gamemode-value',methods=["GET","POST"])
def calculate_gamemode_value():
    return jsonify(CalculateGamemodeValue.calculate_gamemode_value())

@app.route('/eval-game', methods=['GET','POST'])
def eval_game():
    return jsonify(EvalGame.eval_game())

@app.route('/make-ai-move', methods=['GET','POST'])
def make_ai_move():
    return MakeAIMove.make_ai_move()

if __name__ == '__main__':
    app.run()