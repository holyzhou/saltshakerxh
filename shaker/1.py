#!/usr/bin/python
from shaker_core import *

sapi = SaltAPI()
result = sapi.shell_remote_execution('192.168.10.58', 'w')
print result
