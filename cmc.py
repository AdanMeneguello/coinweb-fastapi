import os
import requests

CMC_BASE_URL = "https://pro-api.coinmarketcap.com"
CMC_API_KEY = os.getenv("CMC_API_KEY")

if not CMC_API_KEY:
    raise RuntimeError("CMC_API_KEY não encontrada. Defina a variável de ambiente CMC_API_KEY e reinicie o terminal.")

HEADERS = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": CMC_API_KEY,
}

def _get_json(url: str, params: dict | None = None) -> dict:
    resp = requests.get(url, headers=HEADERS, params=params, timeout=20)

    if resp.status_code != 200:
        try:
            print("ERRO API:", resp.json())
        except Exception:
            print("ERRO API (texto):", resp.text)
        resp.raise_for_status()

    data = resp.json()
    status = data.get("status")
    if status and status.get("error_code", 0) != 0:
        raise RuntimeError(f"CoinMarketCap API erro: {status.get('error_message')}")

    return data

def pegar_cotacoes():
    # BTC em USD
    url_btc = f"{CMC_BASE_URL}/v1/cryptocurrency/quotes/latest"
    btc_usd_data = _get_json(url_btc, {"id": "1", "convert": "USD"})
    btc_usd = btc_usd_data["data"].get("1") or btc_usd_data["data"].get(1)
    bitcoin_usd = float(btc_usd["quote"]["USD"]["price"])

    # BTC em BRL (2ª chamada por limite do plano)
    btc_brl_data = _get_json(url_btc, {"id": "1", "convert": "BRL"})
    btc_brl = btc_brl_data["data"].get("1") or btc_brl_data["data"].get(1)
    bitcoin_brl = float(btc_brl["quote"]["BRL"]["price"])

    # USD -> BRL
    url_fx = f"{CMC_BASE_URL}/v2/tools/price-conversion"
    fx_data = _get_json(url_fx, {"amount": 1, "symbol": "USD", "convert": "BRL"})
    fx_payload = fx_data["data"]
    if isinstance(fx_payload, list):
        fx_payload = fx_payload[0]
    dolar_brl = float(fx_payload["quote"]["BRL"]["price"])

    return dolar_brl, bitcoin_brl, bitcoin_usd
