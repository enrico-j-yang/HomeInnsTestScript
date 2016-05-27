#!/bin/sh

SCRIPT_PROC_NUM=$(ps | grep cont_monkey.sh | grep -v grep  | awk '{print $1}')
# check if cont_monkey.sh is running
echo SCRIPT_PROC_NUM:$SCRIPT_PROC_NUM

# if cont_monkey.sh is running, check adb shell dumpstate is running every minute
while test -n "$SCRIPT_PROC_NUM"
do
    echo sleep1m
    sleep 60
    DUMP_STATE=$(ps | grep shell |grep dumpstate | grep -v grep)
    echo 'DUMP_STATE:'$DUMP_STATE
    
# if adb shell dumpstate is running, check whether it finish 
    if test -n "$DUMP_STATE"
    then
	DUMP_STATE_FILE=$(ls dumpstate*.txt)
	echo 'DUMP_STATE_FILE:'$DUMP_STATE_FILE
	DUMP_STATE_END=$(cat $DUMP_STATE_FILE | grep dumpstate | grep done)
	if test -n "$DUMP_STATE_END"
	then 
# if dumpstate file is done but dumpstate process still runs, kill it 
	    PROC_NUM=$(ps | grep shell | grep dumpstate | grep -v grep  | awk '{print $1}')
	    echo 'PROC_NUM:'$PROC_NUM
	    kill $PROC_NUM   	    
        fi
    fi
    SCRIPT_PROC_NUM=$(ps | grep cont_monkey.sh | grep -v grep | awk '{print $1}')
    echo SCRIPT_PROC_NUM:$SCRIPT_PROC_NUM
done
    
# end until cont_monkey.sh finish
