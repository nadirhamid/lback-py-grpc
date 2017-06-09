import time
import socket
from lback.agent import AgentObject

## AgentServerObject
## adds properties for server to agent
## response latency
class AgentServerObject(AgentObject):
  def __init__(self, *args, **kwargs):
    super(AgentServerObject, self).__init__(*args, **kwargs)
    self.determine_latency()
  def determine_latency(self):
    start = time.time()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    sock.connect_ex((self.host, int( self.port ) ))
    self.latency = time.time()-start
  def get_latency(self):
    return self.latency
