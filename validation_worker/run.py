from flask import Flask, request
app = Flask(__name__)

@app.route('/validate', methods=['POST'])
def validate():
    print("Validating", request.json)
    if not request.json or not 'text' in request.json:
        return {'status': 'error'}

    return {'status': 'ok', 'text': request.json['text']}

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="6666")