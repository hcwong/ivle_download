from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/")
def login():
  try: 
    token_key = request.args.get("token")
    print(f"This is your token: '{token_key}'. Save it inside the env file")
    return "Success"
  except:
    abort(404)