"""Main module for our api."""
import binascii
import logging
from typing import Any, Dict
import numpy as np
import tensorflow as tf
from flask import Blueprint, Flask, current_app, jsonify, request
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
from urllib.request import urlretrieve

from src.errors.errors import ApiError
from src.utils.log import log_execution_time

blueprint = Blueprint('api', __name__)

# Load the model
model = TFAutoModelForSequenceClassification.from_pretrained("bert-base-cased",
                                                             num_labels=2)

url = 'https://www.dropbox.com/scl/fi/2bnritwhdhaobwlgabxcz/tf_model.h5?rlkey=59pebei0jjlo88b8vqa6vi4at&dl=1'
output_path = "tf_model.h5"

# Download the model archive file
urlretrieve(url, output_path)
model.load_weights('tf_model.h5')


@blueprint.route('/inference/sentiment_analysis', methods=['POST'])
@log_execution_time()
def sentiment_analysis() -> Dict[str, Any]:
    """Perform sentiment analysis on a given sentence.

    Returns a dictionary containing sentiment ('POSITIVE' or 'NEGATIVE')
    and confidence (a float value between 0 and 1).
    """
    current_app.logger.info("Running inference")
    current_app.logger.info("Request %s", request.json)
    data = request.json
    current_app.logger.info("Request json %s", data)


    # Check if 'sentence' key exists and is a string
    if 'sentence' not in data or not isinstance(data['sentence'], str):
        raise ApiError(400, 'INVALID_PAYLOAD',
                       'The JSON payload must contain a valid '
                       '"sentence" key with a string value')

    sentence = data['sentence']

    # Input preprocessing
    tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
    preprocessed_test = tokenizer([sentence], return_tensors="np",
                                  padding=True)

    # Inference
    prediction = model.predict(dict(preprocessed_test))['logits']
    test_predictions_class = np.argmax(prediction)

    sentiment = "NEGATIVE" if test_predictions_class == 0 else "POSITIVE"

    # Get confidence from logits with tensorflow's softmax function
    # instead of computing softmax ourselves
    confidence = float(tf.nn.softmax(prediction, axis=1)[0]
                       [test_predictions_class])

    # Return response
    response = {
        "sentiment": sentiment,
        "confidence": confidence
    }

    return jsonify(response)


@blueprint.errorhandler(ApiError)
def handle_api_error(error):  # type: ignore
    """Return a json representation of all API errors."""
    current_app.logger.info(
        'Caught client error: status_code=%d, error=%s',
        error.status_code, error.to_dict())
    return jsonify(error.to_dict()), error.status_code


@blueprint.before_request
def auth_request() -> None:
    """Handle HTTP Basic Authentication.

    Raises ApiError: If API key is not authorized or wrongly formatted."""
    # Skip auth if api key isn't defined in config
    want_key = current_app.config['API_KEY']
    if not want_key or current_app.config['TESTING']:
        return None
    try:
        auth = request.authorization
    except binascii.Error:
        raise ApiError(401, 'WRONGLY_FORMATTED_KEY',
                       'API key is wrongly formatted')
    if auth is None or auth.username != 'admin' or \
            auth.password != want_key:
        raise ApiError(401, 'UNAUTHORIZED_KEY',
                       'API key is not authorized')
    return None


app = Flask('src')
app.logger.setLevel(logging.INFO)
app.config.from_object('src.settings')
app.register_blueprint(blueprint, url_prefix='/api/v1')
