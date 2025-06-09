import pytest
from fastapi.testclient import TestClient
from websockets.client import connect
import json
from app.main import app
from app.schemas import Order

# Fixture for FastAPI test client
@pytest.fixture
def client():
    return TestClient(app)

# Test WebSocket orders
@pytest.mark.asyncio
async def test_websocket_order_matching():
    async with connect("ws://localhost:8000/ws") as websocket:
        test_order = {
            "symbol": "AAPL",
            "price": 150.50,
            "quantity": 10,
            "side": "BUY"
        }
        
        # Send order via WebSocket
        await websocket.send(json.dumps(test_order))
        
        # Verify response
        response = json.loads(await websocket.recv())
        assert response["status"] == "ORDER_PLACED"
        assert response["order"]["symbol"] == "AAPL"

# Test HTTP endpoints
def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 404  # No root endpoint expected

def test_static_files(client):
    response = client.get("/static/index.html")
    assert response.status_code == 200
    assert "Place Order" in response.text

# Test order validation
def test_invalid_order_rejection():
    invalid_order = {
        "symbol": "AAPL",
        "price": -10,  # Invalid price
        "quantity": 0,  # Invalid quantity
        "side": "INVALID"  # Invalid side
    }
    
    with pytest.raises(ValueError):
        Order(**invalid_order)