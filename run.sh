#!/bin/sh
cd /root/TikTokDownload;
echo "Starting TiktokDownload ..."
if [ ! -f /tmp/pidtiktokd ]
then
        nohup  /root/TikTokDownload/env/bin/python -u main.py > nohup2.out 2>&1 &
        echo $! > /tmp/pidtiktokd;
        echo "TiktokDownload started ..."
else
        /tmp/pidtiktokd=$(cat /tmp/pidtiktokd);
        if ps -p $/tmp/pidtiktokd > /dev/null
        then 
                echo "TiktokDownload is already running ...";
        else
                echo "Inactive";
                nohup /root/TikTokDownload/env/bin/python -u main.py > nohup2.out 2>&1 &
                echo $! > /tmp/pidtiktokd;
        fi
fi