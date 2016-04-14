### Environment Variables file for alert logs script 

export MANAGED_SERVERS="mananged1 mananged2 managed3"
export BEA_LOGS_PATH=/opt/bea_logs/wl_domain
export KNOWN_ERRORS_FILE=$BEA_LOGS_PATH/ERROR_RECORDS/Kown_Errors.txt
export TARGET_ERRORS_RECORDS=$BEA_LOGS_PATH/ERROR_RECORDS
export ERROR_RESULT_FILE=$BEA_LOGS_PATH/errors_results.txt
export LOG_NAME="stdout_`date -d "-1 days" +"%Y-%m-%d"`.log"
export START=$(date +%s)
export FINAL_COUNT=0 
export LOG_DIR=/opt/bea_logs/wl_domain
export MAIL_RECIEVERS=me@mail.com
export MAIL_SENDER=me@mail.com
