


from driving.utils.api import Api


class Geo(Api):
    def getGeo(self, src):

        return super().get("https://script.google.com/macros/s/AKfycbytzsMF7hCN7yab9fhuQCZUzOSMSGkI3Q9bXTIerROkrVCqdeS8byvTNFDLiM77o6fO/exec",
            {"src": src})

