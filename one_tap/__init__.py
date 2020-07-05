import logging
import requests, json, datetime
import azure.functions as func

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
    # dock if double tapping - if last action was pause and less than 5 seconds ago
    if now - paused_at < timedelta(seconds=5):
        action = 'dock'
    # if stopped and battery more than 50% and bin is not full
    elif phase == 'stop' and batPct >= 50 and not binFull:
        if cycle == 'none':
            # docked or on pause for too long
            action = 'start'
        elif phase == 'paused':
            action = 'resume'
    else:
        if phase == 'charge':
            logging.info(f'Roomba is charging, not taking any actions')
        else:
            # if already running pause
            paused_at = now
            action = 'pause'

    if action:
        logging.info(f"action: {action}")
        # response = requests.get(f"http://{rest980ApiIp}:{rest980ApiPort}/api/local/action/{action}")
    else:
        # for logging purposes we set action to string 'none'
        action = 'none'

    return func.HttpResponse(f"battery: {batPct}%, is bin full: {binFull}, cycle: {cycle}, phase: {phase}, action: {action}, ran at: {now}, last paused: {paused_at}", status_code=200)
