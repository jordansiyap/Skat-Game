from deal import Deal
from Logic import eval_round
from next_player_betting import NextPlayerBetting
from getgamemodes import GetGamemodes
from makeaigamemodebet import MakeAIGamemodeBet
from evalgamemode import EvalGamemode
from calculategamemodevalue import CalculateGamemodeValue
# from makeaimove import make_ai_move

# from Learnbased_AI_Ausspielen.easyAI import RLeasy
# from Learnbased_AI_Ausspielen.mediumAI import RLmedium
# from Learnbased_AI_Ausspielen.hardAI import RLhard

from Learnbased_betting.rleasy import RLEasy
from Learnbased_betting.rlhard import RLHard
from Learnbased_betting.rlmedium import RLMedium


agent_easy = RLEasy()
agent_medium = RLMedium()
agent_hard = RLHard()

# easyAI = RLeasy()
# mediumAI = RLmedium()
# hardAI = RLhard()

if __name__ == '__main__':

    """
    ---------------------------------------------
    |        Configure AI difficulty here       |
    ---------------------------------------------
    """
    ##difficulty of AI determining which card to play
    ##0 = easy, 1 = medium, 2 = hard
    ai_option = 2

    ##difficulty of AI handling betting
    # "easy","medium","hard"
    ai_model = "Easy Rule-based Bot"     #"RL Bot (Weakest)"
    """
    ---------------------------------------------
    """


    # Initialisierung der Variablen und Spieler
    current_player1_Hand = 0
    current_player2_Hand = 0
    current_player3_Hand = 0
    current_betting_order = ["Player1", "Player2", "Player4"]  # Reihenfolge der Spieler im Spiel
    Players_bots = ["Player1", "Player2", "Player4"]
    skat = 0


    rest_player_in_betting = 0
    previous_bets = []  # Vorherige Gebote
    current_gamemode = []  # Aktueller Modus
    selected_gamemode = 0
    actual_gamemode = 0
    currentplayer = 0
    anspieler = 0
    currenthighestpoints = 0

    rounds_played = 0
    nullspiel_lost = False
    ##currently history makes no sense betting order is included in individual rounds it being outside of "rounds" as a single entity not an array is pointless
    history = {"rounds": [],
               "betting_order": current_betting_order}

    players = ["Player1", "Player2", "Player4"]

    # Instanziiere Deal und rufe die Methode auf
    deal_instance = Deal()
    result = Deal.deal(players)

    # Ergebnisse in Variablen speichern
    current_player1_Hand = result["hands"]["Player1"]
    current_player2_Hand = result["hands"]["Player2"]
    current_player3_Hand = result["hands"]["Player4"]
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
        if current_better_reizen == "Player1":  # <- Markierung: "Player1" anstelle von "player1"
            input_data_get_gamemode = {
                "hand": current_player1_Hand,
                "player": current_better_reizen,
                "previous_bets": previous_bets,
                "players": current_betting_order
            }
        elif current_better_reizen == "Player2":
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
        # getgamemodes_output_data = GetGamemodes.get_gamemodes(input_data_get_gamemode)
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
        #getgamemodes irrelevant für bots
        # for index, gamemode in enumerate(getgamemodes_output_data["gamemodes"], start=0):
        #     print(f"{index}. {gamemode['name']} (betting: {gamemode['betting']})")

        # highest_priority = max(gamemode['betting'] for gamemode in getgamemodes_output_data["gamemodes"])
        # Eingabeaufforderung für den Benutzer
        currenthighestpoints = 17
        better_is_ki = current_better_reizen.lower() in [bot.lower() for bot in
                                                         Players_bots]  # <- Überprüfen, ob aktueller Spieler KI ist

        if not better_is_ki:  # <- Markierung: Konsoleneingabe nur für Player1
            while True:
                auswahl = input("Wähle einen Spielmodus aus (Gib den Namen ein): ").strip()
                selected_gamemode = None
                # for gamemode in getgamemodes_output_data["gamemodes"]:
                #     if gamemode['name'].lower() == auswahl.lower():
                #         print("legaler modus")
                #         selected_gamemode = gamemode
                #         break
                if selected_gamemode is None:
                    print("kein valider Modus, du bist raus")
                try:
                    auswahl = int(
                        input("Wähle einen rizwert aus der höher als der letzte ist bei kleinerer zahl bist du raus"))
                    # if auswahl > highest_priority:
                    #     print("\n\n\n\ngefahr zu überreizen aber möglich")
                    #     break
                    # elif auswahl > currenthighestpoints:
                    #     print("du hast gereizt", auswahl)
                    #     break
                    # else:
                    #     print("zu gering gereizt du bist raus")
                except ValueError:
                    print("Ungültige Eingabe. Bitte gib eine Zahl ein.")
        else:  # <- KI-Aktion bei anderen Spielern
            input_make_ai_bet = {
                "ai_model": ai_model,
                "hand": current_player1_Hand if current_better_reizen == "Player1" else (
                    current_player2_Hand if current_better_reizen == "Player2" else current_player3_Hand
                ),
                "order": current_betting_order,
                "players": current_betting_order,
                "previous_bets": previous_bets
            }
            make_ai_bet_output = MakeAIGamemodeBet.make_ai_gamemode_bet(input_make_ai_bet,agent_easy, agent_medium,agent_hard)

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

        # current_gamemode = getgamemodes_output_data["gamemodes"]
        print(next_player_betting_inputt)
        if "player" in next_player_betting_inputt and "gamemode" in next_player_betting_inputt:
            # Füge das Dictionary zu previous_bets hinzu
            previous_bets.append({
                "player": next_player_betting_inputt["player"],
                **next_player_betting_inputt["gamemode"] 
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
    input_data_eval_gamemode = {
        "previous_bets": previous_bets,
        "ai_model": ai_model,
        "player_hands": {
            "player1":
                current_player1_Hand
            ,
            "player2":
                current_player2_Hand
            ,
            "player4":
                current_player3_Hand
            ,
            "skat":
                skat
        },
        "player": currentplayer
    }

    print(input_data_eval_gamemode)
    output_data_eval_gamemode = EvalGamemode.eval_gamemode(input_data_eval_gamemode,agent_easy,agent_medium,agent_hard)

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

    selected_gamemode = output_data_eval_gamemode.get("gamemode")
    selected_firstplayer = output_data_eval_gamemode.get("player_order_next_round")
    print("\n\n\n\ninput eval gamode3", input_data_eval_gamemode)
    print("\n\n\n\noutput4", output_data_eval_gamemode)

    if "Player1" in selected_firstplayer:
        currentplayer = current_player1_Hand
    if "Player2" in selected_firstplayer:
        currentplayer = current_player2_Hand
    if "Player4" in selected_firstplayer:
        currentplayer = current_player3_Hand

    input_calculate_gamemode = {
        "hand": currentplayer,
        "gamemode": {
            "name": "Null"
        },
        "skatbool": True,  # fehlt player choice spieler ja nein frage stellen will er skat ja/nein
        "previous_bets": previous_bets
    }
    output_calculate_gamemode = CalculateGamemodeValue.calculate_gamemode_value(input_calculate_gamemode)

    # output_calculate_gamemode = [
    #     {
    #         "selected_gamemode": selected_gamemode,
    #         "player_order_next_round": ["player0", "player1", "player2"]
    #     }
    # ]
    print("\n\n\n\ninput_calculate_gamemode", input_calculate_gamemode)
    print("\n\n\n\noutput_calculate_gamemode", output_calculate_gamemode)
    print("reizen klappt")

    anspieler = output_calculate_gamemode.get("player_order_next_round")[0]
    current_betting_order = output_calculate_gamemode.get("player_order_next_round")
    print("\n\n\n\n", anspieler)
    actual_gamemode = output_calculate_gamemode["selected_gamemode"]["gamemode"]

    while rounds_played < 10:
        rounds_played += 1

        open_round = {
            "order": current_betting_order,
            "cards": {}
        }
        player_0_make_ai_move_input = {
            "ai_model": ai_option,
            "open_round": open_round,
            "gamemode": actual_gamemode,
            "hand": current_player1_Hand,
            "history": history
        }
        player_1_make_ai_move_input = {
            "ai_model": ai_option,
            "open_round": open_round,
            "gamemode": actual_gamemode,
            "hand": current_player2_Hand,
            "history": history
        }
        player_2_make_ai_move_input = {
            "ai_model": ai_option,
            "open_round": open_round,
            "gamemode": actual_gamemode,
            "hand": current_player3_Hand,
            "history": history
        }

        for player in current_betting_order:
            ## played_card = make_ai_move["play_card"]
            played_card = None
            """
            output_schema
            "play_card": {"$ref": "base_schemas/cards"}
            """
            if player == "Player0":
                played_card = make_ai_move(player_0_make_ai_move_input)["play_card"]
                """
                make_ai_move aufruf using player 0 data
                """
                current_player1_Hand.remove(played_card)
            elif player == "Player1":
                x = 5
                played_card = make_ai_move(player_1_make_ai_move_input)["play_card"]
                """
                make_ai_move aufruf using player 1 data
                """
                current_player2_Hand.remove(played_card)
            else:
                played_card = make_ai_move(player_2_make_ai_move_input)["play_card"]
                """
                make_ai_move aufruf using player 2 data
                """
                current_player3_Hand.remove(played_card)
            open_round["cards"][player] = played_card
            print(player, played_card)

        eval_round_input = {
            "gamemode": actual_gamemode,
            "round": open_round,
        }
        eval_round_instance = eval_round()
        card_data = open_round["cards"]
        order_data = open_round["order"]
        gamemode_name = actual_gamemode["name"]
        eval_round_output = eval_round_instance.eval_round(card_data, gamemode_name, order_data)

        history["rounds"].append(eval_round_output["round"])
        print("\n\n")
        print(rounds_played)
        print(eval_round_output["round"])
        print("\n\n")

        winner = eval_round_output["round"]["winner"]
        score = eval_round_output["round"]["score"]

        ##should score be 0 its a nullspiel and the active player picked up the trick ->loss
        if score < 0:
            nullspiel_lost = True
            print("you lost due to picking up a trick")
            break

    eval_game_input = {
        "history": history,
        "gamemode": actual_gamemode
    }


