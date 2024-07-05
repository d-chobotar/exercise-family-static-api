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
    # this is how you can use the Family datastructure by calling its methods
    response_body = jackson_family.get_all_members()
    return jsonify(response_body), 200

@app.route('/member/<int:id>', methods=['GET'])
def handle_get_member_by_id(id):
    response_body = jackson_family.get_member(id)
    status_code = 200 if 'error' not in response_body else 404
    return jsonify(response_body), status_code

@app.route('/member', methods=['POST'])
def handle_post_member():
    member = request.get_json()
    new_member_response = jackson_family.add_member(member)
    return jsonify(new_member_response), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def handle_delete_member(id):
    delete_member_response = jackson_family.delete_member(id)
    return jsonify(delete_member_response), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
