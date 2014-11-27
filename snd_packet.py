#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
from scapy.all import *
from scapy.layers.ipsec import *
import string
import time
import sys, getopt
import globals as keys

def payloadGenerator(size=1024):
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
	SA.encrypt(packet)
	encryptTime = time.time()
	send(packet)
	sentTime = time.time()

	print "Packet #: " + str(packetNum)
	print "Encryption Time: " + str((encryptTime - startTime) * 1000) + " ms"
	print "Sent Time: " + str((sentTime - encryptTime) * 1000) + " ms"

def displayAlgoList():
	print "Authentication Algorithms: "
	print "1. HMAC-SHA1 (192-bit integrity key)"
	print "2. SHA2-256 (192-bit integrity key)"
    	print "3. SHA2-384 (192-bit integrity key)"
    	print "4. SHA2-512 (192-bit integrity key)"
    	print "\nEncryption Algorithms: "
    	print "5. 3DES (128-bit encryption key)"
    	print "6. 3DES (192-bit encryption key)"
    	print "7. AES-CBC (128-bit encryption key)"
    	print "8. AES-CBC (192-bit encryption key)"
    	print "9. AES-CBC (256-bit encryption key)"

def displayHelp():
	print 'Usage: snd_packet.py -s <src host> -d <dest host> [-p <dest port>] [-c <packet count sent>]'
      	print '-s or --srchost 	- the host you want to send from'
      	print '-d or --dsthost 	- the host you want to send to'
      	print '-p or --dstport 	- the port you want to send to (default is 8000)'
      	print '-c or --count 	- the number of packets you want to send (default is 10)'

def processUser():

	try:
		choice = int(raw_input("Enter an algorithm choice: "))
	except ValueError:
		print "Invalid input."
		sys.exit(2)


	if choice == 1:
		sa = SecurityAssociation(AH, spi=0xdeadbeef, auth_algo='HMAC-SHA1-96', auth_key=keys.b192_key)
	elif choice == 2:
		sa = SecurityAssociation(AH, spi=0xdeadbeef, auth_algo='SHA2-256-128', auth_key=keys.b192_key)
	elif choice == 3:
		sa = SecurityAssociation(AH, spi=0xdeadbeef, auth_algo='SHA2-384-192', auth_key=keys.b192_key)
	elif choice == 4:
		sa = SecurityAssociation(AH, spi=0xdeadbeef, auth_algo='SHA2-512-256', auth_key=keys.b192_key)
	elif choice == 5:
		sa = SecurityAssociation(ESP, spi=0xdeadbeef, crypt_algo='3DES', crypt_key=keys.b128_key)
	elif choice == 6:
		sa = SecurityAssociation(ESP, spi=0xdeadbeef, crypt_algo='3DES', crypt_key=keys.b192_key)
	elif choice == 7:
		sa = SecurityAssociation(ESP, spi=0xdeadbeef, crypt_algo='AES-CBC', crypt_key=keys.b128_key)
	elif choice == 8:
		sa = SecurityAssociation(ESP, spi=0xdeadbeef, crypt_algo='AES-CBC', crypt_key=keys.b192_key)
	elif choice == 9:
		sa = SecurityAssociation(ESP, spi=0xdeadbeef, crypt_algo='AES-CBC', crypt_key=keys.b256_key)
	else:
		print "Invalid choice, try again."
		sys.exit(2)

	return sa

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
         		destPort = arg
         	elif opt in ("-c", "--count"):
         		count = arg
         	else:
         		assert False, "unhandled option"

        print "Src Host: " + srcHost
        print "Dest Host: " + destHost
        print "Dest Port: " + str(destPort)
        print "Count: " + str(count)
        
        if srcHost is '' or destHost is '' or isinstance(destPort, int) or isinstance(count, int):
        	displayHelp()
        	sys.exit()

       	return {'srcHost': srcHost, 'destHost': destHost, 'destPort': int(destPort), 'count' : int(count)}



if __name__ == "__main__":
	keys.init_key_globals()
	userArgs = processArgs(sys.argv[1:])

	displayAlgoList()
	sa_header = processUser()

	for packetN in range(1, userArgs['count'] + 1):
		packet = createPacket(userArgs['srcHost'], userArgs['destHost'], userArgs['destPort'])
		sendPacket(packet, packetN, sa_header)



	
