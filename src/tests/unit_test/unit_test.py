"""Unit testing module."""
import json

import pytest
from flask import Flask

from src.api.api import blueprint as api_blueprint


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config.from_object('src.settings')
    app.config['TESTING'] = True
    app.register_blueprint(api_blueprint)
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_positive_sentiment(client):
    """Test sentiment analysis for a positive sentence."""
    data = {
        'sentence': 'I love you'
    }
    response = client.post('/inference/sentiment_analysis', json=data)
    assert response.status_code == 200
    response_data = json.loads(response.data.decode('utf-8'))
    assert response_data['sentiment'] == 'POSITIVE'
    assert 0 <= response_data['confidence'] <= 1


def test_negative_sentiment(client):
    """Test sentiment analysis for a negative sentence."""
    data = {
        'sentence': 'I hate you.'
    }
    response = client.post('/inference/sentiment_analysis', json=data)
    assert response.status_code == 200
    response_data = json.loads(response.data.decode('utf-8'))
    assert response_data['sentiment'] == 'NEGATIVE'
    assert 0 <= response_data['confidence'] <= 1


def test_bad_payload(client):
    """Test payload with bad format."""
    data = {
        'sentence2': 'I hate you.'
    }
    response = client.post('/inference/sentiment_analysis', json=data)
    assert response.status_code == 400
    response_data = json.loads(response.data.decode('utf-8'))
    assert 'sentiment' not in response_data
