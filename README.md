# challenge: skinny-flask

## description

This repo contains a code challenge created for a newly-graduated python developer,
to introduce them to the world of frameworks, HTTP status codes, and object-relational
mappings (ORMs). This repo is intended to be populated using Flask.

## the challenge

Build a url-shortening service (like http://bit.ly)  called "skinny" in Python 3, using the Flask
framework (http://flask.pocoo.org/), backed up by a PostgreSQL database.

The framework will be tested using using `curl` (https://curl.haxx.se/docs/manpage.html); it doesn't 
need a user interface right now, just responses. 

### data model

The data model for the service should look (something) like this:

the `slug` object (and `slugs` table) :
- `url`: a unique string/text field containing a uri : "http://a.long.company.com/this/is/some/deep/nesting"
- `slug`: a unique string/text field containing a short string to be used as the slug : "1ab2"
- `id`: an auto-incrementing integer containing the slug's unique identifier : 26

the `lookup` object (and `lookups` table) should have (something like) the following:
- `slug_id`: an integer field containing the id field of a slug object : 26
- `ip_address`: a string/text field containing the IP address of the client making the lookup request : "4.4.4.8"
- `referrer`: a string/text field containing the URL referring the link :
  "http://referrer.com/page"
- `when`: a timestamp field containing the time the client made the request

The shortening service should be able to do the following, in concept (and
assuming the domain name for the service is (http://skinny.dev):

### response should be JSON

all response bodies should be formatted using JSON.

### feature: submitting a url

a client can submit a url to the service via a POST request and receive a slug that can later be used to look up
that url.

```curl
$ curl -v --data "url=http://some.really.long.url.com/this/is/a/path/to/a/resource" http://skinny.dev/

> POST / HTTP/1.1
> Host: skinny.dev
> User-Agent: curl/7.49.1
> Accept: */*
>
< HTTP/1.1 201 Created
{ "location": "http://skinny.dev/1b325ac" }

```

1. if the url already exists in the service's data, it returns the existing
   lookup url (http://skinny.dev/:slug) with an HTTP status code of 200 (OK).
1. if the url does not exist, a new short 'slug' (`a2b3` above) is generated,
   and the url and slug are recorded in the database. This returns with an HTTP
   status code of 201 (Created) and uncludes the lookup url.
1. if the url submitted is poorly formed or does not exist, the server returns a
   response with an HTTP status code of 400 (Bad Request), and an error message.

### feature: retrieving a url from a slug

a client can lookup a url from the slug by submitting a GET request to the
service with the slug in the url.

```curl
$ curl --get http://skinny.dev/a2b3

> GET /a2b3 HTTP/1.1
> Host: skinny.dev
> Location: http://some.really.long.url.com/this/is/a/path/to/a/resource
> User-Agent: curl/7.49.1
> Accept: */*
>
< HTTP/1.1 403 Moved Permanently
```

1. if the slug is found, it responds with a status code of 301, and the full url
   ("http://some.really.long.url.com/this/is/a/path/to/a/resource") in the
   `Location:` field of the response header. in this case, a new `lookup` is
   created with information from the request.
1. if the slug is not found, it responds with a status code of 404.

### feature: retrieving status on a slug

the user should be able to get stats on the slug, via a GET request to
`http://skinny.dev/stats/:slug`

```curl
$ curl --get http://skinny.dev/stats/a2b3

> GET /stats/a2b3 HTTP/1.1
> Host: skinny.dev
> Location: http://some.really.long.url.com/this/is/a/path/to/a/resource
> User-Agent: curl/7.49.1
> Accept: */*
>
< HTTP/1.1 200 OK

{ "lookups": 25 }
```
1. if the slug is found, return the creation time and number of times the slug
   has been looked up with a status code of 200 (OK). (e.g., how many lookups
   are associated with the slug.)
1. if the slug is not found, respond with a status code 404 (Not Found)

## getting started

to get started, `fork` this repository, then `clone` onto your local machine. a
Flask project has already been created (very bare bones!). define the routes;
fill in the logic behind the routes, then the data storage via a connection to
PostgreSQL.

run this project with `python skinny.py`

check in your work regularly, and let me (@bvandgrift) know if you have any
questions or need any help.

good luck!
