from sleekxmpp import ClientXMPP
import logging
from program import Program
from sleekxmpp.xmlstream.stanzabase import ElementBase, ET, JID, register_stanza_plugin
from sleekxmpp.stanza.message import Message

def log(message):
	print message
class WylioStanza(ElementBase):	
	namespace = 'wylio'
	name = 'wylio'
	plugin_attrib = 'wylio'
	interfaces = set(('run', 'source', 'value'))
	sub_interfaces = interfaces
class WylioServer:
	def __init__(self):
		self.connection = None
		log("WylioServer initialised")
	def connected(self,event):
		log("WylioServer connected")
	def disconnected(self,event):
		log("WylioServer disconnected")
	def failed_auth(self,event):
		log("WylioServer failed authentification")
	def message(self, event):
		log("WylioServer message received")
		print event
	def connect(self,jid,password):
		if self.connection == None:
			self.connection = ClientXMPP(jid, password)
		register_stanza_plugin (Message, WylioStanza)
		self.connection.add_event_handler("connected", self.connected)
		self.connection.add_event_handler("disconnected", self.disconnected)
		self.connection.add_event_handler("failed_auth", self.failed_auth)
		self.connection.add_event_handler("session_start", self.start)
		self.connection.add_event_handler("message", self.message)
		print "connect"
		self.connection.connect()
		self.connection.process(block=True)
		print "connected"
		
	def start(self,event):
		log("WylioServer started")
		self.connection.send_presence()
		print "presence sent"
		self.connection.get_roster()

server = WylioServer()
		
def main():
	file = open('/boot/xmpp.txt', 'r')
	jid = file.readline()
	jid = jid.rstrip('\n')
	password = file.readline()
	password = password.rstrip('\n')
	print jid
	print password
	server.connect(jid, password)
	
if __name__ == '__main__':
	main()