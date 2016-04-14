#!/bin/bash 
## if the error exceeds its limit in the specified managed server it will add record in file named record to be sent to L2 Support team
## this file will be formated as error_name managed server name current error of count
## then script will find if the file contains errors it will read from file and send it to L2 Support Team
#set -x

source alert_logs_env.sh 

printFile ()
{
    echo '<br>' > $ERROR_RESULT_FILE;
    echo '<p>' >> $ERROR_RESULT_FILE;
    echo '<table border='1' width='90%' align='center' >' >> $ERROR_RESULT_FILE;
    echo '<tr><th scope="col">Error Name</th>' >>$ERROR_RESULT_FILE
    echo '<th scope="col">Count </th> </tr>'>>$ERROR_RESULT_FILE;
    echo '</p>'>>$ERROR_RESULT_FILE
}


echo the script now is started at the following time $START

> $ERROR_RESULT_FILE
cd $LOG_DIR
#printFile
echo "		------------------------- Application: Errors Daily Report -------------------------	 	" >> $ERROR_RESULT_FILE
echo 

cat  $KNOWN_ERRORS_FILE | while read error
do
        echo "$error"
        error_name=`echo $error | cut -d'$' -f1`
        error_string=`echo $error | cut -d'$' -f2`
        error_limit=`echo $error | cut -d'$' -f3 `
        echo $error_string $error_string $error_limit
	FINAL_COUNT=0
        for server in $MANAGED_SERVERS
		
        do
                echo $error_string
		unset COUNT_ERROR
                COUNT_ERROR=`grep -i $error_string $BEA_LOGS_PATH/$server/logs/$LOG_NAME  |  wc -l`
                echo $COUNT_ERROR 
                if [ $COUNT_ERROR -ge $error_limit ]
                then
			FINAL_COUNT=$(( $FINAL_COUNT + $COUNT_ERROR ))
               fi
		echo this is final count of error $FINAL_COUNT
        done # end of second loop
	if [ $FINAL_COUNT -ge 0 ]
	then
		echo "------------------------- $error_name  : $FINAL_COUNT -------------------------  " >> $ERROR_RESULT_FILE 
	fi 

done  # end of first loop
export END=$(date +%s)

DIFF=$(( $END - $START ))
DIFF=$(( $DIFF/60 ))
echo $DIFF 
test -s $ERROR_RESULT_FILE
mailx -s  "eSh: Top 10 Errors Report Daily" $MAIL_RECIEVERS -- -f $MAIL_SENDER < $ERROR_RESULT_FILE

##############################  end of script  ##############################
