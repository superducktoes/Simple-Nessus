#!/bin/bash

echo "Enter the access key: "
read accessKey
echo "Enter the secret key: "
read secretKey

#sets up the api keys
sed -i "s/accessKeyReplace/$accessKey/g" nessusScan.py
sed -i "s/secretKeyReplace/$secretKey/g" nessusScan.py

#email for scan launch alerts
echo "Enter the email address to send scan alerts to: "
read userEmail
sed -i "s/userEmailReplace/$userEmail/g" disp.py

#sets the email server
echo "Enter the email server: "
read emailServer
sed -i "s/mailServerReplace/$emailServer/g" mail.py
