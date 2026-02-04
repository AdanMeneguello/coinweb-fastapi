from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from cmc import pegar_cotacoes

app = FastAPI(title="CoinWeb")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/cotacoes", response_class=JSONResponse)
def cotacoes():
    dolar_brl, bitcoin_brl, bitcoin_usd = pegar_cotacoes()
    return {
        "dolar_brl": dolar_brl,
        "bitcoin_brl": bitcoin_brl,
        "bitcoin_usd": bitcoin_usd,
    }
