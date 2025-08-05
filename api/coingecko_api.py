import requests

def buscar_preco_cripto(cripto):

    
    url = f"https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": cripto,
        "vs_currencies": "brl,usd"
    }

    try:
        resposta = requests.get(url, params=params)
        data = resposta.json()
        return data.get(cripto)
    except Exception as e:
        print("Erro na API:", e)
        return None
