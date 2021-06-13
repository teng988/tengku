#!/bin/bash +x

for pack in Flask PyAudio python-crontab; 
do 
  pip3 list | grep $pack  >/dev/null 2>&1 
  if [ $? -eq 0 ]; then 
    echo "$pack, Installed"; 
  else 
    pip3 install -r requirements.txt
  fi;
done


echo "\n Executing the Script \n";

python3 src/app.py
