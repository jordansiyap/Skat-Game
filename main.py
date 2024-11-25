from flask import Flask
from get_gamemodes import Get_Gamemodes

app = Flask(__name__)

@app.route('/get_gamemodes',methods=["GET"])
def get_gamemodes():
    utily_obj = Get_Gamemodes()
    return utily_obj.get_gamemodes()

if __name__ == '__main__':
    app.run()