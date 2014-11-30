#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
from scapy.all import *
from scapy.layers.ipsec import *
import string
import time
import sys, getopt

def init_key_globals():
	global b128_key, b192_key, b256_key
	b128_key = "-!L35chvo?q P]Za"
	b192_key = "-!L35chvo?q P]Za*fEZ3rRV"
	b256_key = "-!L35chvo?q P]Za*fEZ3rRV)Kkw|X.Q"

def processUser():

	try:
		choice = int(raw_input("Enter an algorithm choice: "))
	except ValueError:
		print "Invalid input."
		sys.exit(2)

	if choice == 1:
		sa = SecurityAssociation(ESP, spi=0xdeadbeef, crypt_algo='3DES', crypt_key=b128_key)
	elif choice == 2:
		sa = SecurityAssociation(ESP, spi=0xdeadbeef, crypt_algo='3DES', crypt_key=b192_key)
	elif choice == 3:
		sa = SecurityAssociation(ESP, spi=0xdeadbeef, crypt_algo='AES-CBC', crypt_key=b128_key)
	elif choice == 4:
		sa = SecurityAssociation(ESP, spi=0xdeadbeef, crypt_algo='AES-CBC', crypt_key=b192_key)
	elif choice == 5:
		sa = SecurityAssociation(ESP, spi=0xdeadbeef, crypt_algo='AES-CBC', crypt_key=b256_key)
	else:
		print "Invalid choice, try again."
		sys.exit(2)

	return sa

def displayAlgoList():
    	print "\nEncryption Algorithms: "
    	print "1. 3DES (128-bit encryption key)"
    	print "2. 3DES (192-bit encryption key)"
    	print "3. AES-CBC (128-bit encryption key)"
    	print "4. AES-CBC (192-bit encryption key)"
    	print "5. AES-CBC (256-bit encryption key)"