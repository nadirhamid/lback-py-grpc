import grpc 
from . import make_connection_string, safe_rpc
from  . import agent_pb2_grpc
from . import server_pb2
from . import server_pb2_grpc
from . import shared_pb2
from . import shared_pb2_grpc
from traceback import print_exc

from lback.utils import lback_agents, lback_backup_chunked_file, lback_output, lback_backup, lback_agent_is_available, lback_backup_shard_size, lback_backup_shard_start_end
from lback.backup import BackupObject
from lback.restore import Restore

def do_distribution_switch_yield( distribution_strategy, **kwargs ):
   for cmd_response in kwargs[ distribution_strategy ]():
        yield cmd_response
def do_distribution_switch_return( distribution_strategy, **kwargs ):
   return kwargs[ distribution_strategy ] ()
def cmd_response_handler(cmd_response):
   if cmd_response is None:
       return shared_pb2.BackupCmdStatus(errored=True)
   return cmd_response


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
  def FindRestoreCandidate(self, backup, shard=None):
     def route_fn( agent ):
        check_cmd = shared_pb2.CheckCmd(id=backup.id, shard=shard)
        exists = agent[1].DoCheckBackupExists(check_cmd)
        return ( exists, agent, )
     routed = self.RouteOnAllAgents( route_fn )
     for ( check_cmd_resp, agent ) in routed:
       if check_cmd_resp and not (check_cmd_resp.errored):
         return agent
  def RemoveAgent(self, server_object):
     connection_string = make_connection_string( server_object[0] )
     lback_output("Removing AGENT %s"%(connection_string))
     self.agents.remove( server_object )
  def RouteToAgent(self, agent, agent_fn):
     connection_string =  make_connection_string( agent[ 0 ] )
     lback_output("DELIVERING to AGENT %s"%( connection_string))
     result = safe_rpc(agent, agent_fn)
     return result

  def RouteOnAllAgents(self, agent_fn):
    agents = self.agents
    lback_output("ROUTE ON ALL AGENTS")
    lback_output(agents)
    for agent_response in self.RouteToTheseAgents(agents, agent_fn):
        yield agent_response
  def RouteToTheseAgents(self, agents, agent_fn):
     for agent in agents:
       yield self.RouteToAgent(agent, agent_fn)
  def GetEveryAgentPossible(self):
     agents = self.agents
     def filter_fn(agent):
        if lback_agent_is_available( agent[0] ):
            return True
        return False
     return filter( filter_fn, agents )

  def RouteWithShard(self, shard_count, shard_total, db_backup, route_fn):
    while shard_count != shard_total:
      lback_output("RECEIVING SHARD %s"%(shard_count,))
      dst_agent = self.FindRestoreCandidate( db_backup, shard=str( shard_count ) )
      reply = self.RouteOnAgent( dst_agent, route_fn)
      yield reply
      shard_count += 1

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
    backup = BackupObject.find_backup(request.id)
    def do_shared_distribution():
        lback_output("Backup with DISTRIBUTION STRATEGY shared")
        def chunked_iterator(agent):
           lback_output("Ready to pack CHUNKS for backup %s"%request.id)
           chunked_file = lback_backup_chunked_file( request.temp_id )
           for backup_file_chunk in chunked_file:
              lback_output("Packing CHUNK")
              yield shared_pb2.BackupCmdStream( id=request.id,raw_data=backup_file_chunk )
        def route_fn(agent ):
           lback_output("RUNNING CHUNKED ITERATOR")
           iterator = chunked_iterator( agent )
           exists = agent[1].DoCheckBackupExists( shared_pb2.CheckCmd(
              id=request.id ))
           if not exists.errored:
              shared_pb2.BackupCmdStatus(errored=False)
           backup_res = agent[1].DoBackup( iterator )
           lback_output("COMPLETED BACKUP")
           return backup_res
        for cmd_response in self.RouteOnAllAgents( route_fn ) :
            yield cmd_response_handler(cmd_response)
    def do_sharded_distribution():
        lback_output("Backup with DISTRIBUTION STRATEGY sharded")
        shard_count = [ 0 ]
        def chunked_iterator(agent):
           lback_output("Ready to pack shared CHUNKS for backup %s"%request.id)
           shard_start, shard_end = lback_backup_shard_start_end( shard_count[ 0 ], sharded_backup_size )
           chunked_file = lback_backup_chunked_file( request.temp_id, chunk_start=shard_start, chunk_end=shard_end )
           for backup_file_chunk in chunked_file:
              lback_output("Packing CHUNK")
              yield shared_pb2.BackupCmdStream( id=request.id,raw_data=backup_file_chunk, shard=str( shard_count[ 0 ] ) )


        def route_fn( agent ):
           lback_output("RUNNING SHARDED CHUNKED ITERATOR")
           iterator = chunked_iterator( agent )
           exists = agent[1].DoCheckBackupExists( shared_pb2.CheckCmd(
              id=request.id, 
              shard=str(shard_count[ 0 ]) ))
           if not exists.errored:
              return shared_pb2.BackupCmdStatus(errored=False)
           backup_res = agent[1].DoBackup( iterator )
           lback_output("COMPLETED ROUTING SHARDED BACKUP ON ONE AGENT")
           shard_count[ 0 ] += 1
           return backup_res

        agents_possible = self.GetEveryAgentPossible()
        total_shards = len( agents_possible )
        backup.update_field("shards_total", total_shards)
        sharded_backup_size = lback_backup_shard_size( request.temp_id, total_shards )
        for cmd_response in self.RouteToTheseAgents( agents_possible, route_fn ):
            yield cmd_response_handler(cmd_response)
    if backup.distribution_strategy=="sharded":
        iterator = do_sharded_distribution()
    elif backup.distribution_strategy=="shared":
        iterator = do_shared_distribution()
    for cmd_response in iterator:
        yield cmd_response

  def RouteRelocate(self, request, context):  
     lback_output("Received COMMAND RouteRelocate")
     src_agent = self.FindAgent( request.src )
     dst_agent = self.FindAgent( request.dst )
     iterator = None
     def agent_take_fn(agent):
         return agent[1].DoRelocateTake( request )
     def agent_give_fn():
         return agent[1].DoRelocateGive(chunked_iterator())
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
     db_backup = lback_backup( request.id )
     folder = request.folder
     if request.use_temp_folder:
        restore = Restore( request.id, folder=request.folder )
     else:
        restore = Restore( request.id, folder=db_backup.folder )
     def do_restore(iterator):
        restore.run_chunked(iterator)
        return shared_pb2.RestoreCmdStatus(
            errored=False)
        
     def do_shared_restore():
         lback_output("RUNNING SHARED RESTORE")
         dst_agent = self.FindRestoreCandidate( db_backup )
         def agent_restore_fn(agent):
             return agent[1].DoRestore( request )
         def chunked_iterator():
             agent_iterator = self.RouteOnAgent( dst_agent, agent_restore_fn )
             for restore_cmd_chunk in agent_iterator:
               lback_output("Receiving CHUNK")
               if not restore_cmd_chunk:
                  yield None
               else:
                  yield restore_cmd_chunk.raw_data
         return do_restore( chunked_iterator() )
     def do_sharded_restore():
         lback_output("RUNNING SHARDED RESTORE")
         shard_count = [ 0 ]
         shards_total = db_backup.shards_total
         lback_output("TOTAL SHARDS ARE %s"%(shards_total,))

         def agent_restore_fn(agent):
             cmd_request = shared_pb2.RestoreCmd(
                 id=request.id,
                 use_temp_folder=request.use_temp_folder,
                 folder=request.folder,
                 shard=str( shard_count[0] ) )
             return agent[1].DoRestore( cmd_request )
         def chunked_iterator():
             shard_count[0], agent_iterator = self.RouteWithShard(shard_count[0], shards_total, db_backup, agent_restore_fn)
             for restore_cmd_chunk in agent_iterator:
                  lback_output("Receiving CHUNK")
                  if not restore_cmd_chunk:
                      yield None
                  else:
                      yield restore_cmd_chunk.raw_data
         return do_restore(chunked_iterator())
     return do_distribution_switch_return(db_backup.distribution_strategy, 
            shared=do_shared_restore,
            sharded=do_sharded_restore)

  def RouteRm(self, request, context):
      lback_output("Received COMMAND RouteRm")
      all = request.all
      target = request.target
      id = request.id
      db_backup = lback_backup(id)
      def do_shared_rm():
          lback_output("Remove with DISTRIBUTION STRATEGY shared")
          def route_fn(agent):
              status = agent[1].DoRm(request)
              return status
          iterator = self.RouteOnAllAgents( route_fn )
          for rm_cmd_reply in iterator:
             if rm_cmd_reply is None:
                yield shared_pb2.RmCmdStatus(errored=True)
             else:
                lback_output("COMPLETED REMOVE")
                yield rm_cmd_reply
      def do_sharded_rm():
          lback_output("Remove with DISTRIBUTION STRATEGY sharded")
          shard_count = [ 0 ]
          shard_total = db_backup.shard_total
          def route_fn(agent):
              rm_cmd = shared_pb2.RmCmd(
                    id=id,
                    shard=str( shard_count[ 0 ] ) )
              status = agent[1].DoRm(rm_cmd)
              return status
          iterator = self.RouteWithShard(shard_count[ 0 ], shard_total, db_backup, route_fn)
          for rm_cmd_reply in iterator:
             if not rm_cmd_reply:
                yield shared_pb2.RmCmdStatus(errored=True)
             else:
                lback_output("COMPLETED REMOVE")
                yield rm_cmd_reply
      def handle_all_rm():
          if db_backup.distribution_strategy=="shared":
             iterator = do_shared_rm()
          elif db_backup.distribution_strategy=="sharded":
             iterator = do_sharded_rm()
          for cmd_result in iterator:
             if cmd_result.errored:
                yield cmd_result
          yield shared_pb2.RmCmdStatus( errored=False )
      def handle_target_rm():
          lback_output("NOT IMPLEMENTED")
          yield shared_pb2.RmCmdStatus(errored=True)
      iterator = handle_all_rm()
      if not all:
          iterator = handle_target_rm()
      for cmd_result in iterator:
           yield cmd_result
