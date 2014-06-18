import subprocess
import sys
import os
import re
import shutil
import task

class Bowtie(task.taskDef):
	def __init__(self):
		super(Bowtie, self).__init__()
		self.debug = 0
		self.message = "tophat"
		self.project_folder = ""
		self.bowtie_ref = "/home/s4553711/work/ref/human_g1k_v37/ref"
		self.outputFolder = "./tophat_out"
		self.fastq = []
		self.fastq_reads = [[],[]]
		self.thread = 1
		self.stopSignal = 0
		self.SampleName = ""
 
	def setSampleName(self,input):
		self.SampleName = input

	def getFastqFromFolder(self,input):
		zip_files = [f for f in os.listdir(input) if f.endswith('.gz')]
		for file in zip_files:
			m = re.search('(\S+)_R([0-9])_\S+',file)
			if m.group(0):
				if self.debug == 1: print " Debug > get read file: ",file," ... ",m.group(1)," .. ",m.group(2)
				if int(m.group(2)) == 1:
					self.fastq_reads[0].append(input+"/"+file)
				else:
					self.fastq_reads[1].append(input+"/"+file)

	def checkBeforeRun(self):
		# the ncessary file extension for bowite2 index
		bowtie_idx = ["1","2","3","4",'rev.1','rev.2']
		
		# Check if the bowtie2 index files are exist
		if os.path.isdir(self.outputFolder): shutil.rmtree(self.outputFolder)
		for f in bowtie_idx:
			if not os.path.isfile(self.bowtie_ref+"."+f+".bt2"): self.stopSignal+=1

	def addPath(self,input):
		os.environ["PATH"] = os.environ["PATH"]+":"+input

	def setupEnv(self):
		os.environ["PATH"] = os.environ["PATH"]+":/home/s4553711/work/bowtie2-2.1.0:/home/s4553711/work/samtools-0.1.19:/home/s4553711/work/tophat/bin"
		
	def getLog(self):
		return self.message
  
	def setRef(self,input):
		self.bowtie_ref = input

	def setThread(self,input):
		self.thread = input

	def setProjectFolder(self,input):
		self.project_folder = input
  
	def addFastaList(self,input):
		self.fastq.extend(input);
	
	def getDebug(self):
		print "Debug > fastq: ",self.fastq
		print "Debug > ref: ",self.bowtie_ref
	
	def run(self):
		com_ar = ["tophat","-g","1","-p",str(self.thread),self.bowtie_ref,",".join(self.fastq_reads[0]),",".join(self.fastq_reads[1])]
		#com_ar = ["/home/s4553711/work/tophat/bin/tophat","-g","1","-p",str(self.thread),self.bowtie_ref,reada,readb]
		print "Argument> ",com_ar
		
		self.setupEnv()
		self.checkBeforeRun()
		
		if self.stopSignal >= 1:
			print "Debug> Stop Program";
			exit
		
		output = ""
		error = ""
		logHandle = open(self.taskLog, "w+")
		
		try:
			#bowtie_result = subprocess.Popen(com_ar,stdin=None ,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
			#bowtie_result = subprocess.Popen(com_ar,stdin=None ,stdout=logHandle,stderr=subprocess.PIPE)
			
			# STDERR is redirected to STDOUT
			bowtie_result = subprocess.Popen(com_ar,stdin=None ,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=1)
			
			while True:
				out = bowtie_result.stdout.readline()
				if out == '' and bowtie_result.poll() != None:
					break
				if out != '':
					print "Debug > ",str(out).strip()
					logHandle.write(out)
					logHandle.flush()
					sys.stdout.flush()

			bowtie_result.communicate()
		except OSError as e:
			print "OSError > ",e.errno
			print "OSError > ",e.strerror
			print "OSError > ",e.filename
		except Exception as ins:
			print "ERROR > ",sys.exc_info()
			print "ERROR > ",type(ins)
			print "ERROR > ",ins.args

		logHandle.close()
		print "Debug > Finish"
		
	pass