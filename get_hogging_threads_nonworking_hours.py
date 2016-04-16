### hogging thread is a thread which it's response time more than the average response time which weblogic counts 
### for example if you have the average response time of the thread 200 second and you have a thread with response time 250 
### weblogic will mark it as a hogging thread , however stuck thread is a bigger value by default 600 second and you can configure it to be 
### larger.
### script purpose: check every managed server hogging threads and if it more than 40 hogging threads per managed server 
### the server will be added to list and then all of servers which has more than 40 hogging threads will be restarted since the script is scheduled to run 
### out of working hours and then will generate thread dump of every server to be sent to L2 and L3 to check the root cause of the issue in the next working day  
### Author: Mohamed Amr (m.amr.cse@gmail.com)

from java.util import Date
import os

#USERNAME=
#PASSWORD=
#URL=
server_Count=[] ; 
RuntimeServers = [] ; 
maxCount=-1 
flag=0 
sflag = 0
temp=[] 
TD_DIR="/opt/bea_logs/ThreadDumpDir"


def getRuntimeServers():
	domainRuntime()
	runtimeServers=domainRuntimeService.getServerRuntimes()
	for server in runtimeServers :
		if server.getName() != 'admin_server' :  
			RuntimeServers.append(server.getName())


#############    function to get all running servers  ###########
def getRunningStates():
        domainConfig()
        servers=cmo.getServers()
        domainRuntime()
        cd('/ServerLifeCycleRuntimes')
        for server in servers:
		flag=0 
                cd(server.getName())
                serverState=cmo.getState()
                if serverState == 'RUNNING' and server.getName() != 'admin_server'   :
			 shutdown(server.getName(),'Server',force='true')
			 print 'this is sleepe '
			 java.lang.Thread.sleep(20)
			 print cmo.getState() 
			 while flag == 0 : 
			 	if cmo.getState() ==  'FORCE_SHUTTING_DOWN' : 
					java.lang.Thread.sleep(5)
					print cmo.getState()
				else : 
					flag=1
					print flag
			 if flag == 1 : 
				start(server.getName(),'Server') 
				
                cd('..')





def getthreadDump(Server) : 
	threadDump(writeToFile='true',fileName=TD_DIR+'/'+Server+'_TD', serverName=Server)


def restartServer(Server) :
        domainRuntime()
        cd('/ServerLifeCycleRuntimes')
	cd(Server)
        shutdown(Server,'Server',force='true')
	print 'this is sleepe '
	java.lang.Thread.sleep(20)
	print cmo.getState()
	sflag = 0 
	while sflag == 0 :
		if cmo.getState() ==  'FORCE_SHUTTING_DOWN' :
			java.lang.Thread.sleep(5)
			print cmo.getState()
		else :
			sflag=1
			print sflag
		if sflag == 1 :
			start(Server,'Server')



def getStuckThreads() : 
	print 'start of get stuck threads function ' 
	f = open("Stuck_Thread.txt","w")
	domainRuntime()
	cd('/ServerRuntimes') 
	for runTimeServer in temp : 
		print runTimeServer
		cd(runTimeServer+'/ThreadPoolRuntime/ThreadPoolRuntime') 
		count=cmo.getHoggingThreadCount()
		print count 
		if count > maxCount : 
			flag=1
			f.write('server name is ' + runTimeServer ) 
			f.write ('	count is ' + count.toString() + '\n')
			getthreadDump(runTimeServer)  
			restartServer(runTimeServer) 
		cd('/ServerRuntimes')
		
	f.write('\n \n All impacted servers will be restarted one by one ')
	f.write('\n \n @L3 team : Thread dumps are taken under the following path /opt/bea_logs/ThreadDumpDir please extract them to take a look at this issue ') 
	f.close()
	if flag == 1 :
		
        	os.system('/bin/mailx -s "Critical server stuck threads exceed max count , servers restart"  RECIEVER  -- -f SENDER  < Stuck_Thread.txt')

###end of function

###### main script starts here 
connect('USER','PASS','URL')
getRuntimeServers()
getStuckThreads()
