from flask import request, jsonify
from app import app
import requests
import json


# ACCOUNT_ROOT = "http://ip-account-service.herokuapp.com/"
ACCOUNT_ROOT = "http://0.0.0.0:8081/"
TEXT_ROOT = "http://0.0.0.0:8082/"


@app.route('/user', methods=["GET", "POST", "PUT", "DELETE"])
def user():
    if request.method == 'GET':
        data = request.get_json()
        response = requests.get(ACCOUNT_ROOT + "user", json=data)
        response_json = response.json()
        if response_json.get('error') is True:
            return jsonify(error=True)
        return jsonify(user=response_json.get('user'), error=False)

    if request.method == 'POST':
        data = request.get_json()
        response = requests.post(ACCOUNT_ROOT + "user", json=data)
        response_json = response.json()
        if response_json.get('error') is True:
            return jsonify(error=True)
        return jsonify(authToken=response_json.get('authToken'), error=False)

    if request.method == 'PUT':
        data = request.get_json()
        response = requests.put(ACCOUNT_ROOT + "user", json=data)
        response_json = response.json()
        return jsonify(error=response_json.get('error'))

    if request.method == 'DELETE':
        data = request.get_json()
        response = requests.delete(ACCOUNT_ROOT + "user", json=data)
        response_json = response.json()
        return jsonify(error=response_json.get('error'))


@app.route('/auth', methods=["GET"])
def auth():
    data = request.get_json()
    response_json = requests.get(ACCOUNT_ROOT + "auth", json=data).json()
    if response_json.get('error'):
        return jsonify(error=True)
    return jsonify(authToken=response_json['authToken'], error=False)


@app.route('/docs', methods=["POST", "DELETE"])
def docs_route():
    if request.method == 'POST':
        data = request.get_json()
        authToken = data['authToken']
        docs = data.get('docs')
        response_json = requests.get(
            ACCOUNT_ROOT + "user_id", json={'authToken': authToken}
        ).json()
        if response_json.get('error'):
            return jsonify(error=True)
        user_id = response_json.get('userId')
        response = requests.post(
            TEXT_ROOT + "docs",
            json={'userId': user_id, 'docs': docs}
        )
        return response.text
        return jsonify(error=response.json().get('error'))

    if request.method == 'DELETE':
        data = request.get_json()
        authToken = data.get('authToken')
        response_json = requests.get(
            ACCOUNT_ROOT + "user_id", json={'authToken': authToken}
        ).json()
        if response_json.get('error'):
            return jsonify(error=True)
        userId = response_json.get('userId')
        response_json = requests.delete(TEXT_ROOT + "docs", json={'userId': userId}).json()
        return jsonify(error=response_json.get('error'))


@app.route('/doc', methods=["POST", "PUT", "DELETE"])
def doc():
    if request.method == 'POST':
        data = request.get_json()
        authToken = data.get('authToken')
        doc = data.get('doc')
        response_json = requests.get(
            ACCOUNT_ROOT + "user_id", json={'authToken': authToken}
        ).json()
        if response_json.get('error') is True:
            return jsonify(error="true")
        userId = response_json.get('userId')
        response = requests.post(
            TEXT_ROOT + "docs/" + userId,
            json={'userId': userId, 'doc': doc}
        ).json()
        # forward it:
        return jsonify(error=response.get('error'))

    if request.method == 'PUT':
        data = request.get_json()
        authToken = data.get('authToken')
        doc = data.get('doc')
        response_json = requests.get(
            ACCOUNT_ROOT + "user_id", json={'authToken': authToken}
        ).json()
        if response_json.get('error'):
            return jsonify(error="true")
        userId = response_json.get('userId')
        response = requests.put(
            TEXT_ROOT + "docs/" + userId,
            json={'userId': userId, 'doc': doc}
        ).json()
        # forward it:
        return jsonify(error=response.get('error'))

    if request.method == 'DELETE':
        data = request.get_json()
        authToken = data.get('authToken')
        doc_id = data.get('docId')
        response = requests.get(
            ACCOUNT_ROOT + "user_id",
            json={'authToken': authToken}
        ).json()
        if response.get('error'):
            return jsonify(error="true")
        userId = response.get('userId')
        response = requests.delete(
            TEXT_ROOT + "docs/" + userId,
            json={'docId': doc_id}
        ).json()
        return jsonify(error=response.get('error'))
