from flask import Flask, request, jsonify
from now_using import train

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Welcome to Intelligent Gate app backend !'


@app.route('/train', methods=['GET'])
def get_prob():
    print("DEBUG : facial emotion classification API invoked")
    # pic_id = request.form['ID']

    # if pic_id == "1":
    #     return jsonify({"Emotion 1": classify_facial()})
    # elif pic_id == "2":
    #     return jsonify({"Emotion 2": classify_facial()})
    # elif pic_id == "3":
    #     return jsonify({"Emotion 3": classify_facial()})
    # else:
    a = train()
    return jsonify({"Emotion ": a})


# @app.route('/classify/text/emotion', methods=['POST'])
# def get_prob():
#     print("DEBUG : facial emotion classification API invoked")
#     text = request.form['text']
#
#     return jsonify({"Emotion " : classify_facial()})

if __name__ == '__main__':
    app.run(debug=any)
