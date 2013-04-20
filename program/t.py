f = open('/boot/xmpp.txt', 'r')
s = f.readline()
s = s.rstrip('\n')
print s,
s = f.readline()
print s,