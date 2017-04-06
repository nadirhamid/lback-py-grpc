import grpc
from  . import agent_pb2_grpc
from . import server_pb2
from . import server_pb2_grpc
from lback.utils import lback_agents, lback_backup_chunked_file

class Server(server_pb2_grpc.ServerServicer):
  def __init__(self):
    db_agents = lback_agents()
    self.agents = [] ## STUBS and CHANNELS
    for db_agent in db_agents:
	 channel = grpc.InsecureChannel(db_agent['host']+":"+db_agent['port'])
	 self.agents.append( ( db_agent['id'], agent_pb2_grpc.AgentStub( channel ), ) )

  def _GetAgent(self, agent_id):
    for agent in self.agents:
	 if agent[0]==agent_id:
	     return agent[1]

  def _RouteOnAllAgents(self, fn):
    agents = self.agents
    for agent in agents:
	 agent_channel = agent[ 1 ]
	 for cmd_response in fn( agent_channel ):
	      yield cmd_response
  def RouteBackup(self, request, context):
    def chunked_iterator(agent):
	chunked_file = lback_backup_chunked_file( request.id )
	for backup_file_chunk in chunked_file:
	    yield server_pb2.BackupCmdChunk( id=request.id,raw_data=backup_file_chunk )
    def route_fn(agent ):
	 return agent.DoBackup( chunked_iterator )
    try:
       for cmd_response in self._RouteOnAllAgents( route_fn ):
	  yield cmd_response
    except Exception,ex:
       yield server_pb2.BackupCmdStatus(errored=True)

  def RouteRelocate(self, request, context):  
     src_agent = self._GetAgent( request.src )
     dst_agent = self._GetAgent( request.dst )
     def chunked_iterator():
          for relocate_take_chunk in  src_agent.DoRelocateTake( request ):
	   	yield relocate_take_chunk
     try:
	  for _ in dst_agent.DoRelocateGive( chunked_iterator ):
		 pass
     except Exception,ex:
	  return server_pb2.RelocateCmdStatus(errored=True)
     return server_pb2.RelocateCmdStatus(errored=False)
	 
  def RouteRestore(self, request, context):
     dst_agent = self.GetRestoreCandidate()
     db_backup = lback_backup( request.id )
     restore = Restore( request.id, folder=db_backup['folder'] )
     def chunked_iterator():
          for restore_cmd_chunk in dst_agent.DoRestore( request ):
	       yield restore_cmd_chunk.raw_data
     try:
	 restore.run_chunked( chunked_iterator )
     except Exception,ex:
	 return server_pb2.RestoreCmdStatus(errored=True)
     return server_pb2.RestoreCmdStatus(errored=False)

  def RouteRm(self, request, context):
      all = request.all
      target = request.target
      id = request.id
      def route_fn(agent):
	  status = agent.DoRm(request)
	  yield status
      try:
         if all:
	    for rm_cmd_reply in self._RouteOnAllAgents( route_fn ):
	        yield server_pb2.RmCmdStatus(errored=False)
         else:
	     yield server_pb2.RmCmdStatus(errored=False)
      except Exception,ex:
	 yield server_pb2.RmCmdStatus(errored=True)
