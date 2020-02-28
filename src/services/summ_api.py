from typing import List, Dict, Union

import requests
from requests import Response

from application import app


class SummApi:
    def __init__(self) -> None:
        self.url = app.config.get("SUMMARIZER_API_URL")
        self.headers = {"Content-type": "application/json"}

    def run(self, text: str) -> List[Dict[str, Union[str, int, float]]]:
        data: Dict[str, str] = {"text": text}
        response: Response = requests.post(
            url=self.url, json=data, headers=self.headers
        )

        if response.status_code == requests.codes.OK:
            json_data = list(response.json())
            return json_data
        else:
            return list()
