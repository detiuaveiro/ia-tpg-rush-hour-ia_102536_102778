import asyncio
import getpass
import json
import os
import websockets
from time import sleep


def main():
    """Main function."""

    sleep(1) # wait for server to start

    loop = asyncio.get_event_loop()
    SERVER = os.environ.get("SERVER", "localhost")
    PORT = os.environ.get("PORT", "8000")
    NAME = os.environ.get("NAME", getpass.getuser())
    loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))


async def agent_loop(server_address="localhost:8000", agent_name="student"):
    """Example client loop."""
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))

        while True:
            try:
                # receive game update, this must be called timely or your game will get out of sync with the server
                state = json.loads(await websocket.recv())  

                print(state)

                # Next lines are only for the Human Agent, the key values are nonetheless the correct ones!
                key = ""

                # send key command to server - you must implement this send in the AI agent
                await websocket.send(json.dumps({"cmd": "key", "key": key}))
    
            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return


if __name__ == "__main__":
    main()