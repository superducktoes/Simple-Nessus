from bottle import *
from nessusScan import createScanClass
from nessusScan import listPolicies, listScanners
from mail import Alert
import requests

#change this to bind to a specific interface
HOST="0.0.0.0"
#change this to the email you want alerts sent to
userEmail = "userEmailReplace"

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
    scanName = request.forms.get("scanName")

    #strips away any commas and whitespace
    hosts = hosts.split(",")[0]
    hosts = hosts.split(" ")[0]
    
    appScan = createScanClass(policyID,scannerID,hosts,scanName)

    if(appScan):
        scanStatusMessage = "Scan Launched Successfully against  " + str(hosts) + "  and an email has been sent to " + userEmail
        newEmail = Alert()
        newEmail.updateRecipient(userEmail)
        newEmail.updateSubject("Scan launched against " + str(hosts))
        newEmail.sendEmail() 
    else:
        scanStatusMessage = "There was a problem launching the scan. Please go back and check the ID's and host to scan"
        
    return scanStatusMessage

@route("/<filepath:path>")
def server_static(filepath):
    return static_file(filepath, root="./")


@route("/help")
def helper():
    
    return template("help_template")

@error(404)
def error404(error):

    return "<h1 align=\"center\">404</h1><br><p align=\"center\">And as of this morning, we are completely wireless here at Shrute Farms, but as soon as I find out where Mose hid all the wires, we'll get all that power back on. ~Dwight Schrute</p>"

run(host=HOST, port=8080, debug=False)
