from flask import Flask, jsonify, request
from jsonschema import validate, ValidationError

app = Flask(__name__)
s_name = "gabriel"

calc_schema = {
    "type": "object",
    "properties" : {
        "operation_type": {
            "type": "string",
            "enum": ["+", "-", "/", "*"]
        },
        "x":{"type": "number"},
        "y":{"type": "number"}
    },
    "required": ["operation_type", "x", "y"]
}

def validate_json(schema):
    def wrapper(func):
        def _validate(*args, **kwargs):
            if request.method == "POST":
                data = request.json
                try:
                    validate(instance=data, schema=schema)
                except ValidationError as e:
                    data = None
                kwargs.update({"json_data": data})
            return func(*args, **kwargs)
        return _validate
    return wrapper

@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/', methods=["GET", "POST"])
@validate_json(calc_schema)
def main(json_data=None):

    if request.method == "GET":
        return jsonify(
            {
                "slackUsername": s_name, 
                "backend": True, 
                "age": 19, 
                "bio": "backend developer"
            }
        )
    else:
        if json_data:
            op = json_data["operation_type"]
            eval_str = f"{json_data['x']} {op} {json_data['y']}"
            result = eval(eval_str)
            return {"slackUsername": s_name, "operation_type": op, "result": result}

if __name__ == '__main__':
    app.run(debug=True)
