import requests


class Api:
    def get(self, url, params):
        r = requests.get(url, params=params)
        if r.status_code == 200:
            return r.json()
        else:
            return None

    def post(self, url, params):
        r = requests.post(url, params=params, json=params)
        if r.status_code == 200:
            return r.json()
        else:
            return None
