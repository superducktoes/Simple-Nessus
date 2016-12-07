from bottle import *
import requests
import json

#replace these with the keys for the account used for scanning
accessKey = ""
secretKey = ""

url = "https://cloud.tenable.com/"
headers = {'X-ApiKeys': 'accessKey=' + str(accessKey) + '; secretKey = ' + str(secretKey) + ';'}
HOST="0.0.0.0"

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
    hosts = request.forms.get("hostsToScan")
    scannerID = request.forms.get("scannerID")
    policyID = request.forms.get("policyID")
    
    return "<p>Scanning Hosts</p>"


@route("/<filepath:path>")
def server_static(filepath):
    return static_file(filepath, root="./")
run(host=HOST, port=8080, debug=False)
