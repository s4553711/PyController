import time
import task

class job1(task.taskDef):
	def __init__(self):
		super(job1, self).__init__()
		
	def run(self):
		print "I am ",self.step_name
		time.sleep(5)
