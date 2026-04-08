"""Application web minimale pour contrôler le rail de caméra."""

from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        'message': 'Contrôle du rail caméra Raspberry Pi',
        'status': 'ok'
    })

@app.route('/move', methods=['POST'])
def move():
    data = request.json or {}
    direction = data.get('direction')
    speed = data.get('speed', 50)

    if direction not in ('forward', 'backward', 'stop', 'calibrate'):
        return jsonify({'error': 'direction invalide'}), 400

    # TODO: appeler les méthodes du pilote moteur
    return jsonify({'direction': direction, 'speed': speed})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
