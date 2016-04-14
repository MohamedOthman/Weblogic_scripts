#!/usr/bin/bash
#the script purpose is to do a rolling restart for all managed server in case of the below reasons 
#Implementing change 
#Performance issue 
#removing cached requests 
#all of servers will be restarted one by one 


### replace this line with the existing setDomainEnv.sh script 
source /opt/wls_domain/setDomainEnv.sh 

START=$(date +%s)
mailx -s  "Env Rolling Restart" Reciver -- -f Sender<MailBody.txt 
java weblogic.WLST <<EOWLST 

import time
import os 

servers = ['m1','m2','m3','m4']
runningServers = []
username="$WL_USER"
password="$WL_PASS"
URL="$WL_URL"
flag=0 

###### end of declaration section


#############    function to get all running servers  ###########
def getRunningStates():
        domainConfig()
        domainRuntime()
        cd('/ServerLifeCycleRuntimes')
        for server in servers:
		print '------ server %s ------' % server
		flag=0 
                cd(server)
                serverState=cmo.getState()
                if serverState == 'RUNNING'  :
			print 'shutdowning %s ...' % server 
			shutdown(server,'Server',force='true')
			print 'this is sleepe '
			java.lang.Thread.sleep(20)
			print cmo.getState() 
			while flag == 0 : 
				if cmo.getState() ==  'FORCE_SHUTTING_DOWN' : 
					java.lang.Thread.sleep(5)
					print '.',
				else : 
					flag=1
					print '%s is shutdown' % server
				if flag == 1 : 
					print 'starting %s ...' % server
					start(server,'Server') 
		else :
			print 'starting %s ...' % server
			start(server,'Server')
				
                cd('..')



#### end of getting all running servers  and restart them one by one  #### 

####### main script starts here 
#try: 
	connect(username,password,URL) 
#except WLSTException:
#        os.system('/bin/mailx -s "Warning: Connection to Admin Server is not possible please check"  Sender  -- -f Reciver  < RollingMsg ')
#	print exiting now since no active connection to Admin server 
#	exit 	
getRunningStates()
#RollingRestart() 

#### end of WLST script 

EOWLST

END=$(date +%s)
DIFF=$(( $END - $START ))
TOTAL=$(( $DIFF / 60 )) 
echo the total time of script is  :  $TOTAL
mailx -s  "Env Rolling Restart Completed" Sender -- -f Reciever<MailBody.txt 
