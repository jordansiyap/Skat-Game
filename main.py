from flask import Flask

from calculate_bids import Calculate_Bids

app = Flask(__name__)

@app.route('/calculate_bids',methods=["GET"])
def calculate_bids():
    utily_obj = Calculate_Bids()
    return utily_obj.calculate_bids()

if __name__ == '__main__':
    app.run()