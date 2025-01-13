from deal import Deal
from next_player_betting import NextPlayerBetting
from getgamemodes import GetGamemodes
from makeaigamemodebet import MakeAIGamemodeBet
from evalgamemode import EvalGamemode
from calculategamemodevalue import CalculateGamemodeValue

# Initialisierung der Variablen und Spieler
current_player1_Hand = 0
current_player2_Hand = 0
current_player3_Hand = 0
current_betting_order = ["Player0", "Player1", "Player2"]  # Reihenfolge der Spieler im Spiel
Players_bots = ["Player0","Player1", "Player2"]
skat = 0
ai_option = 0
rest_player_in_betting = 0
previous_bets = []  # Vorherige Gebote
current_gamemode = []  # Aktueller Modus
selected_gamemode = 0
currentplayer = 0
anspieler = 0
currenthighestpoints = 0

players = ["Player0", "Player1", "Player2"]

# Instanziiere Deal und rufe die Methode auf
deal_instance = Deal()
result = Deal.deal(players)

# Ergebnisse in Variablen speichern
current_player1_Hand = result["hands"][0]["Player0"]
current_player2_Hand = result["hands"][1]["Player1"]
current_player3_Hand = result["hands"][2]["Player2"]
current_betting_order = result["betting_order"]
skat = result["skat"]
# Setze den ersten Spieler, der das Gebot abgibt
current_better_reizen = current_betting_order[0]

# Beispiel: Eingabedaten für den aktuellen Spieler und Gebote
next_player_betting_inputt = {
    "order": current_betting_order,
    "player": current_better_reizen,
    "gamemode": current_gamemode,
    "previous_bets": previous_bets
}
next_player_betting_outputt = NextPlayerBetting.next_player_betting(next_player_betting_inputt)

# # Funktion zur Bestimmung des nächsten Spielers und Status "skatAufnahme"
# def determine_next_player(next_player_betting_inputt):
#     order = next_player_betting_inputt["order"]
#     current_player = next_player_betting_inputt["player"]

#     current_index = order.index(current_player)

#     # Bestimme den nächsten Spieler
#     next_index = (current_index + 1) % len(order)
#     next_player = order[next_index]

#     output_data = {
#         "next_player": next_player,
#         "skatAufnahme": False  # Initiale Annahme, dass der nächste Spieler skatAufnahme = True bekommt
#     }
#     return output_data

# Schleife, die so lange läuft, bis skatAufnahme = True für einen Spieler gesetzt wird
skat_aufnehmen = False

