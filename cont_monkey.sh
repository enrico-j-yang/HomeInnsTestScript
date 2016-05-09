#!/bin/sh

DEVICE_SN='CDRTCYC3Y16CFDXG'
#ADB_DEVICE="adb -s "$DEVICE_SN
ADB_DEVICE="adb"
#echo $ADB_DEVICE
#MONKEY_SEED='-s 1234567890'
RUN_TIME=500000
EVENT_EXERCUTED=0

if [ $# -gt 1 ]
then
	echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
	echo "!!         输入参数不正确         !!"
	echo "!!      导出失败，未生成文件      !!"
	echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"

	exit 1
fi
if [ $# -eq 1 ]
then
	DATETIME=$(echo $1 | cut -d _ -f 3 | cut -d . -f 1)
	echo "*****analyse monkey log*****"
	RANDOM_SEED=$(cat monkey_log_$DATETIME.txt | grep -o 'seed=[0-9]*' | cut -d = -f 2)
	EVENT_COUNT=$(cat monkey_log_$DATETIME.txt | grep -o 'at event [0-9]*' | awk '{print $3}')
	if test -z "$EVENT_COUNT" ;then
		EVENT_COUNT=0
		mkdir -p unknown
		cd unknown
		mkdir -p $DATETIME
		cd ..
		mv monkey_log_$DATETIME.txt unknown/$DATETIME
		$ADB_DEVICE pull /data/tombstone/ unknown/$DATETIME/
		$ADB_DEVICE pull /data/system/dropbox/ unknown/$DATETIME/
		$ADB_DEVICE shell rm -f /data/tombstones/*
		$ADB_DEVICE shell rm -f /data/system/dropbox/*
	fi
	echo 'random seed:'$RANDOM_SEED
	echo 'event count:'$EVENT_COUNT
	EVENT_EXERCUTED=$(($EVENT_EXERCUTED+$EVENT_COUNT))
	echo 'event exercuted:'$EVENT_EXERCUTED
	ERROR_INFO=$(cat monkey_log_$DATETIME.txt | grep 'ANR in')
	if test -n "$ERROR_INFO" ;then
		echo 'error cause:ANR'
		mkdir -p ANR
		cd ANR
		ERROR_POS=$(echo $ERROR_INFO | cut -d \/ -f 2 | cut -d \) -f 1 | cut -d . -f 2)
		ERROR_INFO=$(echo $ERROR_INFO | awk '{print $3}')
		mkdir -p $ERROR_INFO
		cd $ERROR_INFO
		mkdir -p $ERROR_POS
		cd $ERROR_POS
		mkdir -p $DATETIME
		cd ..
		cd ..
		cd ..
		mv monkey_log_$DATETIME.txt ANR/$ERROR_INFO/$ERROR_POS/$DATETIME/
		$ADB_DEVICE pull /data/tombstone/ ANR/$ERROR_INFO/$ERROR_POS/$DATETIME/
		$ADB_DEVICE pull /data/system/dropbox/ ANR/$ERROR_INFO/$ERROR_POS/$DATETIME/
		$ADB_DEVICE shell rm -f /data/tombstones/*
		$ADB_DEVICE shell rm -f /data/system/dropbox/*
	fi
	if test -z "$ERROR_INFO" ;then
		ERROR_INFO=$(cat monkey_log_$DATETIME.txt | grep 'CRASH:')
		if test -n "$ERROR_INFO" ;then
			ERROR_POS=$(cat monkey_log_$DATETIME.txt | grep '.java:' | head -1 | awk '{printf $3}')
			if test -n "$ERROR_POS" ;then
				echo 'error cause:CRASH'
				echo 'error position:'$ERROR_POS
				mkdir -p CRASH
				cd CRASH
				mkdir -p $ERROR_POS
				cd $ERROR_POS
				mkdir -p $DATETIME
				cd ..
				cd ..
				mv monkey_log_$DATETIME.txt CRASH/$ERROR_POS/$DATETIME/
				$ADB_DEVICE pull /data/tombstone/ CRASH/$ERROR_POS/$DATETIME/
				$ADB_DEVICE pull /data/system/dropbox/ CRASH/$ERROR_POS/$DATETIME/
				$ADB_DEVICE shell rm -f /data/tombstones/*
				$ADB_DEVICE shell rm -f /data/system/dropbox/*
			fi
		fi
	fi

	echo 'error cause:'$ERROR_INFO
fi
if [ $# -eq 0 ]
then
	while [ $EVENT_EXERCUTED -le $RUN_TIME ]
	do
		# reboot devices for next run
		echo "*****reboot device*****"
		$ADB_DEVICE kill-server
		$ADB_DEVICE reboot
		# wait for device connection
		echo "*****wait for device*****"
		$ADB_DEVICE wait-for-device
		# run monkey with a random seed
		if test -z "$MONKEY_SEED" ;then
			echo "*****run monkey with a random seed*****"
		fi
		if test -n "$MONKEY_SEED" ;then
			echo "****run monkey with specified seed" $MONKEY_SEED "*****"
		fi
		DATETIME=`date +%Y%m%d-%H%M%S`
		#DATETIME='20160505-211209'
		$ADB_DEVICE shell monkey --pkg-blacklist-file /data/blacklist.txt --pct-trackball 0 $MONKEY_SEED -v -v -v $RUN_TIME > monkey_log_$DATETIME.txt
		# analyse monkey log, figure out error catagory and pull log to pc
		echo "*****analyse monkey log*****"
		RANDOM_SEED=$(cat monkey_log_$DATETIME.txt | grep -o 'seed=[0-9]*' | cut -d = -f 2)
		EVENT_COUNT=$(cat monkey_log_$DATETIME.txt | grep -o 'at event [0-9]*' | awk '{print $3}')
		if test -z "$EVENT_COUNT" ;then
			EVENT_COUNT=0
			mkdir -p unknown
			cd unknown
			mkdir -p $DATETIME
			cd ..
			mv monkey_log_$DATETIME.txt unknown/$DATETIME
			$ADB_DEVICE pull /data/tombstone/ unknown/$DATETIME/
			$ADB_DEVICE pull /data/system/dropbox/ unknown/$DATETIME/
			$ADB_DEVICE shell /system/bin/screencap -p /sdcard/screenshot.png
			$ADB_DEVICE pull /sdcard/screenshot.png unknown/$DATETIME/
			$ADB_DEVICE shell rm -f /data/tombstones/*
			$ADB_DEVICE shell rm -f /data/system/dropbox/*
		fi
		echo 'random seed:'$RANDOM_SEED
		echo 'event count:'$EVENT_COUNT
		EVENT_EXERCUTED=$(($EVENT_EXERCUTED+$EVENT_COUNT))
		echo 'event exercuted:'$EVENT_EXERCUTED
		ERROR_INFO=$(cat monkey_log_$DATETIME.txt | grep 'ANR in')
		if test -n "$ERROR_INFO" ;then
			echo 'error cause:ANR'
			mkdir -p ANR
			cd ANR
			ERROR_POS=$(echo $ERROR_INFO | cut -d \/ -f 2 | cut -d \) -f 1 | cut -d . -f 2)
			ERROR_INFO=$(echo $ERROR_INFO | awk '{print $3}')
			mkdir -p $ERROR_INFO
			cd $ERROR_INFO
			mkdir -p $ERROR_POS
			cd $ERROR_POS
			mkdir -p $DATETIME
			cd ..
			cd ..
			cd ..
			mv monkey_log_$DATETIME.txt ANR/$ERROR_INFO/$ERROR_POS/$DATETIME/
			$ADB_DEVICE pull /data/tombstone/ ANR/$ERROR_INFO/$ERROR_POS/$DATETIME/
			$ADB_DEVICE pull /data/system/dropbox/ ANR/$ERROR_INFO/$ERROR_POS/$DATETIME/
			$ADB_DEVICE shell /system/bin/screencap -p /sdcard/screenshot.png
			$ADB_DEVICE pull /sdcard/screenshot.png ANR/$ERROR_INFO/$ERROR_POS/$DATETIME/
			$ADB_DEVICE shell rm -f /data/tombstones/*
			$ADB_DEVICE shell rm -f /data/system/dropbox/*
		fi
		if test -z "$ERROR_INFO" ;then
			ERROR_INFO=$(cat monkey_log_$DATETIME.txt | grep 'CRASH:')
			if test -n "$ERROR_INFO" ;then
				ERROR_POS=$(cat monkey_log_$DATETIME.txt | grep '.java:' | head -1 | awk '{printf $3}')
				if test -n "$ERROR_POS" ;then
					echo 'error cause:CRASH'
					echo 'error position:'$ERROR_POS
					mkdir -p CRASH
					cd CRASH
					mkdir -p $ERROR_POS
					cd $ERROR_POS
					mkdir -p $DATETIME
					cd ..
					cd ..
					mv monkey_log_$DATETIME.txt CRASH/$ERROR_POS/$DATETIME/
					$ADB_DEVICE pull /data/tombstone/ CRASH/$ERROR_POS/$DATETIME/
					$ADB_DEVICE pull /data/system/dropbox/ CRASH/$ERROR_POS/$DATETIME/
					$ADB_DEVICE shell /system/bin/screencap -p /sdcard/screenshot.png
					$ADB_DEVICE pull /sdcard/screenshot.png CRASH/$ERROR_POS/$DATETIME/
					$ADB_DEVICE shell rm -f /data/tombstones/*
					$ADB_DEVICE shell rm -f /data/system/dropbox/*
				fi
			fi
		fi

	done
fi