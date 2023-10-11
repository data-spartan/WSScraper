#!/bin/bash
######COMMAND#######
###initial run: nohup bash live_restart_script.sh > /dev/null 2>&1 &
### ps -ef | grep live_restart_script  to find PID
#### kill it with: kill -9 PID_PROCESS

neofeed_3_live=neofeed-3-live
neofeed_3_sender=neofeed-3-sender

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

### call func only once when rest script is called to check if random ids exist
### ids_random.csv is bind to volume so it okay to run this func outside docker
python3 utils/generate_random_missing_ids.py

while true; do
if [[ ! -z `docker-compose ps | grep Exit` ]]; then

  if [ -z `docker ps -q --no-trunc | grep $(docker-compose ps -q $neofeed_3_live)` ]; then
    docker-compose start $neofeed_3_live
    sleep 1
    fi
  if [ -z `docker ps -q --no-trunc | grep $(docker-compose ps -q $neofeed_3_sender)` ]; then
    docker-compose start $neofeed_3_sender
    sleep 1
    fi
  fi
  sleep 100
done
