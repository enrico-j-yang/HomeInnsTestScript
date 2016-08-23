#!/bin/sh

#DEVICE_SN='CDRTCYC3Y16CFDXG'
#ADB_DEVICE="adb -s "$DEVICE_SN
ADB_DEVICE="adb"
#echo $ADB_DEVICE
#MONKEY_SEED='-s 1234567890'
RUN_TIME=1
EVENT_EXERCUTED=0

function normalCat(){
	echo *****normal finish*****
	mkdir -p normal
	LOGPATH=normal/
}

function unknownCat(){
	echo *****unknown reason interruption*****
	mkdir -p unknown
	cd unknown
	mkdir -p $DATETIME
	cd ..
	LOGPATH=unknown/$DATETIME/
}

function anrCat(){
	echo *****error cause:ANR*****
	mkdir -p ANR
	cd ANR
	ERROR_POS=$(echo $ERROR_INFO | cut -d \/ -f 2 | cut -d \) -f 1 | awk -F . '{print $NF}')
	ERROR_MODULE=$(echo $ERROR_INFO | awk '{print $3}')
	mkdir -p $ERROR_MODULE
	cd $ERROR_MODULE
	mkdir -p $ERROR_POS
	cd $ERROR_POS
	mkdir -p $DATETIME
	cd ..
	cd ..
	cd ..
	LOGPATH=ANR/$ERROR_MODULE/$ERROR_POS/$DATETIME/
}

