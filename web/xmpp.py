from sleekxmpp import ClientXMPP, Callback, StanzaPath
from sleekxmpp.plugins.base import base_plugin
from sleekxmpp.xmlstream.stanzabase import ElementBase, ET, JID, register_stanza_plugin
from sleekxmpp.stanza.message import Message
import traceback
import logging

def nr(str):
	try:
		return float(str);
	except:
		return str

def log(message):
	print message

class ValueStanza(ElementBase):	
	namespace = 'wylio'
	name = 'value'
	plugin_attrib = 'value'
	interfaces = set(('program', 'timestamp', 'signal', 'value'))
	sub_interfaces = tuple ()

class WylioStanza(ElementBase):	
	namespace = 'wylio'
	name = 'wylio'
	plugin_attrib = 'wylio'
	interfaces = set(('run', 'source', 'in', 'out', 'err'))
	sub_interfaces = interfaces
	subitem = (ValueStanza,)


class WylioXMPP:
	def __init__(self, email, db):
		self.connection = None
		self.email = email
		self.db = db
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
		self.connection.register_handler (Callback ("Wylio", StanzaPath("message/wylio"), self.message_wylio))
		self.connection.connect(('talk.google.com', 5222))
		self.connection.process ()
		
	def connected(self,event):
		log ("WylioXMPP connected")
		
	def start(self, event):
		log ("WylioXMPP start")
		self.connection	.send_presence()
		log ("Wylio presence")
		#self.run_program ("source", "wylio.project@gmail.com/raspy")
		
	def disconnect (self):
		self.connection.disconnect ()
		
	def message_wylio (self, msg):
		if msg["wylio"]["value"]:
			#print msg	
			signal = msg["wylio"]["value"]["signal"]
			value = nr(msg["wylio"]["value"]["value"])
			
			print signal, " ", value
			if self.db.values.find ({"email":self.email, "signal":signal}).count () == 0:
				self.db.values.insert ({"email":self.email, "signal":signal, "values":[value]})
			else:
				try:
					self.db.values.update ({"email":self.email, "signal":signal}, {"$push": {"values":value}})
				except:
					traceback.print_exc()
		
	def message(self, event):
		print event
		
	def failed(self,event):
		log ("WylioXMPP failed")
	
	def disconnected(self,event):
		log("WylioXMPP disconnected")
		
	def send_value(self, signal, value, jid):
		msg = self.connection.Message (sto=jid, stype="normal")
		msg["wylio"]["value"]["signal"] = signal
		msg["wylio"]["value"]["value"] = value
		print msg
		msg.send()
		
	def run_source (self, source, jid):
		print "fsdafasd"
		msg = self.connection.Message (sto=jid, stype="normal")
		print msg
		msg["wylio"]["run"] = source
		#msg["wylio"]["value"]="4082374"
		#msg["wylio"]["value"]["timestamp"]="4082374"
		#msg["wylio"]["value"]["signal"]="some name"
		#msg["wylio"]["value"]["value"]="478923"
		print "message"
		print msg
		msg.send()
	
if __name__ == '__main__':
	xmpp = WylioXMPP ()
	xmpp.connect ("server@ipworkshop.ro", "raspberrypi")