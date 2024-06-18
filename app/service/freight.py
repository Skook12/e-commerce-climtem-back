import requests
from typing import List
from configs.config import Config
from ezdxf.addons import binpacking as bp

SMALL_ENVELOPE = ("small-envelope", 11.5, 6.125, 0.25, 10)
LARGE_ENVELOPE = ("large-envelope", 15.0, 12.0, 0.75, 15)
SMALL_BOX = ("small-box", 8.625, 5.375, 1.625, 70.0)
MEDIUM_BOX = ("medium-box", 11.0, 8.5, 5.5, 70.0)
MEDIUM_BOX2 = ("medium-box-2", 13.625, 11.875, 3.375, 70.0)
LARGE_BOX = ("large-box", 12.0, 12.0, 5.5, 70.0)
LARGE_BOX2 = ("large-box-2", 23.6875, 11.75, 3.0, 70.0)

ALL_BINS = [
    SMALL_ENVELOPE,
    LARGE_ENVELOPE,
    SMALL_BOX,
    MEDIUM_BOX,
    MEDIUM_BOX2,
    LARGE_BOX,
    LARGE_BOX2,
]

class Product:

    def __init__(self, id, height, width, length, weight ):
        self.first = id
        self.second = height

def build_packer(products):
    packer = bp.Packer()

    for i in range(len(products)):
        for p in range(products[i][1]):
            product = products[i][0]
            packer.add_item(str(product["id"]) + str(p),float(product["width"]),float(product["height"]),float(product["length"]),float(product["weight"]))
    return packer


def calulateFreight(product, postalcodeRecevier, postalcodeSender = 42700000):
    url = "https://www.melhorenvio.com.br/api/v2/me/shipment/calculate"


    payload = {
        "from": { "postal_code": postalcodeSender },
        "to": { "postal_code": postalcodeRecevier },
            "products":[{
                "id": product[0]["id"],
                "height": float(product[0]["height"]),
                "width": float(product[0]["width"]),
                "length": float(product[0]["length"]),
                "weight": float(product[0]["weight"]),
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

    return [entry for entry in response.json() if "error" not in entry]



def calulateMutipleFreight(products, postalcodeRecevier, postalcodeSender = 42700000):
    url = "https://www.melhorenvio.com.br/api/v2/me/shipment/calculate"
    
    bins: List[bp.Bin] = []
    for box in ALL_BINS:
        packerCanvas = build_packer(products)
        packer = packerCanvas
        packer.add_bin(*box)
        packer.pack(bp.PickStrategy.SMALLER_FIRST)
        bins.extend(packer.bins)
   
    smallest_volume = float('inf')
    lightest_weight = float('inf')
    selected_bin = None
    for bin in bins:
        volume = bin.width * bin.height * bin.depth
        if volume < smallest_volume or (volume == smallest_volume and bin.max_weight < lightest_weight):
            smallest_volume = volume
            lightest_weight = bin.max_weight
            selected_bin = bin
    
    payload = {
        "from": { "postal_code": postalcodeSender },
        "to": { "postal_code": postalcodeRecevier },
            "package":{
                "id":"1",
                "height": selected_bin.height,
                "width": selected_bin.width,
                "length": selected_bin.depth,
                "weight": selected_bin.max_weight
            }
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + Config.MEV_SETTINGS,
        "User-Agent": "Aplicação guimaster90@gmail.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    return [entry for entry in response.json() if "error" not in entry]