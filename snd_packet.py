#!/usr/bin/python
# -*- coding: utf-8 -*-

from utils import *

def payloadGenerator(size=1024):
	return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))

def createPacket(srcHost, destHost):
	p = IP(src=srcHost, dst=destHost)
	randSrcPort = random.randint(1024, 65535)
	randDestPort = random.randint(1024, 65535)
        p /= TCP(sport=randSrcPort, dport=randDestPort)
	p /= Raw(payloadGenerator())
	p = IP(str(p))

	return p

def writeSentToFile(sentPktTime, encryptTime):
        with open('sent_data.xlsx', 'a') as f:
                f.write(sentPktTime + ',' + encryptTime + '\n')

def sendPacket(packet, packetNum, SA):
	startTime = time.time()
	encryptedPacket = SA.encrypt(packet)
	encryptTime = time.time()
	
        send(encryptedPacket)
	sentTime = str(time.time() * 1000)

	print "Packet #: " + str(packetNum)
	print "Encryption Time: " + str((encryptTime - startTime) * 1000) + " ms"
	print "Sent Time: " + sentTime + " ms"

	encryptionTime = str((encryptTime - startTime) * 1000)

        writeSentToFile(sentTime, encryptionTime)

def displayHelp():
	print 'Usage: snd_packet.py -s <src host> -d <dest host> [-p <dest port>] [-c <packet count sent>]'
      	print '-s or --srchost 	- the host you want to send from'
      	print '-d or --dsthost 	- the host you want to send to'
      	print '-c or --count 	- the number of packets you want to send (default is 10)'

def processArgs(argv):
	srcHost = ''
   	destHost = ''
   	count = 10
   	
   	try:
      		opts, args = getopt.getopt(argv,"hs:d:c:",["srchost=","dsthost=","count="])
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
        print "Count: " + str(count)
        
        if srcHost is '' or destHost is '':
        	displayHelp()
        	sys.exit()

       	return {'srcHost': srcHost, 'destHost': destHost, 'count' : int(count)}



if __name__ == "__main__":
	init_key_globals()
	userArgs = processArgs(sys.argv[1:])

	displayAlgoList()
	sa_header = processUser()

	for packetN in range(1, userArgs['count'] + 1):
		packet = createPacket(userArgs['srcHost'], userArgs['destHost'])
		sendPacket(packet, packetN, sa_header)
