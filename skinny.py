from flask import Flask

skinny = Flask(__name__)

@skinny.route('/', methods=['POST'])
def submit():
    return

@skinny.route('/<slug>', methods=['GET'])
def lookup(slug):
    return

@skinny.route('/stats/<slug>', methods=['GET'])
def stats(slug):
    return

if __name__ == "__main__":
    skinny.run()