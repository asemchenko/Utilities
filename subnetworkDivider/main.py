#! /usr/bin/python
from sys import argv


def toBinOctet(decimalValue):
    r = int(decimalValue)
    if r < 0 or r > 255:
        raise Exception("Error in reading octet %s" % decimalValue)
    r = bin(r)[2:]
    if len(r) < 8:
        r = (8 - len(r)) * '0' + r
    return r


def divideSubnet(ip, subnetsSize, outSubnetsIP):
    if not subnetsSize:
        return True
    curNetHostsCount = 2 ** (32 - len(ip)) - 2
    if curNetHostsCount < subnetsSize[0]:
        return False
    subnetHostsCount = 2 ** (32 - len(ip) - 1) - 2
    if curNetHostsCount >= subnetsSize[0] and subnetHostsCount < subnetsSize[0]:
        outSubnetsIP.append((subnetsSize[0], ip))
        subnetsSize.pop(0)
        return True
    return divideSubnet(ip + '0', subnetsSize, outSubnetsIP) and divideSubnet(ip + '1', subnetsSize, outSubnetsIP)


def divideNetwork(netIP, subnetsSize):
    result = []
    subnetsSizeCopy = subnetsSize[:]
    subnetsSizeCopy.sort(reverse=True)
    divideSubnet(netIP, subnetsSizeCopy, result)
    if subnetsSizeCopy:
        print("Error in dividing net :(")
        raise Exception("Error in dividing net")
    return result


def netIPtoStr(ip):
    prefix = len(ip)
    ip += (32 - prefix) * '0'
    octets = [str(int(ip[i:i + 8], 2)) for i in range(0, 25, 8)]
    return ".".join(octets) + "/" + str(prefix)


def main():
    sourceNetworkPrefix = int(argv[1].split("/")[1])
    sourceNetworkIp = argv[1].split("/")[0]
    # converting ip to binary representation
    sourceNetworkIp = "".join(map(toBinOctet, sourceNetworkIp.split(".")))[:sourceNetworkPrefix]
    subnetsSize = list(map(lambda n: int(n), argv[2:]))
    r = divideNetwork(sourceNetworkIp, subnetsSize)
    for e in r:
        print("Network size: %d\t\t%s" % (e[0], netIPtoStr(e[1])))


try:
    main()
except Exception as e:
    print(e)
    print("\n\nUsage ndiv <source network> <subnets size>...\nExample: 192.168.0.0/24 2 2 5")
