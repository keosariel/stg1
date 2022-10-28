from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def my_info():
    return jsonify(
        {
            "slackUsername": "gabriel", 
            "backend": True, 
            "age": 19, 
            "bio": "backend developer"
        }
    )

if __name__ == '__main__':
    app.run(debug=True)