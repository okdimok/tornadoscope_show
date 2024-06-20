import websockets
import asyncio
import re
import json
import traceback 


from gyverhub_tags import GHTag
from tornadoscope_state import TornadoscopeVariables

# Where the packet processing happens
# https://github.com/GyverLibs/GyverHub/blob/00e1343ae12d9e5446e8418856ddb2fbc898f176/src/core/hub.h#L216



class Device:
    def __init__(self, ip, port, dev_id, client_id) -> None:
        self.ip = ip
        self.port = port
        self.dev_id = dev_id
        self.client_id = client_id
        self.websocket = None
        self.comm_lock = asyncio.Lock()

    @staticmethod
    async def from_ip(ip, client_id="PYcli"):
        port = 81
        d = Device(ip, port, None, client_id)
        result = await d.discover()
        d.dev_id = result[0]['id']
        return d


    def get_uri(self):
        return f"ws://{self.ip}:{self.port}"
    
    async def connect(self):
        try:
            print(f"Connecting to {self.get_uri()}")
            self.websocket = await websockets.connect(self.get_uri())
            print("Connection established")
        except Exception as e:
            print(f"Failed to connect: {e}")

    @staticmethod
    def decode_response(response):
        def get_tag_name(match):
            matched_string = match.group()
            tag_id = int(matched_string[1:], 16)
            tag = GHTag(tag_id)
            return f'"{tag.name}"'
        
        result = re.sub(r'#[0-9a-f]+', get_tag_name, response)
        return result
    
    async def run_query(self, query="ping", n_responses=1):
        async with self.comm_lock:
            if self.websocket is None:
                await self.connect()

            if self.websocket:
                try:
                    prefix = "MyDevices"
                    if query != "discover":
                        uri = f"{prefix}/{self.dev_id}/{self.client_id}/{query}"
                    else:
                        uri = f"{prefix}"
                    
                    await self.websocket.send(uri)
                    responses = []
                    current_response = ""
                    while len(responses) < n_responses:
                        response = await self.websocket.recv()
                        current_response += response
                        if not current_response.endswith("}#"):
                            continue
                        response = Device.decode_response(current_response)
                        current_response = ""
                        # print(f"Decoded: {response}")
                        if not response.startswith("#{") and not response.endswith("}#"):
                            print(f"WARNING. Wrong response detected: {response}")
                            continue
                        response = response[1:-1]
                        response = json.loads(response)
                        print(f"JSON: {response}")
                        responses.append(response)
                    return responses
                
                except websockets.exceptions.ConnectionClosed as e:
                    print(f"WebSocket connection closed: {e}")
                    self.websocket = None
                except Exception as e:
                    print(f"Error during WebSocket communication: {e} ")
                    traceback.print_exc()

    async def discover(self):
        return await self.run_query("discover")
    
    async def get(self, variable: TornadoscopeVariables):
        got = await self.run_query(f"get/_n{variable.value}")
        # Decoded: #{#id:"1ce9cfea",#type:#get,#value:"111"}#
        # [{'id': '1ce9cfea', 'type': 'update', 'updates': {'_n3': {'value': '112'}}}]
        return got[0]
    
    # setting any variable for Tornadoscope
    # takes approx 22 ms. Updating all the variables takes approx 
    # 22 * ( 7 + 5 * 8 ) = 1034 ms = 1 s
    async def set(self, variable: TornadoscopeVariables, value):
        await self.run_query(f"set/_n{variable.value}={value}", 2)
        # https://github.com/GyverLibs/GyverHub/blob/main/src/core/core.h#L311
        # Decoded: #{#id:"1ce9cfea",#type:#ack,#name:"_n3"}#
        # JSON: {'id': '1ce9cfea', 'type': 'ack', 'name': '_n3'}
        # https://github.com/GyverLibs/GyverHub/blob/main/src/core/core.h#L383
        # Decoded: #{#id:"1ce9cfea",#type:#update,#updates:{"_n3":{#value:"111"}}}#
        # JSON: {'id': '1ce9cfea', 'type': 'update', 'updates': {'_n3': {'value': '112'}}}

    async def ui(self):
        await self.run_query("ui")

    async def ping(self):
        await self.run_query("ping")

async def main():
    # device = await Device.from_ip("192.168.123.17")
    device = await Device.from_ip("192.168.11.70")
    import datetime
    start = datetime.datetime.now().timestamp()
    n = 100
    for i in range(n):
        await device.set(TornadoscopeVariables.ampliX, 112)
    finish = datetime.datetime.now().timestamp()
    duration = (finish - start)/n
    print(f"Duration: {duration}")
    # await device.get(TornadoscopeVariables.ampliX)
    # await device.ui()
    # await device.discover()

if __name__ == "__main__":
    asyncio.run(main())




        


