#!/usr/lib/python

from utils import *

def processPacket(currentPkt, currentPktNum, prevPkt, SA):
	startTime = time.time()
	decryptedPacket = SA.decrypt(currentPkt)
	decryptTime = time.time()

	print "Packet Number #: " + str(currentPktNum)
	print "Decryption Time: " + str((decryptTime - startTime) * 1000) + " ms"
	print "Arrival Time: " + str((prevPkt.time - currentPkt.time) * 1000) + " ms"

def processArgs(argv):

	destHost = ''

	try:
      		opts, args = getopt.getopt(argv,"hd:",["dsthost="])
   	except getopt.GetoptError:
      		displayHelp()	
      		sys.exit(2)
   	for opt, arg in opts:
      		if opt == '-h':
        		displayHelp()
         		sys.exit()
      		elif opt in ("-d", "--dsthost"):
         		destHost = arg
         	else:
         		assert False, "unhandled option"

        print "Dest Host: " + destHost
        
        if destHost is '':
        	displayHelp()
        	sys.exit()

       	return destHost

def displayHelp():
	print 'Usage: recv_packet.py -d <dest host>'
      	print '-d or --dsthost 	- the host you want to listen from'

if __name__ == "__main__":
	init_key_globals()
	destHost = processArgs(sys.argv[1:])

	displayAlgoList()
	sa_header = processUser()

	packetFilter = "host " + destHost
	capturedPacketList = sniff(filter=packetFilter)

	for pkt in capturedPacketList:
		if capturedPacketList.index(pkt) == 0:
			continue
		processPacket(pkt, capturedPacketList.index(pkt), pkt[capturedPacketList.index(pkt)-1], sa_header)