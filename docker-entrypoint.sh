if [ $SWITCH = 'sender' ]
then
  python3 -u sender.py
elif [ $SWITCH = 'live' ]
then
  python3 -u  main.py
fi