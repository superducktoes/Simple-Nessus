from bottle import *
from nessusScan import createScanClass
from mail import Alert
import requests

HOST="0.0.0.0"

#replace these with the keys for the account used for scanning
accessKey = ""
secretKey = ""

url = "https://cloud.tenable.com/"
headers = {'X-ApiKeys': 'accessKey=' + str(accessKey) + '; secretKey = ' + str(secretKey) + ';'}

#gets a list of available policies
def listPolicies():
    policies = requests.get(url+"policies/",headers=headers,verify=True)
    listPolicies = policies.json()["policies"]

    return listPolicies

def listScanners():
    scanners = requests.get(url+"scanners/",headers=headers,verify=True)
    listScanners = scanners.json()["scanners"]

    return listScanners


policies = listPolicies()
scanners = listScanners()


@route("/")
def serveHome():
    return template("disp_table",
                    policyRows=policies,
                    scannerRows=scanners)

@post("/forms")
def getFormData():
    scanStatusMessage = " "
    hosts = request.forms.get("hostsToScan")
    scannerID = request.forms.get("scannerID")
    policyID = request.forms.get("policyID")
    
    #strips away any commas and whitespace
    hosts = hosts.split(",")[0]
    hosts = hosts.split(" ")[0]
    
    newScan = createScanClass(policyID,scannerID,hosts)

    if(newScan):
        scanStatusMessage = "Scan Launched Successfully"
        newEmail = Alert()
        newEmail.updateRecipient("  ")
        newEmail.sendEmail() 
    else:
        scanStatusMessage = "There was a problem with the scan"
        
    return scanStatusMessage

@route("/<filepath:path>")
def server_static(filepath):
    return static_file(filepath, root="./")


@route("/help")
def helper():
    
    return template("help_template")

@error(404)
def error404(error):

    return "<h1>404</h1>"

run(host=HOST, port=8080, debug=False)
