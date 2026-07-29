import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('OPENAI_API_KEY', 'test_key')
os.environ['TWILIO_AUTH_TOKEN'] = ''

import pytest
from app import app, PERSONAS


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c


def test_index(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'Niorlusx' in resp.data


def test_incoming_call_pricing_disclosure(client):
    resp = client.post('/incoming_call', data={'CallSid': 'CA001'})
    assert resp.status_code == 200
    assert b'ninety-five cents per minute' in resp.data


def test_voice_route_alias(client):
    resp = client.post('/voice', data={'CallSid': 'CA002'})
    assert resp.status_code == 200
    assert b'Luna' in resp.data


def test_incoming_call_all_personas_listed(client):
    resp = client.post('/incoming_call', data={'CallSid': 'CA003'})
    assert resp.status_code == 200
    for name in ['Luna', 'Jade', 'Eon', 'Cleo', 'Vox']:
        assert name.encode() in resp.data


def test_select_persona_luna(client):
    resp = client.post('/select_persona', data={'CallSid': 'CA004', 'Digits': '1'})
    assert resp.status_code == 200
    assert b'Luna' in resp.data


def test_select_persona_jade(client):
    resp = client.post('/select_persona', data={'CallSid': 'CA005', 'Digits': '2'})
    assert resp.status_code == 200
    assert b'Jade' in resp.data


def test_select_persona_invalid_digit_defaults_to_vox(client):
    resp = client.post('/select_persona', data={'CallSid': 'CA006', 'Digits': '9'})
    assert resp.status_code == 200
    assert b'Vox' in resp.data


def test_handle_speech_no_text(client):
    resp = client.post('/handle_speech', data={'CallSid': 'CA007'})
    assert resp.status_code == 200
    assert b"didn't catch that" in resp.data


def test_handle_speech_missing_call_sid(client):
    resp = client.post('/handle_speech', data={})
    assert resp.status_code == 200
    assert b'Missing call info' in resp.data


def test_personas_dict_complete():
    assert set(PERSONAS.keys()) == {'1', '2', '3', '4', '5'}
    for key, persona in PERSONAS.items():
        assert 'name' in persona
        assert 'prompt' in persona
        assert len(persona['prompt']) > 0
