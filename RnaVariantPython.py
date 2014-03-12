#!/usr/bin/python
import Alignment
import os
import Queue
import Jobs

print "Log> Job Start"
job1 = Jobs.job1()
job1.setName("gatk");
job1.setPrevStateLog('first.hipipe')
job1.setCurrentStateLog('1.gatk.hipipe')
job1.setTaskLog('gatk.out')
job1.go_by_cmd(['ls','-al'])

bowtie = Alignment.Bowtie()
bowtie.addFastaList(["A_10w_R1_40.fastq".strip(),"A_10w_R2_40.fastq".strip()])
bowtie.setProjectFolder("/work/s4553711/RnaVariantPython")
bowtie.setRef("/home/s4553711/work/ref/human_g1k_v37/ref")
bowtie.addPath("/home/s4553711/work/tophat/bin")
bowtie.setThread(2)
bowtie.getFastqFromFolder("/home/s4553711/work/RnaVariantPython/fastq")
bowtie.setPrevStateLog('*.gatk.hipipe')
bowtie.setCurrentStateLog('tophat.hipipe')
bowtie.setName('Tophat')
bowtie.setTaskLog('tophat.out')
bowtie.go()
print "Log> Job End"

#q1 = Queue.Queue()
#q1.run_check()
