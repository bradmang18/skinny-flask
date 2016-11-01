from flask import Flask
import json

skinny = Flask(__name__)

@skinny.route("/", methods = ['GET'])
def default_route():
    return json.dumps({"message": "welcome!"})

if __name__ == "__main__":
    skinny.run()
