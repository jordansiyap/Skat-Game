from flask import Flask

from makeaigamemodebet import MakeAIGamemodeBet

app = Flask(__name__)

@app.route('/make_ai_gamemode_bet',methods=["GET"])
def make_ai_gamemode_bet():
    return MakeAIGamemodeBet.make_ai_gamemode_bet()

if __name__ == '__main__':
    app.run()