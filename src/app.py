"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

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

# 1) GET /members – devuelve todos los miembros
@app.route('/members', methods=['GET'])
def get_members():
    try:
        members = jackson_family.get_all_members()
        return jsonify(members), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 2) GET /member/<int:member_id> – versión singular (compat)
@app.route('/member/<int:member_id>', methods=['GET'])
def get_member_singular(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if not member:
            return jsonify({"error": "member not found"}), 404
        return jsonify(member), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 2b) GET /members/<int:member_id> – versión plural (los tests la usan)
@app.route('/members/<int:member_id>', methods=['GET'])
def get_member_plural(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if not member:
            return jsonify({"error": "member not found"}), 404
        return jsonify(member), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 3) POST /member – versión singular (compat)
@app.route('/member', methods=['POST'])
def add_member_singular():
    try:
        if not request.is_json:
            return jsonify({"error": "content-type must be application/json"}), 400
        payload = request.get_json()
        created = jackson_family.add_member(payload)
        return jsonify(created), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 3b) POST /members – versión plural (los tests la usan)
@app.route('/members', methods=['POST'])
def add_member_plural():
    try:
        if not request.is_json:
            return jsonify({"error": "content-type must be application/json"}), 400
        payload = request.get_json()
        created = jackson_family.add_member(payload)
        return jsonify(created), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 4) DELETE /member/<int:member_id> – versión singular (los tests suelen usar esta)
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member_singular(member_id):
    try:
        deleted = jackson_family.delete_member(member_id)
        if not deleted:
            return jsonify({"error": "member not found"}), 404
        return jsonify({"done": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#  DELETE /members/<int:member_id> – versión plural (por si acaso)
@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member_plural(member_id):
    try:
        deleted = jackson_family.delete_member(member_id)
        if not deleted:
            return jsonify({"error": "member not found"}), 404
        return jsonify({"done": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':  
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
