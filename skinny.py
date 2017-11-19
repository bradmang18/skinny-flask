from datetime import datetime
from flask import Flask, request, make_response
from hashlib import md5
import json
from pony.orm import Database, Required, Set, db_session, desc

# Constants
MIN_SLUG_LENGTH = 4

skinny = Flask(__name__)

# Connect to database
db = Database()
db.bind(provider='postgres', user='skinny_flask', password='skinny_flask', host='localhost', database='skinny_flask')


# Entities
class Slug(db.Entity):
    url = Required(str, unique=True)
    slug = Required(str, unique=True)
    lookups = Set(lambda: Lookup)


class Lookup(db.Entity):
    slug = Required(Slug)
    ip_address = Required(str)
    referrer = Required(str)
    when = Required(datetime)


# Generate tables if they do not exist
db.generate_mapping(create_tables=True)


# Routes
@skinny.route('/', methods=['POST'])
def submit():
    with db_session:
        url = request.form['url'].lower()

        slug = Slug.select(lambda s: s.url == url).first()
        if slug is None:
            slug = Slug(url=url, slug=slugify(url))
            code = 201
        else:
            code = 200

        Lookup(ip_address=request.remote_addr, referrer=request.referrer, when=datetime.utcnow(), slug=slug)

        return make_response((json.dumps({'location': 'http://skinny.dev/' + slug.slug}), code, {'Content-Type': 'application/json'}))


@db_session
@skinny.route('/<slug>', methods=['GET'])
def lookup(slug):
    return


@db_session
@skinny.route('/stats/<slug>', methods=['GET'])
def stats(slug):
    return


# Helper functions
def slugify(url):
    hasher = md5()
    hasher.update(url.encode())
    url_hash = hasher.hexdigest()

    existing_slug = Slug.select(lambda s: s.slug.startswith(url_hash[:MIN_SLUG_LENGTH])).order_by(lambda s: desc(len(s.slug))).first()

    if existing_slug is None:
        return url_hash[:MIN_SLUG_LENGTH]
    else:
        return url_hash[:len(existing_slug.slug) + 1]


# Run the app
if __name__ == '__main__':
    skinny.run()
