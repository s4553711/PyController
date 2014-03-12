import os
import fnmatch
import re
import subprocess
import sys

class Queue(object):
	def __init__(self):
		self.step_name = ""
		self.prevStateLog = ''
		self.currentStateLog = ''
		self.taskLog = ''
		
	def setTaskLog(self,input):
		self.taskLog = input
	
	def setName(self,input):
		self.step_name = input
	
	def setPrevStateLog(self,input):
		self.prevStateLog = input
	
	def setCurrentStateLog(self,input):
		self.currentStateLog = input
	
	def checkStatus(self,fileName):
		pattern = re.compile(".*?error|.*?stop")
		status = "normal"
		f = open(fileName,"r");
		for line in f:
			if pattern.match(line.strip()):
				status = "error"
				return status
		return status
	
	def run_check(self):
		status = True
		for file in os.listdir('.'):
			if fnmatch.fnmatch(file,self.prevStateLog):
				state = self.checkStatus(file)
				if state == "error": 
					status = False
					return status
		return status
	
	def go_by_cmd(self,input_ar):
		logHandle = open(self.currentStateLog, "w+")
		logHandle.write("[hipipe] start\n")
		
		runCheckResult = self.run_check()
		print "Debug> Run Check for ",self.step_name," : ",runCheckResult
		
		if runCheckResult:
			TasklogHandle = open(self.taskLog, "w+")
			try:
				p = subprocess.Popen(input_ar,stdin=None ,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=1)
				
				while True:
					out = p.stdout.readline()
					if out == '' and p.poll() != None:
						break
					if out != '':
						print "Debug > ",str(out).strip()
						TasklogHandle.write(out)
						TasklogHandle.flush()
						sys.stdout.flush()

				p.communicate()
			except OSError as e:
				print "OSError > ",e.errno
				print "OSError > ",e.strerror
				print "OSError > ",e.filename
			except Exception as ins:
				print "ERROR > ",sys.exc_info()
				print "ERROR > ",type(ins)
				print "ERROR > ",ins.args
				
			TasklogHandle.close()
			print "Debug > Finish"
		else:
			logHandle.write("[hipipe] stop\n")
			logHandle.close()
			return
		
		logHandle.write("[hipipe] end\n")
		logHandle.close()
	
	def go(self):
		logHandle = open(self.currentStateLog, "w+")
		logHandle.write("[hipipe] start\n")
		
		runCheckResult = self.run_check()
		print "Debug> Run Check for ",self.step_name," : ",runCheckResult
		
		if runCheckResult:
			self.run()
		else:
			logHandle.write("[hipipe] stop\n")
			logHandle.close()
			return
		
		logHandle.write("[hipipe] end\n")
		logHandle.close()