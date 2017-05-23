import sys
import urllib
import shutil
import time as systime
#This script deploy application into weblogic instance from given path
connect('','','') ### connect to weblogic admin 
file='path of war'

deploymentName='name of war on weblogic'
deploymentTarget="target_Managed_server"

try: 
	edit()
	startEdit()
	print 'stoping.....' 
	stopApplication(deploymentName)
	print 'undeploying....' 
	undeploy(deploymentName)
	save()
	activate()
except Exception:
		print 'cant undeploy********************'
		error = True


try:
	edit()
	startEdit()
	print 'Deploying....................................' 
	deploy(deploymentName,file+deploymentName+'.war', deploymentTarget)
	save()
	print 'save................................................'
	activate(900000)
	print 'activate................................................' 
	startApplication(deploymentName)
except Exception:
	print 'cant deploy'
	error = True
