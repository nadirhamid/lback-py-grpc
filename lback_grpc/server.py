import grpc
from . import make_connection_string, safe_rpc
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
       self.AddAgentByDbObject(agent_object)

  def AddAgentByDbObject(self, agent_object):
     connection_string = make_connection_string( agent_object )
     lback_output("Registering AGENT %s"%(connection_string))
     channel = grpc.insecure_channel(connection_string)
     self.agents.append( ( agent_object, agent_pb2_grpc.AgentStub( channel ), ) )
  def FindAgent(self, agent_id):
    for agent in self.agents:
     if agent[0].id==agent_id:
         return agent
  def FindRestoreCandidate(self):
     return self.agents[0]
  def RemoveAgent(self, server_object):
     connection_string = make_connection_string( server_object[0] )
     lback_output("Removing AGENT %s"%(connection_string))
     self.agents.remove( server_object )
  def RouteOnAllAgents(self, agent_fn):
    agents = self.agents
    lback_output("ROUTE ON ALL AGENTS")
    lback_output(agents)
    for agent in agents:
       agent_object = agent[ 0 ] 
       agent_channel = agent[ 1 ]
       connection_string =  make_connection_string( agent_object )
       lback_output("DELIVERING to AGENT %s"%( connection_string))
       result = safe_rpc(agent, agent_fn)
       yield result
  def RouteOnAgent(self, agent, agent_fn):
     lback_output("ROUTE ON AGENT")
     agent_object = agent[0]
     connection_string =  make_connection_string( agent_object )
     lback_output("DELIVERING to AGENT %s"%( connection_string))
     reply =  safe_rpc(agent, agent_fn)
     lback_output("RESPONSE")
     lback_output( reply )
     return reply

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
    iterator = self.RouteOnAllAgents( route_fn )
    for cmd_response in iterator:
      if cmd_response is None:
          yield shared_pb2.BackupCmdStatus(errored=True)
      else:
          yield cmd_response
  def RouteRelocate(self, request, context):  
     lback_output("Received COMMAND RouteRelocate")
     src_agent = self.FindAgent( request.src )
     dst_agent = self.FindAgent( request.dst )
     iterator = None
     def agent_take_fn(agent):
         return agent.DoRelocateTake( request )
     def agent_give_fn():
         return agent.DoRelocateGive(chunked_iterator())
     def give_loop_all(iterator):
         for _ in iterator:
             pass

     def chunked_iterator():
         iterator = self.RouteOnAgent( src_agent, agent_take_fn )
         if not iterator:
             yield None
         else:
             for relocate_take_chunk in  iterator:
                 yield relocate_take_chunk
     iterator = self.RouteOnAgent( dst_agent, agent_give_fn )
     if not iterator:
         return shared_pb2.RelocateCmdStatus(errored=True)
     give_loop_all(iterator)
     lback_output("COMPLETED RELOCATE")
     return shared_pb2.RelocateCmdStatus(errored=False)
     
  def RouteRestore(self, request, context):
     lback_output("Received COMMAND RouteRestore")
     dst_agent = self.FindRestoreCandidate()
     db_backup = lback_backup( request.id )
     restore = Restore( request.id, folder=db_backup.folder )
     def agent_restore_fn(agent):
         return agent.DoRestore( request )
     def chunked_iterator():
         agent_iterator = self.RouteOnAgent( dst_agent, agent_restore_fn )
         for restore_cmd_chunk in agent_iterator:
           lback_output("Receiving CHUNK")
           if not restore_cmd_chunk:
              yield None
           else:
              yield restore_cmd_chunk.raw_data
     try:
        iterator = chunked_iterator()
        restore.run_chunked( iterator )
        lback_output("COMPLETED RESTORE")
        return shared_pb2.RestoreCmdStatus(errored=False)
     except Exception,ex:
        return shared_pb2.RestoreCmdStatus(errored=True)

  def RouteRm(self, request, context):
      lback_output("Received COMMAND RouteRm")
      all = request.all
      target = request.target
      id = request.id
      def route_fn(agent):
          status = agent.DoRm(request)
          yield status
      def handle_all_rm():
          iterator = self.RouteOnAllAgents( route_fn )
          for rm_cmd_reply in iterator:
             if not rm_cmd_reply:
                yield shared_pb2.RmCmdStatus(errored=True)
             else:
                lback_output("COMPLETED REMOVE")
                yield shared_pb2.RmCmdStatus(errored=True)
      def handle_target_rm():
          lback_output("NOT IMPLEMENTED")
          yield shared_pb2.RmCmdStatus(errored=True)
      if not all:
          handle_target_rm()
      handle_all_rm()
