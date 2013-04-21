import os, traceback, select, signal
INITIALIZED = 0
RUNNING = 1
TERMINATED = 2
ERRORRUNNING = 3
class Program:
	def __init__(self,id,program):
		self.id = id
		self.program = program
		self.exitStatus = None
		self.stdin = [0,0]
		self.stdout = [0,0]
		self.stderr = [0,0]
		self.mesIn = [0,0]
		self.mesOut = [0,0]
		self.pid = 0
		self.status = INITIALIZED
	def run(self,server,jid):		
		self.stdin[0],self.stdin[1] = os.pipe()
		self.stdout[0], self.stdout[1] = os.pipe()
		self.stderr[0], self.stderr[1] = os.pipe()
		self.mesIn[0], self.mesIn[1] = os.pipe()
		self.mesOut[0], self.mesOut[1] = os.pipe()
		
		try:
			self.pid = os.fork()
			if self.pid == 0:
				os.dup2(self.stdin[0],0)
				os.close(self.stdin[1])
				
				os.dup2(self.stdout[1],1)
				os.close(self.stdout[0])
				
				os.dup2(self.stderr[1],2)
				os.close(self.stderr[0])
				
				os.dup2(self.mesIn[0],3)
				os.close(self.mesIn[1])
				
				os.dup2(self.mesOut[1],4)
				os.close(self.mesOut[0])
				
				try:
					os.execvp('python', ['python' , '-u', self.program])
				except OSError:
					traceback.print_exc()
					status = ERRORRUNNING
					os.close(self.stdin[0])
					os.close(self.stdout[0])
					os.close(self.stderr[0])
					os.close(self.mesIn[0])
					os.close(self.mesOut[0])
					
					os.close(self.stdin[1])
					os.close(self.stdout[1])
					os.close(self.stderr[1])
					os.close(self.mesIn[1])
					os.close(self.mesOut[1])					
					os.exit(-1)
				
			else:
				os.close(self.stdout[1])
				os.close(self.stdin[0])
				os.close(self.stderr[1])
				os.close(self.mesOut[1])
				os.close(self.mesIn[0])
				self.status = RUNNING
				epoll = select.epoll()
				epoll.register(self.stdout[0], select.EPOLLIN)
				epoll.register(self.stderr[0], select.EPOLLIN)
				epoll.register(self.mesOut[0], select.EPOLLIN)
				id = 0
				while id == 0:
					events = epoll.poll(0.01)
					for fileno, event in events:
						if fileno == self.stdout[0]:
							message = os.read(self.stdout[0], 10000)
							print "stdout"+message
							server.send_signal_out(jid,message)	
						elif fileno == self.stderr[0]:
							message = os.read(self.stderr[0], 10000)
							print "stderr"+message
							server.send_signal_err(jid,message)	
						elif fileno == self.mesOut[0]:
							message = os.read(self.mesOut[0], 10000)
							print message
							divided_message = message.split('\n')
							for mes in divided_message:
								m = mes.split(' ')
								if len(m) == 2:
									name = m[0]
									value = m[1]
									server.send_value_signal(jid,"0",name,value)							
					id, e = os.waitpid(self.pid,os.WNOHANG)
				self.status = TERMINATED
		except OSError:
			traceback.print_exc()
			status = ERRORRUNNING
			os.close(self.stdin[0])
			os.close(self.stdout[0])
			os.close(self.stderr[0])
			os.close(self.mesIn[0])
			os.close(self.mesOut[0])
			
			os.close(self.stdin[1])
			os.close(self.stdout[1])
			os.close(self.stderr[1])
			os.close(self.mesIn[1])
			os.close(self.mesOut[1])
			
	def sendInput(self, input):
		if self.status == RUNNING:
			os.write(self.stdout[1],input)
			
	def sendSensorInput(self, signal,input):
		if self.status == RUNNING:
			os.write(self.mesIn[1], signal+' '+input+'\n')
			
	def stop(self):
		if self.status == RUNNING:
			os.kill(self.pid, signal.SIGKILL)
		status = TERMINATED
if __name__ == '__main__':
	prog = Program(12,'test.py')
	prog.run()
	#prog.sendInput(7)
	
	
			