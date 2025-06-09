from pydantic import BaseModel

class Order(BaseModel):
    symbol: str
    price: float
    quantity: int
    side: str  # "BUY" or "SELL"