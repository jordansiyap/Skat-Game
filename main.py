from flask import Flask, jsonify

from makeaigamemodebet import MakeAIGamemodeBet
from makeaigamemodedecision import MakeAIGaemodeDecision

app = Flask(__name__)

@app.route('/make_ai_gamemode_bet',methods=["GET"])
def make_ai_gamemode_bet():
    return jsonify(MakeAIGamemodeBet.make_ai_gamemode_bet())

@app.route('/make_ai_gamemode_decision',methods=["GET"])
def make_ai_gamemode_decision():
    return jsonify(MakeAIGaemodeDecision.get_gamemode_decision())

if __name__ == '__main__':
    app.run()