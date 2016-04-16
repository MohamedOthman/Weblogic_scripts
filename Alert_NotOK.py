### script purpose 
### is to check weblogic servers which health is not ok and restart them 
### Author: Mohamed Amr (m.amr.cse@gmail.com)

from java.util import Date 
import os 

###### declaration section  
runningServers = [] 
shutdownServers = [] 
FNRServers = [] 
RuntimeServers = [] 
not_Ok = [] 
flag = 0 
username=WL_USER
password=WL_PASSWORD
URL=WL_URL

###### end of declaration section 

#############    function to get all servers states  ########### 
def getAllStates(): 
	domainConfig()			
	servers=cmo.getServers()
	domainRuntime()
	cd('/ServerLifeCycleRuntimes') 
	print 'test test tset' 
	for server in servers:
		cd(server.getName()) 
		serverState=cmo.getState()
		if serverState == 'SHUTDOWN':
                	shutdownServers.append(server.getName())
		elif serverState == 'RUNNING':
			runningServers.append(server.getName())
		elif serverState == 'FAILED_NOT_RESTARTABLE': 
			FNRServers.append(server.getName()) 
		cd('..') 

#### end of getting all servers states 


###########   function to store running servers with health status ok  ########### 
def getRuntimeServers():  
	domainRuntime()
	runtimeServers=domainRuntimeService.getServerRuntimes()
	for server in runtimeServers : 
		RuntimeServers.append(server.getName())

######### end of function  ##########		

######## function to print all servers states 
def printAll() :
	if  len(shutdownServers) > 0 : 
		print '#####################   shut down servers    #######################'
		for i in shutdownServers:
        		print i
	if len(runningServers) > 0 : 
		print '#####################   running servers    #######################'
		for i  in runningServers:
        		print i
	if  len(FNRServers) > 0 : 
		print '#####################   failed not restartable  servers    #######################'
		for i  in FNRServers:
        		print i
	if len(not_Ok) > 0 :
		print '####################    Not Ok servers  #######################'
		for i in not_Ok : 
			print i 

###### end of function ###########


##########   function to test if running servers is in runtime servers or not and if running server is not found in runtime server 
#it will add it to not_Ok list 

def get_Not_OkServers():
	runningServers
	RuntimeServers 
	for runningServer in runningServers : 
		flag= 0 
		for runtimeServer in RuntimeServers : 
			if runningServer == runtimeServer :
				flag = 1   
				break  
		if flag == 0 :  
			not_Ok.append(runningServer)
#	for server in not_Ok : 
#		print server 

############   function to restart not Ok servers   ##################
def restartNotOk(): 
	if len(not_Ok) > 0 : 
                f = open("serverState_file","w")
                f.write('----------------- the following servers was not ok at this time ----------------     ' + Date().toString() + '\n')
                for i in not_Ok :
                        f.write('----------------    ' + i + '    ----------------\n')

#		for server in not_Ok :   this section deffered till test of sending mail functionaltiy with out this section sctipt now just alert L2 team when managed servers's health is not OK 
#			shutdown('managed1','Server','true',1000,'true')
#			start(server) 
#		f.write('----------------- the reported servers restarted successfully at this time ----------------     ' + Date().toString() + '\n')
        	f.close()
		os.system('/bin/mailx -s "Critical : Not_OK servers  !!! Please check."  RECIEVER  -- -f RECIEVER < serverState_file')
	else : 
		print 'All of running servers\' health is ok'

##########end of function 


########  Main Script Starts Here ##########
connect(username,password,URL)
getAllStates()
getRuntimeServers() 
get_Not_OkServers()
printAll()
restartNotOk()
#########################################   end of script   #########################################
