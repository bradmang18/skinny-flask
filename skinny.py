from flask import Flask, make_response, request
import json, hashlib

skinny = Flask(__name__)

url_store = {}
slug_store = {}
lookup_store = {}
hash_length = 5

@skinny.route("/", methods = ['GET', 'POST'])
def default_route():
    if request.method == 'POST':
        url = request.form['url']
        if url in url_store:
            return json_url(url_store[url])
        else:
            sl = dig(url)

            # let's deal with hash collisions
            store(url, sl)
            return json_url(sl)
    else:
        return json.dumps({"message": "welcome!"})

@skinny.route("/<slug>", methods = ['GET'] )
def get_slug(slug):
    resp = make_response()
    if slug in slug_store:
        resp.status_code = 301
        resp.headers['Location'] = slug_store[slug]
        lookup_slug(slug)
    else:
        resp.status_code = 404
    return resp

@skinny.route("/stats/<slug>", methods = ['GET'])
def get_stats(slug):
    if slug in lookup_store:
        return json.dumps({"lookups": lookup_store[slug]})
    else:
        resp = make_response()
        resp.status_code = 404
        return resp

#####################
# helper methods

# we want to update both of these
# at the same time
def store(url, sl):
    url_store[url] = sl
    slug_store[sl] = url

def json_url(slug):
    return json.dumps({"location": "http://skinny.dev/{}".format(slug)})

# digest this string and check for backoff
def dig(st):
    h = hashlib.md5()
    h.update(st.encode('utf-8'))
    d =  h.hexdigest()

    # stretch the digest if already present
    offset = 0
    while(d[:(hash_length + offset)] in slug_store):
        offset += 1
        # ignoring the limit here entirely
    return d[:(hash_length + offset)]

def lookup_slug(sl):
    if sl in lookup_store:
        lookup_store[sl] += 1
    else:
        lookup_store[sl] = 1

if __name__ == "__main__":
    skinny.run()
