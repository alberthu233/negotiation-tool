# pyright: reportMissingImports=false
# pylint: disable=import-error
import os
from typing import Optional
from fastapi import FastAPI, Header, HTTPException  # type: ignore
from pydantic import BaseModel, Field  # type: ignore
from app.core.negotiator import next_agent_offer

API_KEY = os.getenv("API_KEY", "")


class NegotiateIn(BaseModel):
    driver_price: float = Field(ge=0)
    price_margin: float = Field(gt=0)
    agent_price: float = Field(ge=0)


class NegotiateOut(BaseModel):
    next_agent_price: float


app = FastAPI(title="Negotiation Tool", version="0.1.0")


def auth(x_api_key: Optional[str]):
    if not API_KEY:
        return
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/negotiate", response_model=NegotiateOut)
def negotiate(payload: NegotiateIn, x_api_key: Optional[str] = Header(default=None, alias="X-API-Key")):
    auth(x_api_key)
    nxt = next_agent_offer(
        driver_price=payload.driver_price,
        price_margin=payload.price_margin,
        agent_price=payload.agent_price,
    )
    return NegotiateOut(next_agent_price=float(nxt))


