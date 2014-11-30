#!/usr/lib/python

from utils import *

def writeArrivalToFile(arrivalPktTime, decryptTime):
	with open('arrival_data.xlsx', 'a') as f:
		f.write(arrivalPktTime+ ','+ decryptTime + '\n')


def processPacket(currentPkt, currentPktNum, SA):
	startTime = time.time()
	decryptedPacket = SA.decrypt(currentPkt)
	decryptTime = time.time()

	pktArrivalTime = str(currentPkt.time * 1000)

	print "Packet Number #: " + str(currentPktNum)
	print "Decryption Time: " + str((decryptTime - startTime) * 1000) + " ms"
	print "Arrival Time: " + pktArrivalTime + " ms"
	decryptionTime = str((decryptTime - startTime) * 1000)
	writeArrivalToFile(pktArrivalTime, decryptionTime)

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

	packetFilter = "ip and not icmp and host " + destHost
	capturedPacketList = sniff(filter=packetFilter)

	for pkt in capturedPacketList:
		print pkt.summary()
		processPacket(pkt[IP], capturedPacketList.index(pkt), sa_header)
