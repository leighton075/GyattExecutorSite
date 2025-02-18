from flask import Flask, render_template, request, jsonify
import re
import tokenize
from io import StringIO
import uwuify
import untokenize

app = Flask(__name__)

gyatt_slang = {
    "rizz": "None",
    "cap": "False",  
    "nocap": "True",  
    "btw": "and",
    "like": "as",
    "skibidi": "assert",
    "stawp": "break",
    "period": "continue",
    "gyatt": "def",
    "hawktuah": "elif",
    "tuah": "else",
    "boom": "except",
    "frfr": "finally",
    "iveplayedthesegamesbefore": "for",
    "aldi": "from",
    "hawk": "if",
    "propertyinegypt": "import",
    "be": "==",
    "huzz": "lambda",
    "nogatekeep": "nonlocal",
    "nogatekeepfrfr": "global",
    "aint": "not",
    "idk": "or",
    "idc": "pass",
    "lowtaperfade": "raise",
    "yeet": "return",
    "choppedchin": "try",
    "yapuntil": "while",
    "chill": "yield",
    "nerd": "math",
    "finna": "=",
    "rn": "",
    "tho": "\abcdefgh:",  
    "sigma": "+",
    "times": "range",
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute_gyatt():
    data = request.get_json()
    gyatt_code = data.get('code', '')

    if not gyatt_code:
        return jsonify({"error": "No code provided"}), 400

    try:
        output = execute(gyatt_code)
        return jsonify({"output": output})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def execute(gyatt_code):
    # Replace Gyatt slang with Python code
    gyatt_code = gyatt_code.replace("aint be", "!=")
    gyatt_code = gyatt_code.replace("skibidi?", "skibidi")
    
    tokens = list(tokenize.generate_tokens(StringIO(gyatt_code).readline))
    python_code = ""

    for i, token in enumerate(tokens):
        for slang, replacement in gyatt_slang.items():
            if token.string == slang:
                tokens[i] = (token[0], replacement, token[2], token[3], token[4])

    python_code = untokenize.untokenize(tokens)
    python_code = python_code.replace(" \abcdefgh:", ":")  # Handle non-code replacements

    try:
        # Execute the Python code and capture the output
        exec(python_code)
        return "Executed Successfully"
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
