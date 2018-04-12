#! /usr/bin/python3
def normalize(s, size):
	if len(s) >= size:
		return s
	return "0" * (size - len(s)) + s
def convertToDec(binAddr):
	o = [binAddr[i:i+8] for i in range(0,len(binAddr) - 7, 8)]
	return ".".join([str(int(i,2)) for i in o])
from sys import argv
try:
	a = argv[1]
	p = int(argv[2])

	b = "".join(normalize(bin(int(i))[2:], 8) for i in a.split("."))
	netPart = b[:p]
	print("Net addr: %s"%convertToDec(netPart + "0"*(32-p)))
	print("Net mask: %s"%convertToDec(p*"1" + (32-p)*"0"))
	print("First addr: %s"%convertToDec(netPart + normalize("1", 32-p)))
	print("Last addr: %s"%convertToDec(netPart + normalize(bin(2**(32-p)-2)[2:],32-p)))
except:
	print("Error. Usage <ip address> <net prefix>")
