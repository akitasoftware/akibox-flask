# Copyright 2021 Akita Software, Inc.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import time
import uuid

from collections import defaultdict
from flask import Flask, Response, make_response, request
from pydantic import BaseModel, parse_obj_as


class CreateUserRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str


class User(CreateUserRequest):
    id: str


class CreateUserFileRequest(BaseModel):
    contents: str


class File(BaseModel):
    id: str
    created_at: int
    contents: str


# Map user IDs to users.
users = {
  "2b9046ac-6112-11eb-ae07-3e22fb0d93ba": User(
    id="2b9046ac-6112-11eb-ae07-3e22fb0d93ba",
    first_name="Devon",
    last_name="Developer",
    email="devon@devonthedeveloper.com",

    # Tutorial: Change this to a US-formatted phone number
    #   by removing the leading "+1-".
    phone="+1-323-867-5309",
  ),
  "38c15834-6112-11eb-86fb-3e22fb0d93ba": User(
    id="38c15834-6112-11eb-86fb-3e22fb0d93ba",
    first_name="Alice",
    last_name="Adventurer",
    email="alice@adventuring.org",
    phone="+1-234-567-8901",
  )
}


# Map user IDs to maps of file IDs to files.
files = defaultdict(dict)

app = Flask(__name__)


@app.route("/users", methods=['GET', 'POST'])
def handle_users():
    if request.method == 'GET':
        return { "users": [u.dict() for u in users.values()] }
    elif request.method == 'POST':
        user_req = CreateUserRequest.parse_obj(request.json)
        user = User(
          id=f'{uuid.uuid1()}',
          first_name=user_req.first_name,
          last_name=user_req.last_name,
          email=user_req.email,
          phone=user_req.phone
        )

        users[user.id] = user
        return user.dict(), 201
    else:
        return { "detail": f"Operation not supported: {request.method}" }, 404


@app.route("/users/<user_id>", methods=['GET', 'PUT', 'DELETE'])
def handle_get_user(user_id: str):
    if user_id not in users:
        return { "detail": "User not found" }, 404

    if request.method == 'GET':
        return users[user_id].dict()
    elif request.method == 'PUT':
        upd = request.json
        if 'id' in upd and upd['id'] != user_id:
            return { "detail": "Cannot change user ID" }, 400
        user = User.parse_obj({
            **users[user_id].dict(),
            **upd,
        })
        users[user_id] = user
        return user.dict()
    elif request.method == 'DELETE':
        del users[user_id]
        return {}, 204
    else:
        return { "detail": f"Operation not supported: {request.method}" }, 404


@app.route("/users/<user_id>/files", methods=['GET', 'POST'])
def handle_user_files(user_id: str):
    if user_id not in users:
        return { "detail": "User not found" }, 404

    if request.method == 'GET':
        user_files = []
        if user_id in files:
            user_files = [f.dict() for f in files[user_id].values()]
        return {"files": user_files}
    elif request.method == 'POST':
        file_req = parse_obj_as(CreateUserFileRequest, request.get_json())
        f = File(
          id=f'{uuid.uuid1()}',
          created_at=time.time(),
          contents=file_req.contents
        )
        files[user_id][f.id] = f
        return {"id": f.id}, 201
    else:
        return { "detail": f"Operation not supported: {request.method}" }, 404


def handle_get_user_file(user_id: str, file_id: str):
    if user_id not in users:
        return { "detail": "User not found" }, 404
    if user_id not in files or file_id not in files[user_id]:
        return { "detail": "File not found" }, 404
    return files[user_id][file_id].dict()


def handle_delete_user_file(user_id: str, file_id: str):
    if user_id not in users:
        return { "detail": "User not found" }, 404
    if user_id not in files or file_id not in files[user_id]:
        return { "detail": "File not found" }, 404
    del files[user_id][file_id]
    return {}, 204


@app.route("/users/<user_id>/files/<file_id>", methods=['GET', 'DELETE'])
def handle_user_file(user_id: str, file_id: str):
    if request.method == 'GET':
        return handle_get_user_file(user_id, file_id)
    elif request.method == 'DELETE':
        return handle_delete_user_file(user_id, file_id)
    else:
        return { "detail": f"Operation not supported: {request.method}" }, 404

