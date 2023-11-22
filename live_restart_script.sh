#!/bin/bash
######COMMAND#######
###initial run: nohup bash live_restart_script.sh > /dev/null 2>&1 &
### ps -ef | grep live_restart_script  to find PID
#### kill it with: kill -9 PID_PROCESS

ws-scraper-live=ws-scraper-live
ws-scraper-sender=ws-scraper-sender

main_logs=logs/main.log
sender_logs=logs/sender.log

if ! [[ -e "$main_logs" ]];
then
    touch 'logs/main.log'
    chmod 666 $main_logs
fi
if ! [[ -e "$sender_logs" ]];
then
    touch 'logs/sender.log'
    chmod 666 $sender_logs
fi

while true; do
if [[ ! -z `docker-compose ps | grep Exit` ]]; then

  if [ -z `docker ps -q --no-trunc | grep $(docker-compose ps -q $ws-scraper-live)` ]; then
    docker-compose start $ws-scraper-live
    sleep 1
    fi
  if [ -z `docker ps -q --no-trunc | grep $(docker-compose ps -q $ws-scraper-sender)` ]; then
    docker-compose start $ws-scraper-sender
    sleep 1
    fi
  fi
  sleep 30
done
