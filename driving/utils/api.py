import requests

class Api:
    def get(self, url, params):
        r = requests.get(url, params=params)
        return r.json()

    def post(self, url, params):
        r = requests.post(url, params=params, json=params)
        return r.json()


