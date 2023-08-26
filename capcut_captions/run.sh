#!/bin/sh
cd /root/artlist-crawl;
echo "Starting Proc ..."
if [ ! -f /tmp/pid-cc ]
then
        nohup /root/artlist-crawl/env/bin/python -u  craw_artlist.py > nohup2.out &
        echo $! > /tmp/pid-cc;
        echo "Proc started ..."
else
        /tmp/pid-cc=$(cat /tmp/pid-cc);
         if ps -p $PID > /dev/null
        then
                echo "Proc is already running ...";
        else
                echo "Inactive";
                nohup /root/artlist-crawl/env/bin/python -u  craw_artlist.py > nohup2.out &
                echo $! > /tmp/pid-cc;
        fi
fi
