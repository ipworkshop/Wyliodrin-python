from sleekxmpp import ClientXMPP
from sleekxmpp.plugins.base import base_plugin
from sleekxmpp.xmlstream.stanzabase import ElementBase, ET, JID, register_stanza_plugin
from sleekxmpp.stanza.message import Message
import logging

def log(message):
	print message
	
class WylioStanza(ElementBase):	
	namespace = 'wylio'
	name = 'wylio'
	plugin_attrib = 'wylio'
	interfaces = set(('run', 'source', 'value'))
	sub_interfaces = interfaces


class WylioXMPP:
	def __init__(self):
		self.connection = None
		self.jid = ""
	def connect(self,jid,password):
		self.jid = jid
		if self.connection == None:
			self.connection = ClientXMPP(jid, password)
		register_stanza_plugin (Message, WylioStanza)	
		self.connection.add_event_handler("connected", self.connected)
		self.connection.add_event_handler("session_start", self.start)
		self.connection.add_event_handler("failed_auth", self.failed)
		self.connection.add_event_handler("disconnected", self.disconnected)
		self.connection.add_event_handler("message", self.message)
		self.connection.connect(('talk.google.com', 5222))
		self.connection.process ()
		
	def connected(self,event):
		log ("WylioXMPP connected")
		
	def start(self, event):
		log ("WylioXMPP start")
		self.connection	.send_presence()
		log ("Wylio presence")
		self.run_program ("source", "wylio.project@gmail.com")
		
	def message(self, event):
		print event
		
	def failed(self,event):
		log ("WylioXMPP failed")
	
	def disconnected(self,event):
		log("WylioXMPP disconnected")
		
	def run_program (self, name, jid):
		print "fsdafasd"
		msg = self.connection.Message (sto=jid, stype="normal")
		print msg
		msg["body"]="dasdsadas"
		msg["wylio"]["run"] = name
		print "message"
		print msg
		msg.send()
	
if __name__ == '__main__':
	xmpp = WylioXMPP ()
	xmpp.connect ("server@ipworkshop.ro", "raspberrypi")