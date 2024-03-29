from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/test', methods=['POST'])
def test():
    return jsonify({"message": "Test endpoint reached successfully"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
