import subprocess
import re
import sys

findIp = re.compile('A\s*(\d*\.\d*\.\d*\.\d*)', re.MULTILINE)
NS = re.compile("IN\s+NS\s+(.+)", re.MULTILINE)
cnameip = re.compile("\.?\s+\d+\s+IN\s+A\s+(.+)",re.MULTILINE)

result = subprocess.check_output(['dig','@192.203.230.10','+norec',sys.argv[1]])
finds = re.findall(findIp,result)
host = sys.argv[1]

found = False
CnameFlag = False
while not found:
	for find in finds:
		try:		
		  result = subprocess.check_output(['dig','@' + find ,'+norec',host])
		  IpResult = re.compile(host + "\.?\s+\d+\s+IN\s+A\s+(.+)",re.MULTILINE)
		  findA = re.search(IpResult,result)
		  if (findA):
		  	found = True
		  	break
		  else:
		  	cnameline = re.compile(host + "\.?\s+\d+\s+IN\s+CNAME\s+(.+)", re.MULTILINE)	
		  	findCname = re.search(cnameline,result)
			if(findCname):
		  		findCname2 = re.search(cnameip,result)
		  		if (findCname2):
		  			found = True
		  			CnameFlag = True
		  			break
		  		else:
		  			find = findCname.group(1)
		  			result2 = subprocess.check_output(['dig', '@192.203.230.10','+norec',find])
		  			host = find
					finds = re.findall(findIp,result2)	
		  			break		
			else:			
				finds = re.findall(NS,result)
				if (finds):
					break
		except:
			pass	

if (found):
	if (CnameFlag):
		if findCname2:
			print sys.argv[1] + ': ' + findCname2.group(1)
		else:
			print 'No se encontro el resultado '
	else:	
		print  sys.argv[1] + ': ' + findA.group(1)			
