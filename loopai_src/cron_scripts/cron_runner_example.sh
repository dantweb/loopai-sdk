#!/bin/bash
# run like this from container
docker compose exec -T -e RUNNING_CRON=True web python3 app.py --loop /app/var/users/1/loops/7/config/technews_general_news.yaml --user 1 --loopId 7
