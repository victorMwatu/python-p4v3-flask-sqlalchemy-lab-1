# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def earthquakes(id):
    import json
    result = Earthquake.query.filter_by(id=id).first()
    
    if result:
        result_json = json.dumps(result.to_dict())
        return make_response(result_json)
    else:
        status_code = 404
        message = {
            "message": f"Earthquake {id} not found."
            }
        return make_response(message, status_code)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def magnitude(magnitude):
    import json
    results = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    if results:
        quakes = [result.to_dict() for result in results]
        output = {
                    "count": len(quakes),
                    "quakes": quakes
                    }
        return make_response(output)
    else:
        output = {
                    "count": 0,
                    "quakes": []
        }
        return make_response(output)
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
