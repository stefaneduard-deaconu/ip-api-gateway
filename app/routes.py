from flask import request, jsonify
from app import app
import requests


ACCOUNT_ROOT = "http://ip-account-service.herokuapp.com/"


@app.route('/user', methods=["POST", "PUT", "DELETE"])
def user():
    if request.method == 'POST':
        data = request.get_json()
        response = requests.post(ACCOUNT_ROOT + "user", json=data)
        if response['error'] is True:
            return jsonify(error=True)
        return jsonify(authToken=response['authToken'], error=False)

    if request.method == 'PUT':
        data = request.get_json()
        response = requests.put(ACCOUNT_ROOT + "user", json=data)
        return jsonify(error=response['error'])

    if request.method == 'DELETE':
        data = request.get_json()
        response = requests.delete(ACCOUNT_ROOT + "user", json=data)
        return jsonify(error=response['error'])


@app.route('/auth', methods=["POST"])
def auth():
    data = request.get_json()
    response = requests.post(ACCOUNT_ROOT + "auth", json=data)
    if response['error'] is True:
        return jsonify(error=True)
    return jsonify(authToken=response['authToken'], error=False)


@app.route('/docs', methods=["POST", "DELETE"])
def docs():
    if request.method == 'POST':
        data = request.get_json()
        authToken = data['authToken']
        docs = data['docs']
        response = requests.post(ACCOUNT_ROOT + "user", json={'authToken': authToken})
        if response['error'] is True:
            return jsonify(error=True)
        userId = response['userId']
        response = requests.post("http://ip-text-service.herokuapp.com/docs", json={'userId': userId, 'docs': docs})
        return jsonify(error=response['error'])

    if request.method == 'DELETE':
        data = request.get_json()
        authToken = data['authToken']
        response = requests.post(ACCOUNT_ROOT + "user", json={'authToken': authToken})
        if response['error'] is True:
            return jsonify(error=True)
        userId = response['userId']
        response = requests.delete("http://ip-text-service.herokuapp.com/docs", json={'userId': userId})
        return jsonify(error=response['error'])


@app.route('/doc', methods=["POST", "PUT", "DELETE"])
def doc():
    if request.method == 'POST':
        data = request.get_json()
        authToken = data['authToken']
        doc = data['doc']
        response = requests.post(ACCOUNT_ROOT + "user", json={'authToken': authToken})
        if response['error'] is True:
            return jsonify(error=True)
        userId = response['userId']
        response = requests.post("http://ip-text-service.herokuapp.com/doc", json={'userId': userId, 'doc': doc})
        if response['error'] is True:
            return jsonify(error=True)
        return jsonify(doc_id=response['doc_id'], error=False)

    if request.method == 'PUT':
        data = request.get_json()
        authToken = data['authToken']
        doc = data['doc']
        response = requests.post(ACCOUNT_ROOT + "user", json={'authToken': authToken})
        if response['error'] is True:
            return jsonify(error=True)
        userId = response['userId']
        response = requests.put("http://ip-text-service.herokuapp.com/doc", json={'userId': userId, 'doc': doc})
        return jsonify(error=response['error'])

    if request.method == 'DELETE':
        data = request.get_json()
        authToken = data['authToken']
        doc_id = data['doc_id']
        response = requests.post(ACCOUNT_ROOT + "user", json={'authToken': authToken})
        if response['error'] is True:
            return jsonify(error=True)
        userId = response['userId']
        response = requests.delete("http://ip-text-service.herokuapp.com/doc",
                                   json={'userId': userId, 'doc_id': doc_id})
        return jsonify(error=response['error'])
