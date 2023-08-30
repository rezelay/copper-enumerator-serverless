import json
import os

import requests


class Copper:

    def __init__(self, base_url):
        api_key = os.getenv('COPPER_API_KEY')
        api_user_email = os.getenv('COPPER_API_USER_EMAIL')

        if api_key is None or api_user_email is None:
            raise ValueError('Copper credentials not present in environment')

        self.base_url = base_url
        self.default_headers = {
            'Content-Type': 'application/json',
            'X-PW-Application': 'developer_api',
            'X-PW-AccessToken': api_key,
            'X-PW-UserEmail': api_user_email,
        }
