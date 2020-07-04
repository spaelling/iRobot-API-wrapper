import logging
import requests, json
import azure.functions as func

rest980ApiIp = '192.168.1.101'
rest980ApiPort = '3000'

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    mission = requests.get(f"http://{rest980ApiIp}:{rest980ApiPort}/api/local/info/mission")

    j = json.loads(mission.text)
    cycle = j['cleanMissionStatus']['cycle']
    phase = j['cleanMissionStatus']['phase']

    if cycle == 'none':
        if phase == 'stop':
            # docked or on pause for too long
            action = 'start'
    else:
        action = 'resume'
    
    # response = requests.get(f"http://{rest980ApiIp}:{rest980ApiPort}/api/local/action/{action}")

    return func.HttpResponse(f"cycle: {cycle}, phase: {phase}, action: {action}", status_code=200)
