#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import scapy
import string
import time
from ipsec_algorithms import *

def payloadGenerator(size=1024):
	return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))

def createPacket(srcHost, destHost, destPort):
	p = IP(src=srcHost, dst=destHost)
	randSrcPort = random.randint(1024, 65535)
	p /= TCP(sport=randSrcPort, dport=destPort)
	p /= Raw(payloadGenerator())
	p = IP(str(p))

	print p
	return p

def sendPacket(packet, packetNum, SA):
	startTime = time.time()
	SA.encrypt(packet)
	encryptTime  = time.time()
	send(packet)
	sentTime = time.time()

	print "Packet #: " + packetNum
	print "Encryption Time: " + (encryptTime - startTime) * 1000 + " ms"
	print "Sent Time: " + (sentTime - encryptTime) * 1000 + " ms"

def encryptionList():
	print "Authentication Algorithms: "
	print "1. HMAC-­SHA1 (128-bit)"
	print "2. HMAC-SHA1 (192-bit)"
    	print "3. SHA2-­256"
    	print "4. SHA2-­384"
    	print "5. SHA2-­512"
    	print "\nEncryption Algorithms: "
    	print "6. 3DES (128-bit)"
    	print "7. 3DES (192-bit)"
    	print "8. AES-CBC (128-bit)"
    	print "9. AES-CBC (192-bit)"
    	print "10. AES-CBC (256-bit)"