from simple_secure_api_models import Base, User
from flask import Flask, jsonify, request, url_for, abort, g
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from flask import Flask
from flask_httpauth import HTTPBasicAuth

engine = create_engine('sqlite:///simple_secure_api.db')
auth = HTTPBasicAuth()

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

@auth.verify_password
def verify_password(username, password):
	user = session.query(User).filter_by(username = username).first()
	if not user or not user.verify_password(password):
		return False
	g.user = user
	return True

@app.route('/users', methods = ['POST'])
def new_user():
	username = request.json.get('username')
	password = request.json.get('password')
	if username is None or password is None:
		abort(400)
	if session.query(User).filter_by(username = username).first() is not None:
		abort(400)
	user = User(username = username)
	user.hash_password(password)
	session.add(user)
	session.commit()
	return jsonify({username: user.username}, 201)

@app.route('/protected_resource')
@auth.login_required
def get_resource():
	return jsonify({'data': 'Hello! %s' % g.user.username})

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)	

