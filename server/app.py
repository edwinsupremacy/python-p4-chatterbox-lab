from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages')
def messages():
    messages = Message.query.order_by('created_at').all()
    return make_response(jsonify([message.to_dict() for message in messages]))

@app.route('/messages', methods=['POST'])
def post_message():
    data = request.get_json()
    message = Message(body=data['body'],username=data['username'])
    db.session.add(message)
    db.session.commit()
    return make_response(message.to_dict())

@app.route('/messages/<int:id>', methods=['PATCH'])
def patch_message(id):
    message = Message.query.filter_by(id=id).first()
    if message:
        data = request.get_json()
        for attr in data:
            setattr(message, attr, data[attr])
        db.session.add(message)
        db.session.commit()
        return make_response(message.to_dict())
    else:
        return print({'error': 'Message not found'})

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.filter_by(id=id).first()
    if message:
        db.session.delete(message)
        db.session.commit()
        return make_response({'deleted': True})
    else:
        return print({'error': 'Message not found'})

if __name__ == '__main__':
    app.run(debug=True)
