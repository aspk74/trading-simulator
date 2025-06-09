from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from app.schemas import Order
import uvicorn
import json

app = FastAPI()

# Mock order book
order_book = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            order = Order(**json.loads(data))
            order_book.append(order)
            print(f"New order: {order}")
            await websocket.send_json({
                "status": "ORDER_PLACED",
                "order_id": len(order_book),
                "order": order.dict()
            })
    except WebSocketDisconnect:
        print("Client disconnected")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)