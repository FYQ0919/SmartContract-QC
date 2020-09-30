from flask import Flask, jsonify, request
import json
import unittest

headers = {
    'Content-Type': "application/json",
}


app = Flask(__name__)
app_client = app.test_client()


class TesterRoute(unittest.TestCase):
    def setUp(self):
        pass

    def test_routes(self):
        data = {"1": 1}
        r1 = app_client.post(f'http://localhost:5000/1', data=json.dumps(data), headers=headers)
        print(r1.data.decode())


@app.route('/1', methods=["POST"])
def test_route1():
    data = request.get_json()
    # print(data)
    r1 = app_client.post(f'http://localhost:5000/2', data=json.dumps(data), headers=headers)
    response = {
        'message': r1.data.decode()
    }
    return jsonify(response), 200


@app.route('/2', methods=["POST"])
def test_route2():
    data = request.get_json()
    # print(data)
    response = {
        'message': "ok"
    }
    return jsonify(response), 200


if __name__ == '__main__':
    unittest.main()
