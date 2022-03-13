"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }
    return jsonify(response_body), 200

@app.route('/member/<int:user_id>', methods=['GET'])
def list_single_member(user_id):
    member = jackson_family.get_member(user_id)
    if member != "not found":
        return jsonify(member), 200
    else: 
        return jsonify('Who is that Jackson?'), 400

@app.route('/members', methods=['POST'])
def add_jackson():
    print(request.data)
    data = request.json
    print(data)
    members = jackson_family.add_member(data)
    if members == "added":
        return jsonify('The new Jackson is here to stay'), 200
    else:
        return jsonify('That guy is not a real Jackson'), 400

@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_jackson(member_id):
    members = jackson_family.delete_member(member_id)
    print(members)
    if members == "not found":
        return jsonify('This Jackson probably is already dead'), 400
    else: 
        return jsonify('R.I.P. Jackson'), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
