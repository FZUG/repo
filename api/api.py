#!/bin/python3
# coding: utf-8
from flask import Flask, jsonify, abort, make_response, request, url_for
from utils import chrome

app = Flask(__name__)

@app.route('/api/v1.0/chrome', methods=['GET'])
def get_chrome():
    platform = ['win', 'mac', 'linux']
    archs = ['x86', 'x64']
    channels = ['stable', 'beta', 'dev', 'canary']

    system = request.args.get('os', platform)
    arch = request.args.get('arch', archs)
    channel = request.args.get('channel', channels)

    system = [system] if type(system) == str else system
    arch = [arch] if type(arch) == str else arch
    channel = [channel] if type(channel) == str else channel

    if system[0] in platform and arch[0] in archs and channel[0] in channels:
        return jsonify({'results': chrome.get_pkg_info(system, channel, arch)})
    else:
        abort(404)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/api')
def index():
    return jsonify({
        'msg': 'Hello, Fedora.',
        'version': 'v1.0',
        'apis': [url_for('get_chrome', _external=True)]
    })

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port='5000')
    app.run(debug=True)
