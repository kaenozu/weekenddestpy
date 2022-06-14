

from driving.utils.api import Api


class Route(Api):
    def getRoute(self, route):

        return super().post("https://script.google.com/macros/s/AKfycbyPvT1K338SNJT_NdqZrqYCw-UxMXOKboW6wM3X8aTIw1bFwNi0Ks8K1jpikrVRfgKC/exec",
                            {"routes": route})


# r = Route()
# r.getRoute([dict(src="大宮駅", dest="上野駅", place_name="上野駅")])
