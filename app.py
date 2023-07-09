from sport import ns as sport_ns
from event import ns as event_ns
from selection import ns as selection_ns

from flask_restx import Api
from flask import Flask


api = Api(
    title='Spectate APIs',
    version='1.0',
    description='All the APIs needed for Spectate',
)

api.add_namespace(sport_ns, path='/')
api.add_namespace(event_ns, path='/')
api.add_namespace(selection_ns, path='/')


app = Flask(__name__)
api.init_app(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
