import logging
import requests, json
import azure.functions as func
import time
from datetime import timedelta
from datetime import datetime

rest980ApiIp = '192.168.1.101'
rest980ApiPort = '3000'
# set initial paused at some time far in the past
paused_at = datetime.now() + timedelta(days=-42)

def main(req: func.HttpRequest) -> func.HttpResponse:
    # logging.info('Python HTTP trigger function processed a request.')

    mission = requests.get(f"http://{rest980ApiIp}:{rest980ApiPort}/api/local/info/mission")

    j = json.loads(mission.text)
    cycle = j['cleanMissionStatus']['cycle']
    phase = j['cleanMissionStatus']['phase']
    # 30% or 40% is low on battery
    batPct = j['batPct']
    binFull = j['bin']['full'] == 'true'

    # phase = 'running'

    now = datetime.now()
    global paused_at
    action = None
    if phase == 'charge' and batPct < 50:
        logging.info(f'Roomba is charging, not taking any actions')    
    # dock if double tapping - if last action was pause and less than 5 seconds ago
    elif now - paused_at < timedelta(seconds=5):
        action = 'dock'
        # wait a few seconds to not confuse the robot
        time.sleep(5)
    # if stopped and bin is not full
    elif phase == 'stop' or phase == 'charge' and not binFull:
        if cycle == 'none':
            # docked or on pause for too long
            action = 'start'
        else:
            action = 'resume'
    else:
        # if already running pause
        paused_at = now
        action = 'pause'

    # TODO: what if phase is hmUsrDock, ie. returning to dock
    if action:
        logging.info(f"action: {action}")
        response = requests.get(f"http://{rest980ApiIp}:{rest980ApiPort}/api/local/action/{action}")
    else:
        # for logging purposes we set action to string 'none'
        action = 'none'

    return func.HttpResponse(f"battery: {batPct}%, is bin full: {binFull}, cycle: {cycle}, phase: {phase}, action: {action}, ran at: {now}, last paused: {paused_at}", status_code=200)
