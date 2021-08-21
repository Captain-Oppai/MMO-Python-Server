import asyncio
import websockets
import json
import os

# Protocol Codes:
#   0 = Server instantiation
#   1 = Client Server Swap
#
#
#
#
#
#

registeredScenes = [
    "ttc_pg",
    "ttc_pp",
    "ttc_ll",
    "ttc_ss",
    "dd_pg",
    "dd_bb",
    "dd_ss",
    "dd_ll",
    "Scene2"
]

#message = '{ "port":"1234", "scene":"Scene1" }'
message = {"port": [], "scene": []}

activeServers = {}

portCounter = 2234

firstRun = False

serverData = []

def ServerInstantiate(scene):
    global firstRun
    global serverData
    if firstRun == False :
        print("System instantiation, booting Toontown Central playground server.")
        firstRun = True
        print('cmd /c "docker run -dp 127.0.0.1:' + str(portCounter) + ':' + str(portCounter) + ' --rm toontown_alpha:0.0.4')
        #os.system('cmd /c "docker run -dp 127.0.0.1:' + str(portCounter) + ':' + str(portCounter) + ' --rm toontown_alpha:0.0.4')
        data = {"port": str(portCounter), "scene": scene}
        serverData.append(data)
        print(serverData)
        activeServers[scene] = {'port': str(portCounter), 'scene': scene}
    else:
        print("Server instantiation, booting server with requested scene.")
        return {""}

def ClientServerSwap(scene):
    global portCounter
    global serverData
    for server in activeServers:
        if server == scene:
            print("Server already active, sending server info to client.")
            return json.dumps(activeServers[server]) 
            break
    print("Server doesn't currently exist, instantiating server and sending into to client.")
    portCounter = portCounter + 1
    os.system('cmd /c "docker run -dp ' + str(portCounter) + '--rm ToontownAlpha')
    #array = ['{ "port:' + str(portCounter) + ', "scene":' + scene + ' }']
    dic = {"port": portCounter, "scene": scene}
    serverData.append(dic)
    activeServers[scene] = {'port': portCounter, 'scene': scene}
    for server in activeServers:
        if activeServers[scene]['scene'] == scene:
            return json.dumps(activeServers[server])

protocolCode = {
    0 : ServerInstantiate,
    1 : ClientServerSwap
}

async def hello(websocket, path):
    datajson = await websocket.recv()
    print(datajson)
    data = json.loads(datajson)
    print(data["scene"])
    
    #protocolCode[data["protocol"]]()

    if data["protocol"] == 0:
        #message = ServerInstantiate()
        #message = {"port": str(portCounter), "scene": "Scene1"}
        message = json.dumps(serverData.pop(0))
    if data["protocol"] == 1:
        message = ClientServerSwap(data["scene"])

    print("Message:")
    print(message)
    await websocket.send(message)
start_server = websockets.serve(hello, "127.0.0.1", 8080)

#init = ServerInstantiate("Scene1")
#asyncio.get_event_loop().run_until_complete(init)

ServerInstantiate("Scene1")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()