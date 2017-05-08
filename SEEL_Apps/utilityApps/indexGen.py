def autogen(files=[]):
	res = '''
	<html>
	<head>
	<meta content="text/html; charset=windows-1252" http-equiv="content-type">
	<title>index</title>
	</head>
	<body >All Experiments<br><br>
	'''
	for a in files:
		res+='''<a href="/usr/share/seelablet/seel_res/HTML/%s">%s</a><br>'''%(a,a.split('.')[0])

	res+='''
	</body>
	</html>
	'''
	return res

