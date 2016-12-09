<html>
<h1>Nessus Scan Launcher</h1>
<h5>Version: 0.2</h5>
<h3>Usage</h3>
<p>Used to launch scans using the Nessus Cloud Scanner</p>
<p>The only information that needs to be entered is the host to scan,
policy ID, and scannerID that are listed in the tables above them.</p>

<h3>Initial Configuration</h3>
<p>In the disp.py file the only changes that need to be changed are the Nessus
API keys, and the HOST variable if you want to specift a specific interfce. By default it is set to listen on 0.0.0.0</p>
<p>After a scan is launched an email will also be sent to the contact listed in mail.py</p>
<h3>Things to be added</h3>
<p>Some things to still be added:
  error checking before submitting values to Nessus,
  name field for tracking scan names,
  logging
</p>
<br>
<br>
<a href="/">Back</a>
</html>
