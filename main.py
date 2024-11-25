from flask import Flask

#from calculate_bids import Calculate_Bids
from make_ai_gamemode_bet import Make_AI_Gamemode_Bet

app = Flask(__name__)

#@app.route('/calculate_bids',methods=["GET"])
#def calculate_bids():
#    utily_obj = Calculate_Bids()
#   return utily_obj.calculate_bids()

@app.route('/make_ai_gamemode_bet',methods=["GET"])
def make_ai_gamemode_bet():
    utily_obj = Make_AI_Gamemode_Bet()
    return utily_obj.make_ai_gamemode_bet()

if __name__ == '__main__':
    app.run()