from checker import run_checks
from alerts import send_slack_alert
import json, os
import logging

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/uptime.log", level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

STATE_FILE = "logs/state.json"
FAILURE_THRESHOLD = 2  # consecutive fails before we alert

def load_state():
    if os.path.exists(STATE_FILE):
        return json.load(open(STATE_FILE))
    return {}

def save_state(state):
    os.makedirs("logs", exist_ok=True)
    json.dump(state, open(STATE_FILE, "w"))

def main():
    results = run_checks()
    state = load_state()

    for r in results:
        key = r["name"]
        fails = state.get(key, 0)

        logging.info(f"{r['name']} status={r['status']} latency={r.get('latency_ms')}ms")

        if r["status"] == "DOWN":
            fails += 1
        else:
            if fails >= FAILURE_THRESHOLD:
                send_slack_alert(f"✅ RECOVERED: {key} is back up.")
            fails = 0
        state[key] = fails

        if fails == FAILURE_THRESHOLD:
            msg = f"🚨 DOWN: {key} ({r['url']}) — {r.get('error', r.get('code'))}"
            send_slack_alert(msg)

    save_state(state)
    print(json.dumps(results, indent=2))

if name == "__main__":
    main()