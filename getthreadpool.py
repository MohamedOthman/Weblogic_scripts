## script purpose: get current threads running on weblogic managed servers 

RuntimeServers = [] ;

def getRuntimeServers():
        domainRuntime()
        runtimeServers=domainRuntimeService.getServerRuntimes()
        for server in runtimeServers :
                 RuntimeServers.append(server.getName())

def print_thread_details():
	for runTimeServer in RuntimeServers :
		cd('ServerRuntimes/'+runTimeServer+'/ThreadPoolRuntime/ThreadPoolRuntime')
		all=cmo.getExecuteThreadTotalCount() ; 
		stand=cmo.getStandbyThreadCount() ; 
		result=all-stand ; 
		print runTimeServer  , result
		cd('/') 
		
connect(username,pass,url) 
getRuntimeServers()
print_thread_details()
