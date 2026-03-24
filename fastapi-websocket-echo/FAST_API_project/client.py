import asyncio
import websockets

async def test():
    async with websockets.connect("ws://localhost:8000/ws") as websocket:
        await websocket.send("Hello Server")
        response = await websocket.recv()
        print(response)

async def run_test():
    try:
        await test()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(run_test())