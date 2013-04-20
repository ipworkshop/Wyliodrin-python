from sleekxmpp import ClientXMPP
from sleekxmpp.plugins.base import base_plugin
from sleekxmpp.xmlstream.stanzabase import ElementBase, ET, JID, register_stanza_plugin
from sleekxmpp.stanza.message import Message
import logging

def log(message):
	print message

class ValueStanza(ElementBase):	
	namespace = 'wylio'
	name = 'value'
	plugin_attrib = 'value'
	interfaces = set(('timestamp', 'signal', 'value'))
	sub_interfaces = tuple ()

class WylioStanza(ElementBase):	
	namespace = 'wylio'
	name = 'wylio'
	plugin_attrib = 'wylio'
	interfaces = set(('run', 'source'))
	sub_interfaces = interfaces
	subitem = (ValueStanza,)


class WylioXMPP:
	def __init__(self):
		self.connection = None
		self.jid = ""
	def connect(self,jid,password):
		self.jid = jid
		if self.connection == None:
			self.connection = ClientXMPP(jid, password)
		register_stanza_plugin (Message, WylioStanza)	
		register_stanza_plugin (WylioStanza, ValueStanza)	
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
		self.run_program ("source", "wylio.project@gmail.com/raspy")
		
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
		msg["wylio"]["run"] = name
		#msg["wylio"]["value"]="4082374"
		msg["wylio"]["value"]["timestamp"]="4082374"
		msg["wylio"]["value"]["signal"]="some name"
		msg["wylio"]["value"]["value"]="478923"
		print "message"
		print msg
		msg.send()
	
if __name__ == '__main__':
	xmpp = WylioXMPP ()
	xmpp.connect ("server@ipworkshop.ro", "raspberrypi")