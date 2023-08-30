import json
import os

import requests


class Copper:

    def __init__(self, base_url):
        api_key = os.getenv('COPPER_API_KEY')
        api_user_email = os.getenv('COPPER_API_USER_EMAIL')
        target_pipeline_id = os.getenv('COPPER_TARGET_PIPELINE_ID')
        target_custom_field_definition_id = os.getenv('COPPER_TARGET_CUSTOM_FIELD_DEFINITION_ID')

        if not all([api_key, api_user_email, target_pipeline_id, target_custom_field_definition_id]):
            raise ValueError('Copper credentials not present in environment')

        self.base_url = base_url
        self.default_headers = {
            'Content-Type': 'application/json',
            'X-PW-Application': 'developer_api',
            'X-PW-AccessToken': api_key,
            'X-PW-UserEmail': api_user_email,
        }
        self.target_pipeline_id = int(target_pipeline_id)
        self.target_custom_field_definition_id = int(target_custom_field_definition_id)

    def fetch_opportunity(self, opportunity_id: int) -> dict:
        response = requests.request(
            'GET',
            "{base_url}/opportunities/{id}".format(base_url=self.base_url, id=opportunity_id),
            headers=self.default_headers
        )

        return json.loads(response.text)

    def fetch_pipeline_stages_ids(self, pipeline_id: int) -> list[int]:
        response = requests.request(
            'GET',
            "{base_url}/pipeline_stages/pipeline/{id}".format(base_url=self.base_url, id=pipeline_id),
            headers=self.default_headers
        )

        return list(map(lambda stage: stage['ids'], json.loads(response.text)))[1:]



