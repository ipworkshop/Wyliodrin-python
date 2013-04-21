from sleekxmpp import ClientXMPP, Callback, StanzaPath
import logging
from program import Program
from sleekxmpp.xmlstream.stanzabase import ElementBase, ET, JID, register_stanza_plugin
from sleekxmpp.stanza.message import Message
import thread
import traceback

program = None

def log(message):
	print message
class ValueStanza(ElementBase):	
	namespace = 'wylio'
	name = 'value'
	plugin_attrib = 'value'
	interfaces = set(('timestamp', 'signal', 'value','program'))
	sub_interfaces = tuple ()

class WylioStanza(ElementBase):	
	namespace = 'wylio'
	name = 'wylio'
	plugin_attrib = 'wylio'
	interfaces = set(('run', 'source', 'in', 'out', 'err'))
	sub_interfaces = interfaces
	subitem = (ValueStanza,)
	
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
	def send_value_signal(self,jid,timestamp,name,value):
		msg = self.connection.Message (sto=jid, stype="normal")
		msg["wylio"]["value"]["timestamp"]=timestamp
		msg["wylio"]["value"]["signal"]=name
		msg["wylio"]["value"]["value"]=value
		#print "message"
		#print msg
		msg.send()
	def send_signal_out(self,jid,value):
		msg = self.connection.Message (sto=jid, stype="normal")
		msg["wylio"]["out"]=value
		#print "message"
		#print msg
		msg.send()
	def send_signal_err(self,jid,value):
		msg = self.connection.Message (sto=jid, stype="normal")
		msg["wylio"]["err"]=value
		#print "message"
		#print msg
		msg.send()
	def message_wylio(self, event):
		global program
		try:
			log("WylioServer message wylio received")
			print event['wylio']
			if event['wylio']['run']:
				#print "run in wylio"
				code = event['wylio']['run']
				file = open('received_program.py', 'w')
				file.write(code)
				file.close()
				if program != None:
					program.stop()
				program = Program(1,'received_program.py')
				try:
					thread.start_new_thread(program.run,(self,event['from']))
					print "created thread"
				except:
					traceback.print_exc()
					log("Error creating thread")
			if event['wylio']['value']:
				signal = event['wylio']['value']['signal']
				value = event['wylio']['value']['value']
				if program != None:
					program.sendSensorInput(signal,value)
		except:
			traceback.print_exc()
			
	def connect(self,jid,password):
		if self.connection == None:
			self.connection = ClientXMPP(jid, password)
		register_stanza_plugin (Message, WylioStanza)
		register_stanza_plugin (WylioStanza, ValueStanza)
		self.connection.add_event_handler("connected", self.connected)
		self.connection.add_event_handler("disconnected", self.disconnected)
		self.connection.add_event_handler("failed_auth", self.failed_auth)
		self.connection.add_event_handler("session_start", self.start)
		self.connection.add_event_handler("message", self.message)
		self.connection.register_handler(Callback("Wylio", StanzaPath("message/wylio"), self.message_wylio))
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
	file.close()
	server.connect(jid, password)
	
if __name__ == '__main__':
	main()