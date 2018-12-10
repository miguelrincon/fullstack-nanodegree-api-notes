# Secure API notes

Sample code for implementing secure APIs using Flask and Python 3. Below, some of my notes.

## Simple approach

Using the package `flask_httpauth.HTTPBasicAuth` create a simple API authorization:

1. Registration of a new user using a `POST /users` request which stores a new user with a hashed password in the database. Hashing is done using `passlib.apps.custom_app_context`.
2. Authentication to API resources using two annotations `@auth.verify_password` and `@auth.login_required` which implement HTTP basic authentication.

## Bagels (Token based authentication)

Using the package `flask_httpauth.HTTPBasicAuth` and `itsdangerous` create a simple API flow which can provide the following:

1. Registration of a new user using a `POST` as above.
2. Generation of a token for registered users using a `GET /token` endpoint. Which generates a token based on a randomly generated secret key.
3. Authentication to APIs using two previously used annotations: `@auth.verify_password` and `@auth.login_required`, but using the token to allow access to the API.

## Rate limiting

Lkmit rate of usage of an API based on IP address.

1. For a given `remote_addr` and `endpoint` of a request, identify a single use of an API resource.
2. Use Redis and a decorator to wrap a method which defines an endpoint.  Call redis.pipeline().incr() to record the API resource usage.
1. Define an expiration window to allow for more API calls after a period of time.

### Acknowledgment 

Code based on API course on the Fullstack Nanodegree by Udacity: https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004