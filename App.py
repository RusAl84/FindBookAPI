from flask import Flask, request, jsonify
from flask_cors import CORS
import npl_process

app = Flask(__name__)
CORS(app)

@app.route('/')
def dafault_route():
    return 'find books API'

# отправка сообщений
@app.route("/find_book", methods=['POST'])
def SendMessage():
    data = request.json
    print(data)
    text = data['text']
    data = npl_process.find_book(text)
    print(data)
    return data, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
