import requests

def calulateFreight(products, postalcodeSender, postalcodeRecevier):
    url = "https://www.melhorenvio.com.br/api/v2/me/shipment/calculate"

    payload = {
        "from": { "postal_code": postalcodeSender },
        "to": { "postal_code": postalcodeRecevier },
            "products":[{
                "id": p.id,
                "height": p.height,
                "width": p.width,
                "length": p.length,
                "weight": p.weight,
                "quantity": p.quantity
            }for p in products]
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiOTQ1N2EzODA1ZDNiODk0ODVjOTBjN2JhM2Y5YTI2N2VlYTNjMDNmMmM4NDdjZGI2ZDI4Y2YzNDI5ZjAzMDQwYWFjNjM0ODYxZWE5NTdhZWQiLCJpYXQiOjE3MTM5ODUwODguNTMxODU0LCJuYmYiOjE3MTM5ODUwODguNTMxODU2LCJleHAiOjE3NDU1MjEwODguNTIwMDI3LCJzdWIiOiI5YmUyY2NmMy1iMGY4LTQ2MzItOTQzMS0xYzVkNDhkZjljMDYiLCJzY29wZXMiOlsic2hpcHBpbmctY2FsY3VsYXRlIl19.vmkFNG3OskZ803CsIvPUHIF7Kucb5Z5433kewv0oM4ddShNgkAnl3XJyAknFlsc1sfXXJVTfspV8XQJoZiMUn_HtlOSEXfwgVFd2maSwNJEZBoyFgN6H5jdFk3Khe605ZIz4RqOlqTyfD9L8H_78BtrUXi7BR0wqy5WGY06AR7WUvzq3LeaQa8RtBfAEon_67_AqD0dG6_Hwc6Lr2-oB7pfj47-kt0NN-dynbkA2mpN9N7i5uxFbx7JSCecE--m7DfUcJWVwGq1qGkD_AI8ACDYMmaRBYo-k9LgpLKYYteryfjNWC8YrUGtQ0DW-LbOyGovFfHpgHCNP7DuQuFfI8YLtP39BZhccpmycx3-jDE_rY5_2UdmXFJqklAnFksrmyNFLsDWFFvvvphsK7M9H73Ez8Jx5ly0eU7l9FhLxRhmJ0ZyLbeKtUGzsjB46tP9Zwv_EGAtZU0nknycuDR0FWktM20VJ0mA_xJiCXN0lw3X3cowEdrE72QWwgsJ-giH1eF7oqx7mOIi3_xvti1f58coGFkiYMCLWLaWN6PSoWUXZBJ-L57Cp0XTc4dJLdEZ2hOhnD0ASB1M2MxosR62jVrUcFsaz8L75TbPC6uFpKK01GqefVQ6St_AiPvDR1wIQ7OpIj6O2ZHpwBIyqa5zD2US-xxDQLi4efMHqHrbAY70",
        "User-Agent": "Aplicação guimaster90@gmail.com"
    }

    response = requests.post(url, json=payload, headers=headers)
    
    print(response.text)

    return response
calulateFreight(1,1,1,1,1,1)