import time
import requests
from config import TARGETS

def check_target(target):
    start = time.time()
    try:
        r = requests.get(target["url"], timeout=target["timeout"])
        latency = round((time.time() - start) * 1000, 1)
        return {
            "name": target["name"], "url": target["url"],
            "status": "UP" if r.status_code < 400 else "DOWN",
            "code": r.status_code, "latency_ms": latency
        }
    except requests.exceptions.RequestException as e:
        return {
            "name": target["name"], "url": target["url"],
            "status": "DOWN", "code": None,
            "latency_ms": None, "error": str(e)
        }

def run_checks():
    return [check_target(t) for t in TARGETS]