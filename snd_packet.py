#!/usr/bin/python
# -*- coding: utf-8 -*-

from utils import *

def payloadGenerator(size=1):
	return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))

def createPacket(srcHost, destHost, destPort):
	p = IP(src=srcHost, dst=destHost)
	randSrcPort = random.randint(1024, 65535)
	p /= TCP(sport=randSrcPort, dport=destPort)
	p /= Raw(payloadGenerator())
	p = IP(str(p))

	return p

def sendPacket(packet, packetNum, SA):
	startTime = time.time()
	encryptedPacket = SA.encrypt(packet)
	encryptTime = time.time()
	send(encryptedPacket)
	sentTime = time.time()

	print "Packet #: " + str(packetNum)
	print "Encryption Time: " + str((encryptTime - startTime) * 1000) + " ms"
	print "Sent Time: " + str((sentTime - encryptTime) * 1000) + " ms"

def displayHelp():
	print 'Usage: snd_packet.py -s <src host> -d <dest host> [-p <dest port>] [-c <packet count sent>]'
      	print '-s or --srchost 	- the host you want to send from'
      	print '-d or --dsthost 	- the host you want to send to'
      	print '-p or --dstport 	- the port you want to send to (default is 8000)'
      	print '-c or --count 	- the number of packets you want to send (default is 10)'

def processArgs(argv):
	srcHost = ''
   	destHost = ''
   	destPort = 8000
   	count = 10
   	
   	try:
      		opts, args = getopt.getopt(argv,"hs:d:p:c:",["srchost=","dsthost=","dstport=","count="])
   	except getopt.GetoptError:
      		displayHelp()	
      		sys.exit(2)
   	for opt, arg in opts:
      		if opt == '-h':
        		displayHelp()
         		sys.exit()
      		elif opt in ("-s", "--srchost"):
         		srcHost = arg
      		elif opt in ("-d", "--dsthost"):
         		destHost = arg
         	elif opt in ("-p", "--dstport"):
         		try:
         			destPort = int(arg)
         		except ValueError:
         			displayHelp()
         			sys.exit()
         	elif opt in ("-c", "--count"):
         		try:
         			count = int(arg)
         		except ValueError:
         			displayHelp()
         			sys.exit()
         	else:
         		assert False, "unhandled option"

        print "Src Host: " + srcHost
        print "Dest Host: " + destHost
        print "Dest Port: " + str(destPort)
        print "Count: " + str(count)
        
        if srcHost is '' or destHost is '':
        	displayHelp()
        	sys.exit()

       	return {'srcHost': srcHost, 'destHost': destHost, 'destPort': int(destPort), 'count' : int(count)}



if __name__ == "__main__":
	init_key_globals()
	userArgs = processArgs(sys.argv[1:])

	displayAlgoList()
	sa_header = processUser()

	for packetN in range(1, userArgs['count'] + 1):
		packet = createPacket(userArgs['srcHost'], userArgs['destHost'], userArgs['destPort'])
		sendPacket(packet, packetN, sa_header)