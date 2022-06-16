import requests
import json
from datetime import datetime, timedelta
import threading
from time import sleep
import timeit

start = timeit.default_timer()
def get_dates(service_id: str) -> list[datetime]:
    baseurl = 'https://central.qnomy.com/CentralAPI/SearchAvailableDates'
    headers = {
        'Application-Api-Key': '8640a12d-52a7-4c2a-afe1-4411e00e3ac4',
        'Authorization': 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Im92VFc2ckQ4ZmExM1V1cUdKT1BQNkFqa2NMQSJ9.eyJpc3MiOiJodHRwOi8vY2VudHJhbC5xbm9teS5jb20iLCJhdWQiOiJodHRwOi8vY2VudHJhbC5xbm9teS5jb20iLCJuYmYiOjE2NTU0MDA4ODgsImV4cCI6MTY1NjAwNTY4OCwidW5pcXVlX25hbWUiOiI4M2ZjY2FhOC1lNWY3LTQ5M2QtODYwYi1hNjE2MzI4ZWQxNjEiLCJ1aWQiOiJlcU1XNjVGN2RRL0FISmtDODQzRXpRPT0ifQ.gKwcTcWveWsi7x-46VTRaLWga-K4a3j4zN5vAgtJBLGPFNCcMfaILAOLALPDJYuYw_wP6yiCVBbL11tha-M9qRHPH-4nQZjQXTfb9YmhXqSSunghNC--CJiU33aqH5DGWfDlJi7irduGqoOCUPkU9koYce42V2PRFQOusaPo8Vey_L9XjBv2Ms29S63i0YTLyHWkf-cWXUsVJs_KDzrlar-AjKAUmOeOjORSjZbJexAx_vPyPakUjxu4Z6TCJme6UUS0aEMIEwYL_CYqGZiYTDc1PVixV15DP45eQeaQnq-vwz5gxFH7zrOex2QZIs_6t4uZVfYSk9d0Vm-jtFugoQ',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
        'Application-Name': 'myVisit.com v3.5'
    }
    queryString = {
        'serviceId': service_id,
        'startDate': '2022-06-16'
    }

    res = requests.get(baseurl, params=queryString, headers=headers)
    if res.status_code != 200:
        print(res.status_code)
        print(res.text)
        return []
    data = json.loads(res.text)
    dates = []
    if not data['Success'] or data['Results'] is None:
        return []
    for result in data['Results']:
        queryString = {
            'CalendarId': result['calendarId'],
            'ServiceId': service_id,
            'dayPart': 0
        }
        baseurl = 'https://central.qnomy.com/CentralAPI/searchAvailableSlots'
        res = requests.get(baseurl, params=queryString, headers=headers)
        if res.status_code != 200:
            print(res.status_code)
            continue
        times = json.loads(res.text)
        try:
            if times['Results'] is None:
                continue
        except KeyError:
            continue
        for time in times['Results']:
            dates.append(str(
                datetime.strptime(result['calendarDate'], "%Y-%m-%dT00:00:00") + timedelta(minutes=time['Time'])))
    return dates


def get_locations():
    baseurl = 'https://central.qnomy.com/CentralAPI/LocationSearch'
    headers = {
        'Application-Api-Key': '8640a12d-52a7-4c2a-afe1-4411e00e3ac4',
        'Authorization': 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Im92VFc2ckQ4ZmExM1V1cUdKT1BQNkFqa2NMQSJ9.eyJpc3MiOiJodHRwOi8vY2VudHJhbC5xbm9teS5jb20iLCJhdWQiOiJodHRwOi8vY2VudHJhbC5xbm9teS5jb20iLCJuYmYiOjE2NTUzOTIzNTcsImV4cCI6MTY1NTk5NzE1NywidW5pcXVlX25hbWUiOiJiNmYyODFjYS03ODVlLTQ5NjYtYWZkYi1kOTFmN2NkM2JjNDMiLCJ1aWQiOiJRN2cyZDRrK1FZcnFjcGFtV3pyMHp3PT0ifQ.g_Ze127R40j7iEeMLlPJQ2W1UHMqHmfmGwh2LQLz8rVmw90xuc1HFny45GMe0ln1_J7A2q0L1pHXt9a4CkwqxDQ7VnjkAa76b0udMALBqGpZffyMZzJinDsd8JzYKxLPTjYouSM5WgGJJ6fif1dZgumcOcqiCNbupTe2tdWC0koUaSbO6tKRuthPMm-GevUHTg0_NvwEV7URNbxpnrgXZtSAY4drQQAOWKpWmPAnlMhOOxwPGjDBgBP0HnneGimTx45ii4gNRmnX84ShCt-fygrSmqb001aMCpd0Sbtjpd71iGFsScKv0vWWtLa9zgL3d4k3r-qgY0i9qjjIPUqwtQ',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
        'Application-Name': 'myVisit.com v3.5'
    }
    queryString = {
        'currentPage': '1',
        'isFavorite': 'false',
        'orderBy': 'Distance',
        'organizationId': '56',
        'position': '{"lat": "32.1798", "lng": "34.9408", "accuracy": 1440}',
        'resultsInPage': '100',
        'serviceTypeId': '156',
        'src': 'mvws'
    }
    res = requests.get(baseurl, params=queryString, headers=headers)
    if res.status_code != 200:
        print(res.status_code)
        print(res.text)
        return []
    data = json.loads(res.text)
    return data['Results']


def starter(location):
    print(location['LocationName'], get_dates(str(location['ServiceId'])))


if __name__ == '__main__':
    locations = get_locations()
    threads = []
    for location in locations:
        t = threading.Thread(target=lambda: starter(location))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()
    print(f"finished in {timeit.default_timer()-start} seconds.")