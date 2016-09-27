#This script start/stop Managed Servers listed in order first start EJB (backend) servers then wait for EJB (backend) servers to start 
# then start frontend managed servers and wait for them till getting running  
import getopt
adminurl="t3://localhost:3000"
adminusername=""
adminpassword=""
backend_serverlist=["Admin","Alert","parts"]
frontend_serverlist=["AlertGUI","AdminGUI"]
stop_list=["Admin","AdminGUI","Alert","AlertGUI","parts"]
 
def connect_admin():
    try:
        print "connecting to admin server"
        connect(adminusername, adminpassword, adminurl)
        print 'connected to admin server'
    except:
        print "can not connect to admin servers please check provided credentials or admin server's state"
 

 
def start_stop(serverlistSplit):
	domainRuntime()
	if getcommand == 'start':
		for s in serverlistSplit :
			bean = getMBean('ServerRuntimes/' + s)
			if bean:
				print 'Server ' + s + ' is ' + bean.getState()
			else:
				start(s, 'Server', block='false')
				print 'Started Server ' + s
	if getcommand == 'stop':
		for s in serverlistSplit:
			bean = getMBean('ServerRuntimes/' + s)
			if bean:
				shutdown(s, 'Server' ,force='true')
				print 'Stopped Server ' + s
			else:
				print 'Server ' + s + ' is not running'
			
def ServrState(servers_list):
	print 'inside server state'
	dummy_flag=0
	server_status_flag='not_running'
	serverConfig()
	Servers = cmo.getServers()
	while server_status_flag != 'running':
		server_status_flag = 'running'
		for server in Servers:
			for server_l in servers_list: 
#				print "server_l is : " + server_l + " and server is" + server.getName() 
				if server.getName() == server_l:
					cd('domainRuntime:/ServerLifeCycleRuntimes/' + server.getName());
					serverState = cmo.getState()
					if serverState == 'RUNNING':
						print server.getName() + ' server is running'
					elif serverState == 'SHUTDOWN' or serverState == 'FAILED_NOT_RESTARTABLE' :
						print "one of servers is shutdown"
						print "the script will exit"
						sys.exit(1)
					else:
						print server.getName() + " server is not running"
						server_status_flag = 'not_running'
						print 'sleeping 20 second'
						java.lang.Thread.sleep(20000);
				else: 
					dummy_flag=1     
					
##########################################
###  MAIN Script Starts Here           ###
##########################################
# Get the command, must be 'start' or 'stop'
getcommand=sys.argv[1]
if getcommand == 'start':
	connect_admin()
	start_stop(backend_serverlist)
	ServrState(backend_serverlist)
	start_stop(frontend_serverlist)
	ServrState(frontend_serverlist)
elif getcommand == 'stop':
	connect_admin()
	start_stop(stop_list)
else:
	print "please enter valid commnad start or stop"
	exit()
