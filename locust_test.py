from locust import HttpUser, task, between
import json
import random


class AdventureLoadTest(HttpUser):
    host = "http://localhost:8000"  # Base URL for the API
    wait_time = between(1, 3)  # Random wait between 1-3 seconds between tasks

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queries = [
            "Создайте описание приключения, в котором герои отправляются в зачарованный лес, чтобы найти потерянный артефакт.",
            "Опишите сцену, в которой герои готовятся спасти похищенную принцессу из тёмного замка.",
            "Создайте описание приключения, в котором герои расследуют серию таинственных исчезновений в оживлённом городе.",
            "Опишите сцену, в которой герои отправляются в путешествие через раскалённую пустыню, чтобы найти скрытый оазис.",
            "Создайте описание приключения, в котором герои погружаются под воду, чтобы исследовать затонувший корабль.",
        ]

    @task
    def generate_adventure(self):
        query = random.choice(self.queries)
        headers = {"Content-Type": "application/json"}
        payload = json.dumps({"query": query})

        with self.client.post(
            "/generate", data=payload, headers=headers, catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"Request failed with status {response.status_code}")
            elif not response.json().get("result"):
                response.failure("Empty response received")
