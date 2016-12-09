import json
import requests
import time


url = "https://cloud.tenable.com/"
headers = {'X-ApiKeys': 'accessKey=' + str(accessKey) + '; secretKey = ' + str(secretKey) + ';'}

#gets a list of available policies
def listPolicies():
	policies = requests.get(url+"policies/",headers=headers,verify=True)
	listPolicies = policies.json()["policies"]	

	return policyChoice

#used to get the uuid of the template once we have the policy id
def templateUuid(policyChoice):
	templateInfo = requests.get(url+"policies/"+str(policyChoice),headers=headers,verify=True)
	templateInfo = templateInfo.json()["uuid"]
	templateUuid = str(templateInfo)
	
	return templateUuid

#gets a list of available cloud/local scanners.		
def listScanners():
	scanners = requests.get(url+"scanners/",headers=headers,verify=True)
	listScanners = scanners.json()["scanners"]
        
	return scannerChoice

def createScanClass(policyChoice,scannerChoice,ipsToScan):
        newScanStatus = " "
        newScan = Scan(policyChoice,scannerChoice,ipsToScan)
        runningUUID = newScan.launchScan()
        
        newScan.updateRunningUUID(runningUUID)
        
        if(newScan.scanStatus(runningUUID) == True):
                newScanStaus = True
        
        return newScanStatus

# Scan class. takes in the policy id, scanner id of the scanner to use, and the ips to scan
#
# launchScan() is used to kick off the scan
# updateRunningUUID() updates the class with the id of the launched scan
# checkScanStatus(runningUUID) - gets the staus of a runnign scan. takes the scanid from the scan launched

class Scan:
	
	def __init__(self,policyChoice,scannerChoice,ipsToScan):
		self.uuid = templateUuid(policyChoice)
		self.policy = policyChoice
		self.scanner = scannerChoice
		self.hosts = ipsToScan
		self.runningUUID = 0

	def displayHosts(self):
		return self.hosts
	
	def displayScanner(self):
		return self.scanner

	def displayPolicy(self):
		return self.policy
	
	def displayUuid(self):
		return self.uuid

	#updated after the scan is launched with the id. Initially intialized to zero
	def updateRunningUUID(self,uuid):
		self.runningUUID = uuid
	
	#launches the scan in nessus
	#returns the id of the scan launched
	def launchScan(self):
		scan = {"uuid":self.uuid,
			"settings": {
			"name": "api scan", #add something here for the names of scans launched
			"enabled": "true",
			"scanner_id":self.scanner,
			"policy_id":self.policy,
			"text_targets":self.hosts,
			"launch_now":"true"}
			}

		scanData = requests.post(url+"scans",json=scan,headers=headers,verify=True)

		#checks to make sure that there weren't any errors when adding/kicking off the scan
		if(scanData.status_code == 200):
			print("Scan launched successfully")
		else:
			print("Error with launching the scan")		
		
		#parse the response to get the uuid of the running scan
		runningUUID = json.loads(scanData.text)
		runningUUID = runningUUID['scan']['id']
		#return the UUID of the scan launched
		return runningUUID

        #def scanStatus() - takes the running UUID and reports on whether or not the scan is completed.
	def scanStatus(seld,runningUUID):
		#GET /scans/{scan_id}
		runningStatus = requests.get(url+"scans/"+str(runningUUID),headers=headers,verify=True)
		completed = json.loads(runningStatus.text)
		completed = completed["info"]
		
		if(completed["status"] == "completed"):
			return False
		else:
			return True
		
                