while not skat_aufnehmen:
    # Eingabedaten für get gamemodes
    if current_better_reizen == "Player0":  # <- Markierung: "Player1" anstelle von "player1"
        input_data_get_gamemode = {
            "hand": current_player1_Hand,  
            "player": current_better_reizen,  
            "previous_bets": previous_bets,  
            "players": current_betting_order 
        }
    elif current_better_reizen == "Player1":
        input_data_get_gamemode = {
            "hand": current_player2_Hand,  
            "player": current_better_reizen,  
            "previous_bets": previous_bets,  
            "players": current_betting_order 
        } 
    else:
        input_data_get_gamemode = {
            "hand": current_player3_Hand,  
            "player": current_better_reizen,  
            "previous_bets": previous_bets,  
            "players": current_betting_order 
        }    
    getgamemodes_output_data = GetGamemodes.get_gamemodes(input_data_get_gamemode)

    # Beispielausgabe der verfügbaren Spielmodi
    # getgamemodes_output_data = {
    #     "gamemodes": [
    #         {
    #             "name": "Grand",
    #             "description": "A high-stakes mode where the player must win the majority of the tricks.",
    #             "betting": "High betting value, typically leads to larger pots.",
    #             "priority": 18
    #         },
    #         {
    #             "name": "Null",
    #             "description": "A low-stakes mode where the player tries to lose the majority of the tricks.",
    #             "betting": "Low betting value, typically leads to smaller pots.",
    #             "priority": 10
    #         },
    #         # Weitere Spielmodi hinzufügen
    #     ]
    # }
    
    for index, gamemode in enumerate(getgamemodes_output_data["gamemodes"], start=0):
        print(f"{index}. {gamemode['name']} (betting: {gamemode['betting']})") 

    highest_priority = max(gamemode['betting'] for gamemode in getgamemodes_output_data["gamemodes"])
    # Eingabeaufforderung für den Benutzer
    currenthighestpoints = 17
    better_is_ki = current_better_reizen.lower() in [bot.lower() for bot in Players_bots]  # <- Überprüfen, ob aktueller Spieler KI ist

    if not better_is_ki:  # <- Markierung: Konsoleneingabe nur für Player1
        while True:
            auswahl = input("Wähle einen Spielmodus aus (Gib den Namen ein): ").strip()
            selected_gamemode = None
            for gamemode in getgamemodes_output_data["gamemodes"]:
                if gamemode['name'].lower() == auswahl.lower():
                    print("legaler modus")
                    selected_gamemode = gamemode
                    break 
            if selected_gamemode is None:
                print("kein valider Modus, du bist raus")        
            try:
                auswahl = int(input("Wähle einen rizwert aus der höher als der letzte ist bei kleinerer zahl bist du raus"))
                if auswahl > highest_priority:
                    print("\n\n\n\ngefahr zu überreizen aber möglich")
                    break
                elif auswahl > currenthighestpoints:
                    print("du hast gereizt", auswahl)
                    break 
                else:
                    print("zu gering gereizt du bist raus")
            except ValueError:
                print("Ungültige Eingabe. Bitte gib eine Zahl ein.") 
    else:  # <- KI-Aktion bei anderen Spielern
        input_make_ai_bet = {
            "ai_model": "name",
            "hand": current_player1_Hand if current_better_reizen == "Player1" else (
                current_player2_Hand if current_better_reizen == "Player2" else current_player3_Hand
            ),
            "order": current_betting_order,
            "players": current_betting_order, 
            "previous_bets": previous_bets
        }
        make_ai_bet_output = MakeAIGamemodeBet.make_ai_gamemode_bet(input_make_ai_bet)

        # make_ai_bet_output = {
        #     "gamemode": {
        #         "name": "ai",
        #         "description": "A high-stakes mode where the player must win the majority of the tricks.",
        #         "betting": "High betting value, typically leads to larger pots.",
        #         "priority": 20
        #     }
        # }
        selected_gamemode = make_ai_bet_output
    # Nachfolgende Schritte...
    next_player_betting_inputt = {
        "order": current_betting_order,
        "player": current_better_reizen,
        "gamemode": selected_gamemode,
        "previous_bets": previous_bets
    }

    current_gamemode = getgamemodes_output_data["gamemodes"]
    print(next_player_betting_inputt)
    if "player" in next_player_betting_inputt and "gamemode" in next_player_betting_inputt:
    # Füge das Dictionary zu previous_bets hinzu
        previous_bets.append({
            "player": next_player_betting_inputt["player"],
            "gamemode": next_player_betting_inputt["gamemode"]
        })
    next_player_betting_outputt = NextPlayerBetting.next_player_betting(next_player_betting_inputt)
    next_player = next_player_betting_outputt["next_player"]
    skat_aufnehmen = next_player_betting_outputt["skatAufnahme"]
    current_better_reizen = next_player
    print("ein durchlauf")

    if skat_aufnehmen:
        print(next_player_betting_outputt)
    else:
        print(f"Spieler {next_player_betting_outputt} geht weiter.")

print("funkt alles")
input_data_eval_gamemode = [
    {
        "previous_bets": previous_bets,
        "player_hands": {
            "player0": 
                current_player1_Hand
            ,
            "player1": 
                current_player2_Hand
            ,
            "player2": 
                current_player3_Hand
            ,
            "skat": 
                skat
        }
    }
]

output_data_eval_gamemode = EvalGamemode.eval_gamemode(input_data_eval_gamemode)

# output_data_eval_gamemode = [
#     {
#         "selected_gamemode": current_gamemode,
#         "player_order_next_round": [
#             "player0",
#             "player1",
#             "player2"
#         ]
#     }
# ]

selected_gamemode = output_data_eval_gamemode[0]["selected_gamemode"]
selected_firstplayer = output_data_eval_gamemode[0].get("player_order_next_round")
print("\n\n\n\ninput eval gamode3", input_data_eval_gamemode)
print("\n\n\n\noutput4", output_data_eval_gamemode)

if "Player0" in selected_firstplayer:
    currentplayer = current_player1_Hand
if "Player1" in selected_firstplayer:
    currentplayer = current_player2_Hand
if "Player2" in selected_firstplayer:
    currentplayer = current_player3_Hand


input_calculate_gamemode = [
    {
        "hand": currentplayer,
        "gamemode": selected_gamemode,
        "skatbool": True,               #fehlt player choice spieler ja nein frage stellen will er skat ja/nein
        "previous_bets": previous_bets
    }
]
output_calculate_gamemode = CalculateGamemodeValue.calculate_gamemode_value(input_calculate_gamemode)

# output_calculate_gamemode = [
#     {
#         "selected_gamemode": selected_gamemode,
#         "player_order_next_round": ["player0", "player1", "player2"]
#     }
# ]
print("\n\n\n\ninput_calculate_gamemode", input_calculate_gamemode)
print("\n\n\n\noutput_calculate_gamemode", output_calculate_gamemode)

anspieler = output_calculate_gamemode[0]["player_order_next_round"][0]
print("\n\n\n\n",anspieler)


