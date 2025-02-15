from flask import request


class NextPlayerBetting:
    @staticmethod
    def next_player_betting(data):
        player_order = data.get("order")
        player = data.get("player")
        gamemode = data.get("gamemode")
        previous_bets = data.get("previous_bets")

        sagen = player_order[0]
        hören = player_order[1]
        weitersagen = player_order[2]



        if not previous_bets:
            return {"next_player": hören,"skatAufnahme": False}
        elif previous_bets[-1].get("player") == player and len(previous_bets) == 1:
            return {"next_player": hören,"skatAufnahme": False}
        elif previous_bets[-1].get("player") == player and len(previous_bets) > 1:
            bet = previous_bets[-1]
            bet_before = previous_bets[-2]
        elif previous_bets[-1].get("player") != player:
            try:
                if gamemode.get("active_player") == "player":
                    bet = gamemode
                    bet_before = previous_bets[-1]
            except:
                return {"error message": "cant decide who did the last bid"}
        else:
            return {"error message": "cant decide who did the last bid"}
        gamemode_name = bet.get("gamemode",{}).get("name")
        if player == sagen:
            if gamemode_name == "Raise":
                return {"next_player": hören,"skatAufnahme": False}
            elif gamemode_name == "Check":
                return {"next_player": weitersagen,"skatAufnahme": False}
            elif gamemode_name == "Pass":
                return {"next_player": weitersagen, "skatAufnahme": True}
        elif player == hören:
            if gamemode_name == "Raise":
                return {"error message": "invalid previous betting order at -hören-"}
            elif gamemode_name == "Check":
                if bet_before.get("player") == sagen:
                    return {"next_player": sagen, "skatAufnahme": False}
                elif bet_before.get("player") == weitersagen:
                    return {"next_player": weitersagen, "skatAufnahme": False}
                else:
                    return {"error message": "failure during check who continues at Step -hören-"}
            elif gamemode_name == "Pass":
                return {"next_player": weitersagen, "skatAufnahme": False}
        elif player == weitersagen:
            if gamemode_name == "Raise":
                if bet_before.get("player") == sagen:
                    return {"next_player": sagen, "skatAufnahme": False}
                elif bet_before.get("player") == hören:
                    return {"next_player": hören, "skatAufnahme": False}
                else:
                    return {"error message": "failure during check who continues at Step -weitersagen-"}
            elif gamemode_name == "Check":
                return {"error message": "invalid previous betting order at -weitersagen-"}
            elif gamemode_name == "Pass":
                if bet_before.get("player") == sagen:
                    return {"next_player": sagen, "skatAufnahme": True}
                elif bet_before.get("player") == hören:
                    if bet_before.get("name") == "Pass":
                        return {"next_player": sagen, "skatAufnahme": True}
                    else:
                        return {"next_player": hören, "skatAufnahme": True}
                else:
                    return {"error message": "failure during check who continues at Step -weitersagen-"}
        else:
            return {"error message": "invalid player input"}

    @staticmethod
    def next_player(player_order,previous_bets):
        sagen = player_order[0]
        hören = player_order[1]
        weitersagen = player_order[2]

        if len(previous_bets) == 1:
            return {"next_player": hören, "skatAufnahme": False}
        else:
            bet = previous_bets[-1]
            player = previous_bets[-1].get("player")
            bet_before = previous_bets[-2]
            gamemode_name = bet.get("gamemode",{}).get("name")
            if player == sagen:
                if gamemode_name == "Raise":
                    return {"next_player": hören, "skatAufnahme": False}
                elif gamemode_name == "Check":
                    return {"next_player": weitersagen, "skatAufnahme": False}
                elif gamemode_name == "Pass":
                    return {"next_player": weitersagen, "skatAufnahme": True}
            elif player == hören:
                if gamemode_name == "Raise":
                    return {"error message": "invalid previous betting order at -hören-"}
                elif gamemode_name == "Check":
                    if bet_before.get("player") == sagen:
                        return {"next_player": sagen, "skatAufnahme": False}
                    elif bet_before.get("player") == weitersagen:
                        return {"next_player": weitersagen, "skatAufnahme": False}
                    else:
                        return {"error message": "failure during check who continues at Step -hören-"}
                elif gamemode_name == "Pass":
                    return {"next_player": weitersagen, "skatAufnahme": False}
            elif player == weitersagen:
                if gamemode_name == "Raise":
                    if bet_before.get("player") == sagen:
                        return {"next_player": sagen, "skatAufnahme": False}
                    elif bet_before.get("player") == hören:
                        return {"next_player": hören, "skatAufnahme": False}
                    else:
                        return {"error message": "failure during check who continues at Step -weitersagen-"}
                elif gamemode_name == "Check":
                    return {"error message": "invalid previous betting order at -weitersagen-"}
                elif gamemode_name == "Pass":
                    if bet_before.get("player") == sagen:
                        return {"next_player": sagen, "skatAufnahme": True}
                    elif bet_before.get("player") == hören:
                        if bet_before.get("name") == "Pass":
                            return {"next_player": sagen, "skatAufnahme": True}
                        else:
                            return {"next_player": hören, "skatAufnahme": True}
                    else:
                        return {"error message": "failure during check who continues at Step -weitersagen-"}
            else:
                return {"error message": "invalid player input"}