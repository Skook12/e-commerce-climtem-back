import requests
from configs.config import Config

class Product:

    def __init__(self, id, height, width, length, weight ):
        self.first = id
        self.second = height


def calulateFreight(product, postalcodeRecevier, postalcodeSender = 42700000):
    url = "https://www.melhorenvio.com.br/api/v2/me/shipment/calculate"


    payload = {
        "from": { "postal_code": postalcodeSender },
        "to": { "postal_code": postalcodeRecevier },
            "products":[{
                "id": product[0]["id"],
                "height": product[0]["height"],
                "width": product[0]["width"],
                "length": product[0]["length"],
                "weight": product[0]["weight"],
                "quantity": 1
            }]
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + Config.MEV_SETTINGS,
        "User-Agent": "Aplicação guimaster90@gmail.com"
    }

    response = requests.post(url, json=payload, headers=headers)
    
    print(response.text)

    return response



def calulateMutipleFreight(products, postalcodeRecevier, postalcodeSender = 42700000):
    url = "https://www.melhorenvio.com.br/api/v2/me/shipment/calculate"


    payload = {
        "from": { "postal_code": postalcodeSender },
        "to": { "postal_code": postalcodeRecevier },
            "products":[{
                "id": p[0]["id"],
                "height": p[0]["height"],
                "width": p[0]["width"],
                "length": p[0]["length"],
                "weight": p[0]["weight"],
                "quantity": 1
            }for p in products]
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + Config.MEV_SETTINGS,
        "User-Agent": "Aplicação guimaster90@gmail.com"
    }

    response = requests.post(url, json=payload, headers=headers)
    
    print(response.text)

    return response