function crashCat(){
	echo *****error cause:CRASH*****
	ERROR_MODULE=$(cat monkey_log_$DATETIME.txt | grep 'CRASH:' | awk '{printf $3}')
	ERROR_POS=$(cat monkey_log_$DATETIME.txt | grep '.java:' | head -1 | awk '{printf $3}' | cut -d \( -f 1)
	if test -n "$ERROR_POS" ;then
		echo 'error cause:CRASH'
		echo 'error position:'$ERROR_POS
		mkdir -p CRASH
		cd CRASH
		mkdir -p $ERROR_MODULE
		cd $ERROR_MODULE
		mkdir -p $ERROR_POS
		cd $ERROR_POS
		mkdir -p $DATETIME
		cd ..
		cd ..
		cd ..
		LOGPATH=CRASH/$ERROR_MODULE/$ERROR_POS/$DATETIME/
	fi
}

function moveMonkeyLog(){
	FILE_SIZE=$(wc -c monkey_log_$DATETIME.txt | awk '{print int($1/1024/1024)}')
	#echo 'FILE_SIZE:'$FILE_SIZE
	if test $FILE_SIZE -gt 10
	then
		zip monkey_log_$DATETIME.zip monkey_log_$DATETIME.txt
		mv monkey_log_$DATETIME.zip $LOGPATH
		rm monkey_log_$DATETIME.txt
	else
		mv monkey_log_$DATETIME.txt $LOGPATH
	fi

}

function pullLogAndMove(){
	$ADB_DEVICE pull /data/system/dropbox/ $LOGPATH
	cd $LOGPATH
	mkdir -p log
	cp -f *_anr* *_crash* log/
	rm *@*
	cp -f log/* .
	rm -rf log
	cd -
	$ADB_DEVICE pull /data/tombstones/ $LOGPATH
	$ADB_DEVICE shell rm -f /data/tombstones/*
	$ADB_DEVICE shell rm -f /data/system/dropbox/*
	$ADB_DEVICE shell /system/bin/screencap -p /sdcard/screenshot.png
	$ADB_DEVICE pull /sdcard/screenshot.png $LOGPATH

	#echo $PWD
	FILE_SIZE=$(wc -c main_log_$DATETIME.txt | awk '{print int($1/1024/1024)}')
	#echo 'FILE_SIZE:'$FILE_SIZE
	if test $FILE_SIZE -gt 10
	then
		zip main_log_$DATETIME.zip main_log_$DATETIME.txt
		mv main_log_$DATETIME.zip $LOGPATH
		rm main_log_$DATETIME.txt
	else
		mv main_log_$DATETIME.txt $LOGPATH
	fi
	FILE_SIZE=$(wc -c event_log_$DATETIME.txt | awk '{print int($1/1024/1024)}')
	#echo 'FILE_SIZE:'$FILE_SIZE
	if test $FILE_SIZE -gt 10
	then
		zip event_log_$DATETIME.zip event_log_$DATETIME.txt
		mv event_log_$DATETIME.zip $LOGPATH
		rm event_log_$DATETIME.txt
	else
		mv event_log_$DATETIME.txt $LOGPATH
	fi

}

function dumpstateAndMove(){
	FILE_SIZE=$(wc -c dumpstate_$DATETIME.txt | awk '{print int($1/1024/1024)}')
	#echo 'FILE_SIZE:'$FILE_SIZE
	if test $FILE_SIZE -gt 10
	then
		zip dumpstate_$DATETIME.zip dumpstate_$DATETIME.txt
		mv dumpstate_$DATETIME.zip $LOGPATH
		rm dumpstate_$DATETIME.txt
	else
		mv dumpstate_$DATETIME.txt $LOGPATH
	fi

}

while getopts "r:n:l:s:" arg
do
	case $arg in
	l ) #echo $OPTARG
		DATETIME=$(echo $OPTARG | cut -d _ -f 3 | cut -d . -f 1)
		#echo $DATETIME
	;;
	r ) #echo $OPTARG
		if test -z "$DATETIME"
		then
			RUN_TIME=$OPTARG
		fi
		#echo 'RUN_TIME:'$RUN_TIME
	;;
	n ) #echo $OPTARG
		if test -z "$DATETIME"
		then
			DEVICE_SN=$OPTARG
			ADB_DEVICE="adb -s "$DEVICE_SN
		fi
		#echo 'DEVICE_SN:'$DEVICE_SN
	;;
	s ) #echo $OPTARG
		if test -z "$DATETIME"
		then
			MONKEY_SEED='-s '$OPTARG
		fi
		#echo 'MONKEY_SEED:'$MONKEY_SEED
	;;
	? ) echo usage:
		echo 'script will run 1 time if no arg found'
        echo 
		echo '-l \<monkey log file\ >				- analyse monkey log file. log file name should be monkey_log_yyyymmdd-hhmmss.txt'
		echo '-r \<monkey event count\ >			- specified monkey test event count'
		echo '-n \<device hardware sn\ >			- specified device sn for ads'
		echo '-s \<monkey test seed\ >				- specified monkey test seed'
		exit 1
	;;
	esac
done

#echo 'DATETIME:'$DATETIME
# process monkey log file only
if test -n "$DATETIME"
then
	echo "*****analyse monkey log*****"
	RANDOM_SEED=$(cat monkey_log_$DATETIME.txt | grep -o 'seed=[0-9]*' | cut -d = -f 2)
	EVENT_COUNT=$(cat monkey_log_$DATETIME.txt | grep -o 'Events injected: [0-9]*' | awk '{print $3}')
	if test -z "$EVENT_COUNT" ;then
		EVENT_COUNT=0
		unknownCat
	fi
	echo 'random seed:'$RANDOM_SEED
	echo 'event count:'$EVENT_COUNT
	EVENT_EXERCUTED=$(($EVENT_EXERCUTED+$EVENT_COUNT))
	echo 'event exercuted:'$EVENT_EXERCUTED
	ERROR_INFO=$(cat monkey_log_$DATETIME.txt | grep 'ANR in')
	if test -n "$ERROR_INFO" ;then
		anrCat
		moveMonkeyLog
	fi
	if test -z "$ERROR_INFO" ;then
		ERROR_INFO=$(cat monkey_log_$DATETIME.txt | grep 'CRASH:')
		if test -n "$ERROR_INFO" ;then
			crashCat
			moveMonkeyLog
		fi
		if test -z "$ERROR_INFO" ;then
			normalCat
			moveMonkeyLog
		fi
	fi

	# run monkey for specified events count
else
	if test -z “$RUN_TIME”
	then
		echo RUN_TIME is null
		exit 1
	fi

	while test $EVENT_EXERCUTED -lt $RUN_TIME
	do
        # set volume to 1 so as to prevent fm annoying sound
        for((i=1;i<=5;i++))
        do
            $ADB_DEVICE shell input keyevent 4
        done
        $ADB_DEVICE shell input keyevent 66
        $ADB_DEVICE shell input keyevent 21
        $ADB_DEVICE shell input keyevent 21
        $ADB_DEVICE shell input keyevent 66
        $ADB_DEVICE shell input keyevent 66
        for((i=1;i<=15;i++))
        do
            $ADB_DEVICE shell input keyevent 21
        done
        $ADB_DEVICE shell input keyevent 22
		# reboot devices for next run
		echo "*****reboot device*****"
		$ADB_DEVICE kill-server
		$ADB_DEVICE reboot
		# wait for device connection
		echo "*****wait for device*****"
		$ADB_DEVICE wait-for-device
		$ADB_DEVICE push blacklist.txt /data/
		# run monkey with a random seed
		if test -z "$MONKEY_SEED" ;then
			echo "*****run monkey with a random seed*****"
		fi
		if test -n "$MONKEY_SEED" ;then
			echo "****run monkey with specified seed" $MONKEY_SEED "*****"
		fi
		DATETIME=`date +%Y%m%d-%H%M%S`
		nohup $ADB_DEVICE logcat *:W > main_log_$DATETIME.txt &
		nohup $ADB_DEVICE logcat -b events -v time > event_log_$DATETIME.txt &
		#--pct-touch 18 --pct-motion 12 --pct-pinchzoom 2 --pct-trackball 0 --pct-nav 30 --pct-majornav 18 --pct-syskeys 2 --pct-appswitch 2 --pct-flip 1 --pct-anyevent 15 --throttle 50
#$ADB_DEVICE shell monkey --pkg-blacklist-file /data/blacklist.txt --pct-touch 0 --pct-trackball 0 --throttle 50 $MONKEY_SEED -v -v -v $RUN_TIME > monkey_log_$DATETIME.txt
$ADB_DEVICE shell monkey --pkg-blacklist-file /data/blacklist.txt --pct-majornav 40 --pct-nav 30 --pct-syskeys 20 --throttle 50 --pct-appswitch 5 --pct-anyevent 5 $MONKEY_SEED -v -v -v $RUN_TIME > monkey_log_$DATETIME.txt

		# analyse monkey log, figure out error catagory and pull log to pc
		echo "*****analyse monkey log*****"
		RANDOM_SEED=$(cat monkey_log_$DATETIME.txt | grep -o 'seed=[0-9]*' | cut -d = -f 2)
		EVENT_COUNT=$(cat monkey_log_$DATETIME.txt | grep -o 'Events injected: [0-9]*' | awk '{print $3}')
		if test -z "$EVENT_COUNT" ;then
			EVENT_COUNT=0
			unknownCat
			moveMonkeyLog
			pullLogAndMove
			$ADB_DEVICE shell dumpstate > dumpstate_$DATETIME.txt
			dumpstateAndMove
		fi
		echo 'random seed:'$RANDOM_SEED
		echo 'event count:'$EVENT_COUNT
		EVENT_EXERCUTED=$(($EVENT_EXERCUTED+$EVENT_COUNT))
		echo 'event exercuted:'$EVENT_EXERCUTED
		ERROR_INFO=$(cat monkey_log_$DATETIME.txt | grep 'ANR in')
		if test -n "$ERROR_INFO" ;then
			anrCat
			moveMonkeyLog
			pullLogAndMove
			$ADB_DEVICE shell dumpstate > dumpstate_$DATETIME.txt
			dumpstateAndMove
		fi
		if test -z "$ERROR_INFO" ;then
			ERROR_INFO=$(cat monkey_log_$DATETIME.txt | grep 'CRASH:')
			if test -n "$ERROR_INFO" ;then
				crashCat
				moveMonkeyLog
				pullLogAndMove
				$ADB_DEVICE shell dumpstate > dumpstate_$DATETIME.txt
				dumpstateAndMove
			fi
			if test -z "$ERROR_INFO" ;then
				normalCat
				moveMonkeyLog
				pullLogAndMove
			fi
		fi

	done
fi


