#!/usr/bin/python
import os
import sys
import fnmatch
import re

state_log = {
	"qc":"qc1.hipipe",
	"tophat":"tophat.hipipe",
	"split":".split.*.hipipe",
	"gatk":".gatk.*.hipipe",
	"catVcf":"catvcf.hipipe",
	"vcfByS":"vcfbys.*.hipipe"
}

p_start = re.compile(".*?start")
p_end = re.compile(".*?end")
p_error = re.compile(".*?error")
p_stop = re.compile(".*?stop")

def checkFileStatus(input):
	num_error = 0
	num_stop = 0
	num_start = 0
	num_end = 0
	status = ""

	f = open(input,"r");
	for line in f:
		if p_error.match(line.strip()): 
			num_error += 1
			break
		if p_stop.match(line.strip()): 
			num_stop += 1
			break
		if p_start.match(line.strip()): 
			num_start += 1
		if p_end.match(line.strip()): 
			num_end += 1

	return num_start,num_end,num_error,num_stop

def getStatus(cwd_path,pattern):
	status = None
	num_error = 0
	num_stop = 0
	num_start = 0
	num_end = 0
	diff_num = 0
	
	for file in os.listdir(cwd_path+"/log"):
		if fnmatch.fnmatch(file,os.path.basename(pattern)):
			tmp_start,tmp_end,tmp_error,tmp_stop = checkFileStatus(cwd_path+"/log/"+file)
			num_start += tmp_start
			num_end += tmp_end
			num_error += tmp_error
			num_stop += tmp_stop

	diff_num = num_start - num_end

	if num_error > 1 or num_stop > 1:
		status = "error"
	elif diff_num == 0:
		status = "done"
	else:
		status = "running ",str(diff_num)

	if 0:
		print "start> start",num_start;
		print "start> end",num_end;
		print "start> stop",num_stop;
		print "start> errror",num_error;

	return status

for key in state_log:
	step_state = getStatus(sys.argv[1],state_log[str(key)])
	print "Log> ",key,":",step_state
