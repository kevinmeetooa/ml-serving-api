"""Load testing module"""
import os
import random

from locust import HttpUser, between, task

API_KEY = os.environ.get('API_KEY')


def get_random_sentence():
    sentences = ["i love you",
                 "i hate you",
                 "i don't know"]
    return random.choice(sentences)


class ApiUser(HttpUser):
    """API User class for load test."""
    wait_time = between(0.5, 1)

    def on_start(self):
        """."""
        self.client.trust_env = True

    @task(1)
    def send_sentence(self):
        sentence = get_random_sentence()
        self.client.post("api/v1/inference/sentiment_analysis",
                         headers={
                                    'accept': 'application/json',
                                    'Authorization': 'Basic ' + API_KEY,
                                    'Content-Type': 'application/json'
                                },
                         json={'sentence': sentence})
