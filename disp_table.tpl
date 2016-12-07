%# disp_table.tpl

<head>
<link rel="stylesheet" type="text/css" href="stylesheet.css">
<title>Nessus Scan</title>
</head>

<body>
<h1>Nessus Scan Launcher</h1>
<h3>Used to launch a scan against one host using pre-selected policies</h3>
<p>The following policies are available for use:</p>	

<table style="width:35%" border="1">  
<tr>
	<th>Scan Policy Name</th>
	<th>Scan Policy ID  </th>
</tr>
%for r in policyRows:
<tr>
	<td> {{r['name']}} </td>
	<td> {{r['id']}} </td>
</tr>
%end
</table>

<p>The following scanners are available for use:</p>
<table style="width:35%" border="1">
<tr>
	<th>Scanner Name</th>
	<th>Scanner ID  </th>
</tr>
%for r in scannerRows:
<tr>
	<td> {{r['name']}} </td>
	<td> {{r['id']}} </td>
</tr>
%end
</table>

<hr>
<br>

<form action="/forms" method="POST">
      IP to Scan: <input name="hostsToScan" type="text" />
      Policy ID: <input name="policyID" type="text" />
      Scanner ID: <input name="scannerID" type="text" />
<input value="Launch Scan" type="submit" />
</form>


</body>