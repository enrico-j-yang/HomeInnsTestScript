#!/bin/sh

function wftCat(){
    echo error cause:WTF
    cd $LOGPATH
    mkdir -p WTF
    cd WTF
    ERROR_MODULE=$(cat ../../$LOG_FILE | grep Process: | head -1 | awk '{print $2}')
    ERROR_POS=$(cat ../../$LOG_FILE | grep .java | head -1 | awk '{print $2}')
    if test -z "$ERROR_POS"
    then
        ERROR_POS=$(cat ../../$LOG_FILE | grep at  | head -1 | awk '{print $2}')
    fi
echo $ERROR_MODULE
echo $ERROR_POS
    mkdir -p $ERROR_MODULE
    cd $ERROR_MODULE
    mkdir -p $ERROR_POS
    cd $ERROR_POS
    cd ..
    cd ..
    cd ..
    cd ..
    LOGPATH=$LOGPATH/WTF/$ERROR_MODULE/$ERROR_POS
echo $LOG_FILE $LOGPATH/
    mv $LOG_FILE $LOGPATH/
}

function unknownCat(){
	echo unknown reason interruption
	mkdir -p unknown
	cd unknown
    cd ..
	LOGPATH=unknown
#echo $LOG_FILE $LOGPATH/
	mv $LOG_FILE $LOGPATH/
}

function anrCat(){
	echo error cause:ANR
    cd $LOGPATH
	mkdir -p ANR
	cd ANR
    ERROR_MODULE=$(cat ../../$LOG_FILE | grep Package: | head -1 | awk '{print $2}')
    ERROR_POS=$(cat ../../$LOG_FILE | grep .java | head -1 | awk '{print $2}')
    #echo $ERROR_MODULE
    #echo $ERROR_POS
    mkdir -p $ERROR_MODULE
	cd $ERROR_MODULE
	mkdir -p $ERROR_POS
	cd $ERROR_POS
    cd ..
	cd ..
    cd ..
    cd ..
    LOGPATH=$LOGPATH/ANR/$ERROR_MODULE/$ERROR_POS
    #echo $LOG_FILE $LOGPATH/
    mv $LOG_FILE $LOGPATH/
}

function crashCat(){
    echo error cause:CRASH
    cd $LOGPATH
    mkdir -p CRASH
    cd CRASH
    ERROR_MODULE=$(cat ../../$LOG_FILE | grep Package: | head -1 | awk '{print $2}')
    ERROR_POS=$(cat ../../$LOG_FILE | grep .java | head -1 | awk '{print $2}')
    if test -z "$ERROR_POS"
    then
        ERROR_POS=$(cat ../../$LOG_FILE | grep at  | head -1 | awk '{print $2}')
    fi
echo $ERROR_MODULE
echo $ERROR_POS
    mkdir -p $ERROR_MODULE
    cd $ERROR_MODULE
    mkdir -p $ERROR_POS
    cd $ERROR_POS
    cd ..
    cd ..
    cd ..
    cd ..
    LOGPATH=$LOGPATH/CRASH/$ERROR_MODULE/$ERROR_POS
#echo $LOG_FILE $LOGPATH/
    mv $LOG_FILE $LOGPATH/
}

for i in *.txt
do
LOG_FILE=$i
echo $LOG_FILE
LOG_MODULE=$(echo $LOG_FILE | cut -d _ -f 2)
#echo $LOG_MODULE
LOG_CAT=$(echo $LOG_FILE | cut -d _ -f 3 | cut -d @ -f 1)
#echo $LOG_CAT

# process monkey log file only

echo "*****analyse log*****"

if test -z "$LOG_MODULE" ;then
    unknownCat
elif [ "$LOG_MODULE" == 'server' ]; then
    LOGPATH=server
    mkdir -p $LOGPATH
    if [ "$LOG_CAT" == "anr" ]; then
        anrCat
    elif [ "$LOG_CAT" == "crash" ]; then
        crashCat
    elif [ "$LOG_CAT" == "wtf" ];then
        wftCat
    else
        unknownCat
    fi

elif [ "$LOG_MODULE" == "app" ];then
    LOGPATH=app
    mkdir -p $LOGPATH
    if [ "$LOG_CAT" == "anr" ]; then
        anrCat
    elif [ "$LOG_CAT" == "crash" ]; then
        crashCat
    elif [ "$LOG_CAT" == "wtf" ];then
        wftCat
    else
        unknownCat
    fi

else
    unknownCat
fi

done




