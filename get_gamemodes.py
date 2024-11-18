from flask import Flask

app = Flask(__name__)

@app.route('/get_gamemodes',methods=['GET'])

#Wiedergabe aller Spielarten
#Die Methode definiert die von der Skat-KI angebotenen Spielarten Null, Farbspiel und Grand zu Informationszwecken.
#Die Methode soll keine Informationen über die aktuell gespielte Spielart liefern.
def get_gamemodes():
    valid_gamesmodes = [
        {"name": "Null", "active_player": "player0"},
        {"name": "Kreuz", "active_player": "player0"},
        {"name": "Pik", "active_player": "player0"},
        {"name": "Herz", "active_player": "player0"},
        {"name": "Karo", "active_player": "player0"},
        {"name": "Grand", "active_player": "player0"},
    ]
    return valid_gamesmodes

if __name__ == '__main__':
    app.run()