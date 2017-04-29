import grpc
from  . import agent_pb2_grpc
from . import server_pb2
from . import server_pb2_grpc
from . import shared_pb2
from . import shared_pb2_grpc
from traceback import print_exc

from lback.utils import lback_agents, lback_backup_chunked_file, lback_output, lback_backup
from lback.restore import Restore

class Server(server_pb2_grpc.ServerServicer):
  def __init__(self):
    agent_objects = lback_agents()
    self.agents = [] ## STUBS and CHANNELS
    for agent_object in agent_objects:
     connection_string = agent_object.host+":"+agent_object.port
     lback_output("Registering AGENT %s"%(connection_string))
     channel = grpc.insecure_channel(connection_string)
     self.agents.append( ( agent_object, agent_pb2_grpc.AgentStub( channel ), ) )

  def _GetAgent(self, agent_id):
    for agent in self.agents:
     if agent[0]==agent_id:
         return agent[1]
  def _GetRestoreCandidate(self):
     return self.agents[0][1]

  def _RouteOnAllAgents(self, fn):
    agents = self.agents
    for agent in agents:
       agent_object = agent[ 0 ] 
       agent_channel = agent[ 1 ]
       connection_string = agent_object.host+":"+agent_object.port
       lback_output("DELIVERING to AGENT %s"%( connection_string))
       result = fn( agent_channel )
       yield result
  def RouteBackup(self, request, context):
    lback_output("Received COMMAND RouteBackup")
    def chunked_iterator(agent):
       lback_output("Ready to pack CHUNKS for backup %s"%request.id)
       chunked_file = lback_backup_chunked_file( request.temp_id )
       for backup_file_chunk in chunked_file:
          lback_output("Packing CHUNK")
          yield shared_pb2.BackupCmdStream( id=request.id,raw_data=backup_file_chunk )
    def route_fn(agent ):
       lback_output("RUNNING CHUNKED ITERATOR")
       iterator = chunked_iterator( agent )
       backup_res = agent.DoBackup( iterator )
       lback_output("COMPLETED BACKUP")
       return backup_res
    try:
       iterator = self._RouteOnAllAgents( route_fn )
       for cmd_response in iterator:
           yield cmd_response
    except Exception,ex:
       print_exc( ex )
       yield shared_pb2.BackupCmdStatus(errored=True)

  def RouteRelocate(self, request, context):  
     lback_output("Received COMMAND RouteRelocate")
     src_agent = self._GetAgent( request.src )
     dst_agent = self._GetAgent( request.dst )
     def chunked_iterator():
         iterator = src_agent.DoRelocateTake( request )
         for relocate_take_chunk in  iterator:
             yield relocate_take_chunk
     try:
         iterator = dst_agent.DoRelocateGive(chunked_iterator())
         for _ in iterator:
              pass
     except Exception,ex:
         print_exc( ex )
         return shared_pb2.RelocateCmdStatus(errored=True)

     lback_output("COMPLETED RELOCATE")
     return shared_pb2.RelocateCmdStatus(errored=False)
     
  def RouteRestore(self, request, context):
     lback_output("Received COMMAND RouteRestore")
     dst_agent = self._GetRestoreCandidate()
     db_backup = lback_backup( request.id )
     restore = Restore( request.id, folder=db_backup.folder )
     agent_iterator = dst_agent.DoRestore( request )
     def chunked_iterator():
         for restore_cmd_chunk in agent_iterator:
             yield restore_cmd_chunk.raw_data
     try:
         iterator = chunked_iterator()
         restore.run_chunked( iterator )
     except Exception,ex:
         print_exc( ex )
         return shared_pb2.RestoreCmdStatus(errored=True)

     lback_output("COMPLETED RESTORE")
     return shared_pb2.RestoreCmdStatus(errored=False)

  def RouteRm(self, request, context):
      lback_output("Received COMMAND RouteRm")
      all = request.all
      target = request.target
      id = request.id
      def route_fn(agent):
          status = agent.DoRm(request)
          yield status
      try:
          if all:
              iterator = self._RouteOnAllAgents( route_fn )
              for rm_cmd_reply in iterator:
                  yield shared_pb2.RmCmdStatus(errored=False)
                  lback_output("COMPLETED REMOVE")
          else:
              yield shared_pb2.RmCmdStatus(errored=False)
              lback_output("COMPLETED REMOVE")
      except Exception,ex:
          print_exc( ex )
      yield shared_pb2.RmCmdStatus(errored=True)
