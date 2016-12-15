import json
import requests
import sys #used for command line arguments
import time

#replace these with the keys for the account used for scanning
accessKey = "827a7e8af83d84fad4b56db8f611547f470fad196bb193060d19cded0795b928"
secretKey = "25afd3344ac1018d645f80c7c9cb84a8b3e0e061252692713b7348b25160eb1e"

url = "https://cloud.tenable.com/"
headers = {'X-ApiKeys': 'accessKey=' + str(accessKey) + '; secretKey = ' + str(secretKey) + ';'}

#gets a list of available policies
def listPolicies():
        policies = requests.get(url+"policies/",headers=headers,verify=True)
        listPolicies = policies.json()["policies"]
        
        return listPolicies

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

        return listScanners

def createScanClass(policyChoice,scannerChoice,ipsToScan,scanName):
	newScan = Scan(policyChoice,scannerChoice,ipsToScan,scanName)
	runningUUID = newScan.launchScan()
	newScan.updateRunningUUID(runningUUID)
	
	#pauses 30 seconds after submit is clicked to make sure that the scan is launched successfully
	scanStatus = False
	time.sleep(30)
	if(newScan.scanStatus(runningUUID) == True):
		scanStatus = True
	#returns true if the scan launched, false if there was an issue
	return scanStatus

# Scan class. takes in the policy id, scanner id of the scanner to use, and the ips to scan
#
# launchScan() is used to kick off the scan
# updateRunningUUID() updates the class with the id of the launched scan
# checkScanStatus(runningUUID) - gets the staus of a runnign scan. takes the scanid from the scan launched

class Scan:
	
	def __init__(self,policyChoice,scannerChoice,ipsToScan,scanName):
		self.uuid = templateUuid(policyChoice)
		self.policy = policyChoice
		self.name = scanName
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
			"name": self.name,
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
		
                
if __name__ == '__main__':
	running = True

	if((len(sys.argv) != 4)):
		ipsToScan = input("Enter the ip/ip's to scan: ")
                #list all of the available scan policies
		policyChoice = listPolicies()
		scannerChoice = listScanners()	
		scanUuid = templateUuid(policyChoice)
                #Create the scan
		createScanClass(policyChoice,scannerChoice,ipsToScan)	
	
        #displays infomration about command line arguments	
	elif(sys.argv[1] == "help"):
		print("arg1 - Scan policy ID")
		print("arg2 - Scanner choice ID")
		print("arg3 - IP or cidr to scan")
		print("Hosts can be entered as either a single host/IP, comma seperated hosts, or cidr")

	#if there are command line args then we can go ahead and launch the scan
	else:
		policyChoice = sys.argv[1]
		scannerChoice = sys.argv[2]
		ipsToScan = sys.argv[3]
		crateScanClass(policychoice,scannerChoice,ipsToScan)
