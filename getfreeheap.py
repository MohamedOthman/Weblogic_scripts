## script purpose: print free heap size for list of managed servers 
RuntimeServers = [] ;

def getRuntimeServers():
        domainRuntime()
        runtimeServers=domainRuntimeService.getServerRuntimes()
        for server in runtimeServers :
                 RuntimeServers.append(server.getName())

def print_Free_Heap():
	domainRuntime()
	for runTimeServer in RuntimeServers :
		cd('ServerRuntimes/'+runTimeServer+'/JVMRuntime/'+runTimeServer)
		print runTimeServer  , cmo.getHeapFreePercent()
		cd('/') 

		
connect(username,pass,url) 
getRuntimeServers()
print_Free_Heap() 
