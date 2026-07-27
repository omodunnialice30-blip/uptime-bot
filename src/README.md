# Uptime Bot with Alerts

A lightweight uptime monitoring bot that checks a list of websites/APIs on a schedule and sends Slack alerts when something goes down — and when it recovers.

Built as part of a DevOps capstone project (DO-12).

## Problem it solves

Outages often go unnoticed until a user complains. This bot continuously checks target URLs and proactively alerts a Slack channel the moment something crosses a failure threshold, so issues get caught early.

## How it works

1. **`src/checker.py`** — sends an HTTP request to each target URL, records status (UP/DOWN), response code, and latency.
2. `src/alerts.py` — posts a message to a Slack channel via an Incoming Webhook.
3.er → New File → nam— orchestrates the above: runs checks, tracks consecutive failures per target inname it README.md ( and only alerts once a target has failedp-level uptime-bot fotimes in a row (avoids alert spam from single blips). Also sends a "recovered" message when a target comes back up.
4. GitHub Actions (`.github/workflows/monitor.yml`) runs the bot automatically every 10 minutes via cron, with state persisted between runs using actions/cache so the failure count isn't reset each run.
5.vel uptime-b— the bot is containerized for portable, consistent execution.

## Architecture

GitHub Actions (cron, every 10 min) │ ▼ checkout code → install deps → restore cached state │ ▼ src/main.py ├── checker.py → HTTP GET each target → UP/DOWN + latency ├── (state.json)→ tracks consecutive failures per target └── alerts.py → POST to Slack Incoming Webhook (on threshold breach / recovery) │ ▼ save state to cache for next run │ ▼ logs/uptime.log (structured, timestamped)
## Tech stack

- Python 3.11,ains. This b- Docker
- GitHub Actions (CI/CD + scheduling)
- Slack Incoming Webhooks

## Running locally

```bash
export SLACK_WEBHOOK_URL="your-webhook-url-here"
cd src
python3 main.py
Running with Docker
docker build -t uptime-bot .
docker run --rm -e SLACK_WEBHOOK_URL="your-webhook-url-here" uptime-bot
Running automatically (production)
Handled by .github/workflows/monitor.yml — runs every 10 minutes on GitHub’s infrastructure. No manual intervention needed. Can also be triggered manually from the Actions tab (workflow_dispatch).
Configuration
Targets are defined in src/config.py:
TARGETS = [
    {"name": "Main Website", "url": "https://example.com", "timeout": 5},
]
FAILURE_THRESHOLD = 2  # consecutive failures before alerting
Add/edit entries here to monitor your own sites.
Secrets
SLACK_WEBHOOK_URL is never hardcoded — it’s read from an environment variable locally/in Docker, and stored as a GitHub Actions repository secret in production.
Known limitations / future improvements
Base Docker image currently has 1 flagged critical vulnerability (common in base images) — could add automated container scanning (e.g. Trivy) in CI as a stretch goal
No persistent dashboard yet — could add Prometheus + Grafana for historical uptime visualization
Currently monitors HTTP(S) endpoints only
