from flask import Flask
from getgamemodes import GetGamemodes

app = Flask(__name__)

@app.route('/get_gamemodes',methods=["GET"])
def get_gamemodes():
    return GetGamemodes.get_gamemodes()

if __name__ == '__main__':
    app.run()