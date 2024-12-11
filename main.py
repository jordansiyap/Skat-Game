@app.route('/deal', methods=['POST'])
def deal_route():
    data = request.get_json()
    if not data or 'players' not in data :
        abort(400, description="players missing")

    players_data = data['players']
    players = []
    for player in players_data:
        players.append(player)


    return jsonify(deal(players))