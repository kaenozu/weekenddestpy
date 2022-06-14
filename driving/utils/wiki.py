

from driving.utils.api import Api


class Wiki(Api):
    def getWiki(self, title):

        res = super().get("https://ja.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro&explaintext",
                          {"titles": title})

        for v in res["query"]["pages"].values():
            try:
                return v["extract"]
            except KeyError as e:
                return None


# r = Wiki()
# print(r.getWiki("ふぇあふぇあえｆ"))
# print(r.getWiki("六義園"))
