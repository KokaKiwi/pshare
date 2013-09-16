import flask
from . import utils
from .settings import settings
from .utils.web import (view, json)
from .models import *

app = flask.Flask(__name__)

utils.web.VIEW_DEFAULTS = {
    'siteName': settings.site_name,
    'settings': settings
}

# Index
@app.route('/')
@view('index')
def index():
    pass

# Owner
@app.route('/o/<oid>')
@view('owner')
def owner(oid):
    q = session.query(Pad).filter(Pad.owner_id == oid)
    pad = q.first()

    if not pad:
        pad = Pad(oid)
        session.add(pad)
        session.commit()

    return {'pad': pad}

# Pad
@app.route('/p/<pid>')
@view('pad')
def pad(pid):
    q = session.query(Pad).filter(Pad.pad_id == pid)
    pad = q.first()

    if not pad:
        flask.abort(404)

    return {'pad': pad}

# Send message
@app.route('/s/<pid>', methods = ['POST'])
@json()
def send(pid):
    q = session.query(Pad).filter(Pad.pad_id == pid)
    pad = q.first()

    if not pad:
        return {'status': 'NOPE'}

    req = flask.request
    content = req.form['content']

    message = Message(pid, content)
    session.add(message)
    session.commit()

    return {'status': 'OK'}

# Delete pad
@app.route('/d/<oid>', methods = ['POST', 'GET'])
@json()
def delete(oid):
    q = session.query(Pad).filter(Pad.owner_id == oid)
    pad = q.first()

    if not pad:
        return {'status': 'NOPE'}

    session.delete(pad)
    session.commit()

    return {'status': 'OK'}

if settings.debug:
    def message_to_json(message):
        o = dict()
        o['date'] = str(message.date)
        o['pad_id'] = message.pad_id
        o['content'] = message.content

        return o

    def pad_to_json(pad):
        o = dict()
        o['date'] = str(pad.date)
        o['owner_id'] = pad.owner_id
        o['pad_id'] = pad.pad_id
        o['messages'] = []

        for message in pad.messages:
            o['messages'].append(message_to_json(message))

        return o

    # List pads
    @app.route('/pads')
    @json(pretty_print = True)
    def pads():
        q = session.query(Pad)
        items = q.all()

        pads = []
        for item in items:
            pads.append(pad_to_json(item))

        return pads

    # List messages
    @app.route('/messages')
    @json(pretty_print = True)
    def messages():
        q = session.query(Message)
        items = q.all()

        messages = []
        for item in items:
            messages.append(message_to_json(item))

        return messages
