# 1 domain 2 ip
import subprocess
import re
import sys


domain_find = re.compile('IN\s*MX\s*\d*\s*([\w*\.]*)', re.MULTILINE) #regexp to find the domain of mail server
ip_find = re.compile('([\d+\.]+)', re.MULTILINE) #regexp to find the ip of the mail server

ok = False

result = subprocess.check_output(['dig','MX','+noall','+answer',sys.argv[1]])
finds = re.findall(domain_find,result)
for find in finds: #loop of mail servers
	print find + ' dominio'
	result_ip = subprocess.check_output(['dig','+short',find]) 
	finds_ip = re.findall(ip_find,result_ip)
	for find_ip in finds_ip: #loop ip for mail server
		print find_ip + ' ip'
		if sys.argv[2] == find_ip:
			ok = True
if ok == True:
	print 'True'
else:	
	print 'False'


#Ip: 72.167.238.32
#domain: Montevideo.com
#Ip: 108.177.119.26
#domain: netflix.com
#Ip 200.40.31.19
#domain: adinet.com.uy


	