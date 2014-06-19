import os
import fnmatch
import re
import subprocess
import sys

class taskDef(object):
	def __init__(self):
		self.step_name = ""
		self.prevStateLog = ''
		self.currentStateLog = ''
		self.taskLog = ''
		self.logFolder = ''

	def setLogFolder(self,input):
		self.logFolder = input
		if not os.path.isdir(self.logFolder):
			os.makedirs(self.logFolder)
		
	def getLogFolder(self):
		return self.logFolder
		
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
		for file in os.listdir(self.getLogFolder()):
			if fnmatch.fnmatch(file,os.path.basename(self.prevStateLog)):
				state = self.checkStatus(self.getLogFolder()+"/"+file)
				if state == "error" or state == "stop": 
					status = False
					return status
		return status
	
	def go_by_cmd(self,input_ar):
		logHandle = open(self.getLogFolder()+"/"+self.currentStateLog, "w+")
		logHandle.write("[hipipe] start\n")
		logHandle.flush()
		
		runCheckResult = self.run_check()
		
		if runCheckResult:
			TasklogHandle = open(self.getLogFolder()+"/"+self.taskLog, "w+")
			try:
				p = subprocess.Popen(input_ar,stdin=None ,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=1)
				
				while True:
					out = p.stdout.readline()
					if out == '' and p.poll() != None:
						break
					if out != '':
						TasklogHandle.write(out)
						TasklogHandle.flush()
						sys.stdout.flush()

				p.communicate()
				if p.poll() >= 1:
					logHandle.write("[hipipe] error\n")
					logHandle.close()
					return
				
			except OSError as e:
				print "OSError > ",e.errno
				print "OSError > ",e.strerror
				print "OSError > ",e.filename
				logHandle.write("[hipipe] error\n")
			except Exception as ins:
				print "ERROR > ",sys.exc_info()
				print "ERROR > ",type(ins)
				print "ERROR > ",ins.args
				logHandle.write("[hipipe] error\n")
				
			TasklogHandle.close()
		else:
			logHandle.write("[hipipe] stop\n")
			logHandle.close()
			return
		
		logHandle.write("[hipipe] end\n")
		logHandle.close()
	
	def go(self):
		logHandle = open(self.getLogFolder()+"/"+self.currentStateLog, "w+")
		logHandle.write("[hipipe] start\n")
		logHandle.flush()
		
		runCheckResult = self.run_check()
		
		if runCheckResult:
			self.run()
		else:
			logHandle.write("[hipipe] stop\n")
			logHandle.flush()
			logHandle.close()
			return
		
		logHandle.write("[hipipe] end\n")
		logHandle.flush()
		logHandle.close()