from flask import Flask, jsonify, request
from Logic.is_legal_move import process_legal_move_request

app = Flask(__name__)

@app.route('/get_is_legal_move', methods=['POST'])
def get_is_legal_move():
    try:
        data = request.json
        if not data:
            return jsonify(status=False, reason="No JSON body provided"), 400

        result = process_legal_move_request(data)
        return jsonify(result), (200 if result.get("status") else 400)
    except Exception as e:
        return jsonify(status=False, reason=str(e)), 

if __name__ == '__main__':
    app.run(debug=True)