from enum import Enum
import websockets
import asyncio
import re
import json

from gyverhub_tags import GHTag

# Where the packet processing happens
# https://github.com/GyverLibs/GyverHub/blob/00e1343ae12d9e5446e8418856ddb2fbc898f176/src/core/hub.h#L216

class TornadoscopeVariables(Enum):
    state = 1
    freq = 2
    ampliX = 3
    ampliY = 4
    phaseY = 5
    multY = 6
    expo = 7
    phase = 8
    phase_state = 9
    phase_hue_auto = 10
    phase_trig_auto = 11
    phase_hue_val = 12
    phase_trig_val = 13
    phase_hue_step = 14
    phase_trig_step = 15

class Device:
    def __init__(self, ip, port, cat_id, dev_id) -> None:
        self.ip = ip
        self.port = port
        self.cat_id = cat_id
        self.dev_id = dev_id
        self.websocket = None

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
        if self.websocket is None:
            await self.connect()

        if self.websocket:
            try:
                await self.websocket.send(f"MyDevices/{self.cat_id}/{self.dev_id}/{query}")
                responses = []
                for i in range(n_responses):
                    response = await self.websocket.recv()
                    response = Device.decode_response(response)
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
                print(f"Error during WebSocket communication: {e}")
    
    async def get(self, variable):
        got = await self.run_query(f"get/_n{variable.value}")
        # Decoded: #{#id:"1ce9cfea",#type:#get,#value:"111"}#
        # [{'id': '1ce9cfea', 'type': 'update', 'updates': {'_n3': {'value': '112'}}}]
    
    async def set(self, variable, value):
        await self.run_query(f"set/_n{variable.value}={value}", 2)
        # https://github.com/GyverLibs/GyverHub/blob/main/src/core/core.h#L311
        # Decoded: #{#id:"1ce9cfea",#type:#ack,#name:"_n3"}#
        # JSON: {'id': '1ce9cfea', 'type': 'ack', 'name': '_n3'}
        # https://github.com/GyverLibs/GyverHub/blob/main/src/core/core.h#L383
        # Decoded: #{#id:"1ce9cfea",#type:#update,#updates:{"_n3":{#value:"111"}}}#
        # JSON: {'id': '1ce9cfea', 'type': 'update', 'updates': {'_n3': {'value': '112'}}}

async def main():
    device = Device("192.168.123.17", 81, "1ce9cfea", "22b6215d")
    device = Device("192.168.11.70", 81, "1ce9cfea", "22b6215d")
    await device.set(TornadoscopeVariables.ampliX, 112)
    await device.get(TornadoscopeVariables.ampliX)

if __name__ == "__main__":
    asyncio.run(main())




        


