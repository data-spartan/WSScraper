# WSScraper

HINT: Using .gitkeep to keep logs and raw_missing dirs but to exclude files inside

Deploying steps:

1. Install redis db;
2. Disable redis port for any internet connection to prevent intrusion
3. Install and configure docker
4. Install, configure, test, run Kafka server
5. Configure gitlab logbroker(kafka consumer) on same server
6. Clone the project logbroker on same server
7. Build,start logbroker docker images and containers
8. Integrate Kafka and Slack
9. Configure gitlab neofeed_3_live on server
10. Clone the project neofeed_3_live
11. Run live_restart_script.sh to generate logs files, ids_random.csv pool of missing ids and run in background indefinitely
12. Build,start neofeed_3_live docker images and containers
13. Check logs main.log and sender.log
