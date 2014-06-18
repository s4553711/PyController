## Task Controller in Python
This library is a wrapper to control jobs written in scripting language. Here are some featrues below: 

1. Job dependence
2. Logging
3. Job error handling

This lib can receive the exit code from script and record its status in log file. If the previous job status is error or stop, the next job will not execute but just stop. 


