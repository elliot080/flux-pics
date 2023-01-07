#!/usr/bin/env python3

from ast import parse
from flask import Flask, render_template, request, jsonify
from webargs import fields
from webargs.flaskparser import use_args
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def hello():
    return "hello"

@app.route('/deploy', methods=['GET'])
def dropdown():
    colors = ['Red', 'Blue', 'Black', 'Orange']
    return render_template('test.html', colours=colors)

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        return 'Get', 200
    elif request.method == 'POST':
        return 'Post', 200
    else:
        return 'Error', 500

@app.errorhandler(422)
@app.errorhandler(400)
def error_handler(err):
    headers = err.data.get("headers", None)
    messages = err.data.get("messages", ["Invalid request."])
    if headers:
        return jsonify({"errors": messages}), err.code, headers
    else:
        return jsonify({"errors": messages}), err.code

@app.route('/echo', methods=['GET','PUT','POST'])
@use_args({"args": fields.Str()}, location='query')
def containers(args):
    if request.method == 'POST':
        return args['args']

@app.route('/images', methods=['GET', 'POST'])
def images():
    if request.method == 'GET':
        return "Not implemented"
    elif request.method == 'POST':
        if not request.files:
            return 'No file uploaded', 400
        f = request.files['file']
        if 'png' not in f.filename:
            return 'Invalid filetype', 400
        try:
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
            return 'File saved!', 200
        except Exception as E:
            return 'Failed to save file', 500
    else:
        return 'Error', 500
