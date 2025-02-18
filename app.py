from flask import Flask, render_template, request, jsonify
import re
from io import StringIO
import sys
from contextlib import redirect_stdout

app = Flask(__name__)

# Dictionary mapping Gyatt slang to Python keywords and operators
GYATT_SLANG = {
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
    "tho": ":",
    "sigma": "+",
    "times": "range"
}

def translate_gyatt_to_python(gyatt_code):
    """Translate Gyatt code to Python code."""
    python_code = gyatt_code
    
    # Replace multi-character operators first
    python_code = python_code.replace("aint be", "!=")
    
    # Replace all other Gyatt terms
    for slang, replacement in GYATT_SLANG.items():
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(slang) + r'\b'
        python_code = re.sub(pattern, replacement, python_code)
    
    return python_code

def execute_python_code(python_code):
    """Execute Python code and capture output."""
    output = StringIO()
    error = None
    
    try:
        # Redirect stdout to capture print statements
        with redirect_stdout(output):
            # Create a new dictionary for local variables
            local_dict = {}
            # Execute the code in a restricted environment
            exec(python_code, {"__builtins__": __builtins__}, local_dict)
        
        # Get the captured output
        execution_output = output.getvalue()
        return execution_output if execution_output else "Code executed successfully (no output)"
    except Exception as e:
        error = f"Error: {str(e)}"
        return error

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute_gyatt():
    try:
        data = request.get_json()
        gyatt_code = data.get('code', '').strip()
        check_only = data.get('check_only', False)
        
        if not gyatt_code:
            return jsonify({"error": "No code provided"}), 400
        
        # Translate Gyatt code to Python
        try:
            python_code = translate_gyatt_to_python(gyatt_code)
        except Exception as e:
            return jsonify({"error": f"Translation error: {str(e)}"}), 400
            
        # If we're just checking for errors, try to compile the code
        if check_only:
            try:
                compile(python_code, '<string>', 'exec')
                return jsonify({"status": "valid"})
            except Exception as e:
                return jsonify({"error": str(e)}), 400
        
        # Otherwise execute the code
        output = execute_python_code(python_code)
        return jsonify({
            "output": output,
            "python_code": python_code
        })
    
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)