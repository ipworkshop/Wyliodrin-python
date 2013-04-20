from sleekxmpp import ClientXMPP
import logging
from program import Program

def log(message):
	print message

class WylioServer:
	def __init__(self):
		self.connection = None
	def connect(self,jid,password):
		if self.connection == None:
			self.connection = ClientXMPP(jid, password)
		self.connection.add_event_handler("connected", self.start)
		self.connection.connect()
		
	def start(self,event):
		log("WylioServer connected")
		self.send_presence()

server = WylioServer()
		
def main():
	file = open('/boot/xmpp.txt', 'r')
	jid = file.readline()
	jid = jid.rstrip('\n')
	password = file.readline()
	password = password.rstrip('\n')
	server.connect(jid, password)
	
if __name__ == '__main__':
	main()