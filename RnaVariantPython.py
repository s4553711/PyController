#!/usr/bin/python
import Alignment
import os
import task
import Jobs
import sys

print sys.argv[1]

print "Log> Job Start"
job1 = Jobs.job1()
job1.setName("job1");
#job1.setPrevStateLog('first.hipipe')
job1.setLogFolder("./log")
job1.setCurrentStateLog('j1.hipipe')
job1.setTaskLog('j1.out')
job1.go_by_cmd(['bash','./step1.sh'])
#job1.go();

job2 = Jobs.job1()
job2.setName("job2");
job2.setPrevStateLog('j1.hipipe')
job2.setLogFolder("./log")
job2.setCurrentStateLog('j2.hipipe')
job2.setTaskLog('j2.out')
job2.go_by_cmd(['bash','./step2.sh'])

job3 = Jobs.job1()
job3.setName("job3");
job3.setPrevStateLog('j2.hipipe')
job3.setLogFolder("./log")
job3.setCurrentStateLog('j3.hipipe')
job3.setTaskLog('j3.out')
job3.go_by_cmd(['bash','./step3.sh'])


#bowtie = Alignment.Bowtie()
#bowtie.addFastaList(["A_10w_R1_40.fastq".strip(),"A_10w_R2_40.fastq".strip()])
#bowtie.setProjectFolder("/work/s4553711/RnaVariantPython")
#bowtie.setRef("/home/s4553711/work/ref/human_g1k_v37/ref")
#bowtie.addPath("/home/s4553711/work/tophat/bin")
#bowtie.setThread(2)
#bowtie.getFastqFromFolder("/home/s4553711/work/RnaVariantPython/fastq")
#bowtie.setPrevStateLog('*.gatk.hipipe')
#bowtie.setCurrentStateLog('tophat.hipipe')
#bowtie.setName('Tophat')
#bowtie.setTaskLog('tophat.out')
#bowtie.go()
print "Log> Job End"

#q1 = Queue.Queue()
#q1.run_check()
