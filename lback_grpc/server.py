import grpc 
from . import make_connection_string, safe_rpc
from  . import agent_pb2_grpc
from . import server_pb2
from . import server_pb2_grpc
from . import shared_pb2
from . import shared_pb2_grpc
from . import protobuf_empty_to_none
from .server_scheduler import ServerScheduler
from .server_exceptions import ServerAgentNotFoundException
from .sharded_iterator import ShardedIterator
from .agent_server_object import AgentServerObject
from traceback import print_exc

from lback.utils import lback_agents, lback_backup_chunked_file, lback_output, lback_backup, lback_agent_is_available, lback_backup_shard_size, lback_backup_shard_start_end, lback_backup_remove
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

def verify_errored(resp):
   pass


class Server(server_pb2_grpc.ServerServicer, ServerScheduler):
  def __init__(self):
    agent_objects = lback_agents(transform_cls=AgentServerObject)
    self.agents = [] ## STUBS and CHANNELS
    self.locked = False
    for agent_object in agent_objects:
       self.AddAgentByDbObject(agent_object)

  def Lock(self):
     lback_output("LOCKING SERVER")
     self.locked = True
  def Unlock(self):
     lback_output("UNLOCKING SERVER")
     self.locked =False

  
  def WithLockStream( fn ):
    def locked_fn( *args ):
            self = args[0]
            self.Lock()
            yielded_results = fn( *args )
            for result in yielded_results:
                yield result
            self.Unlock()
    return locked_fn

  def WithLock( fn ):
    def locked_fn( *args ):
            self = args[ 0 ]
            self.Lock()
            result = fn( *args )
            self.Unlock()
            return result
    return locked_fn


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
     def filter_fn( agent ):
        if not lback_agent_is_available( agent[0] ):
           return False
        def agent_fn(agent):
            check_cmd = shared_pb2.CheckCmd(id=backup.id, shard=shard)
            lback_output(
                "CHECKING IF BACKUP EXISTS ID: %s, SHARD: %s ON AGENT %s"%( backup.id, shard, make_connection_string(agent[0]) ) 
            )
            exists = agent[1].DoCheckBackupExists(check_cmd)
            return exists
        reply = self.RouteToAgent( agent, agent_fn )
        return not reply.errored
     def agent_key_getter( agent ):
        return agent[0].latency

     filtered = filter( filter_fn, self.agents )
     if not len( filtered ) > 0:
        return None
     lback_output("DETERMINING BEST AGENT BY LATENCY")
     by_latency = sorted(filtered, key=agent_key_getter)
     lback_output("BEST AGENT FOR RESTORE IS %s"%( make_connection_string( by_latency[0][0] ) ))
     return by_latency[ 0 ]

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
    def filter_fn( agent ):
       return lback_agent_is_available( agent[0] )
    agents = filter( filter_fn, self.agents )
    lback_output("ROUTE ON ALL AGENTS")
    lback_output(agents)
    for agent_response in self.RouteToTheseAgents(agents, agent_fn):
        yield agent_response
 
  def RouteToTheseAgents(self, agents, agent_fn):
     for agent in agents:
       yield self.RouteToAgent(agent, agent_fn)
  def FetchEveryAgentPossible(self):
     agents = self.agents
     def filter_fn(agent):
        if lback_agent_is_available( agent[0] ):
            return True
        return False
     return filter( filter_fn, agents )

  def FetchAllAgentsByIds(self, ids):
     agents = self.agents
     def filter_fn(agent):
         if ( agent[0].id in ids ) and  ( lback_agent_is_available( agent[ 0 ] ) ):
            return True
         return False
     return filter( filter_fn, agents )

  def FetchAgentById(self, id):
     def filter_fn(agent):
         if ( agent[0].id == id ):
            return True
         return False
     found_agents = filter( filter_fn, self.agents )
     if not len( found_agents ) > 0:
        raise ServerAgentNotFoundException("Agent was not found.")
     return found_agents[ 0 ]

  def RouteWithShard(self, sharded_iterator, db_backup, route_fn):
    while sharded_iterator.get_count() != sharded_iterator.get_total():
      shard_count = sharded_iterator.get_count()
      lback_output("RECEIVING SHARD %s"%(shard_count,))
      dst_agent = self.FindRestoreCandidate( db_backup, shard=str( shard_count ) )
      reply = self.RouteOnAgent( dst_agent, route_fn)
      for cmd_response in reply:
        yield cmd_response
      sharded_iterator.increment_count()

  def RouteOnAgent(self, agent, agent_fn):
     lback_output("ROUTE ON AGENT")
     agent_object = agent[0]
     connection_string =  make_connection_string( agent_object )
     lback_output("DELIVERING to AGENT %s"%( connection_string))
     reply =  safe_rpc(agent, agent_fn)
     lback_output("RESPONSE")
     lback_output( reply )
     return reply

  @WithLockStream
  def RouteBackup(self, request, context):
    lback_output("Received COMMAND RouteBackup")
    agents = self.FetchAllAgentsByIds( request.agent_ids )
    id = request.id
    folders = request.folder
    encryption_key = request.encryption_key
    distribution_strategy = request.distribution_strategy
    diff = request.diff
    did_backup = [ False ]
    folder = None
    agent = self.FetchAgentById( request.target )
    if not len( request.agent_ids ) > 0:
       agents = self.FetchEveryAgentPossible()
    def do_backup():
        if did_backup[ 0 ]:
            return
        if not diff:
            backup_res = agent[1].DoBackupAcceptFull( shared_pb2.BackupCmdAcceptFull(
                 id=id,
                 folder=folder,
                 encryption_key=encryption_key) )
        else:
            def diff_restore_iterator():
                for chunk in restore_backup_file:
                    yield shared_pb2.DoBackupAcceptDiff(
                        id=id,
                        folder=folder,
                        encryption_key=encryption_key,
                        raw_data=chunk)
            restore_res = self.RouteRestore(shared_pb2.RestoreCmd(
                id=backup_obj.id,
                skip_run=True), None)
            verify_errored( restore_res )
            restore_backup_file = lback_backup_chunked_file(lback_id(id, suffix="R"))
            backup_res = agent[1].DoBackupAccept(diff_restore_iterator())
        verify_errored( backup_res )
        did_backup[ 0 ] = True

    def do_backup_and_fetch_chunks(take_shard=None):
        do_backup()
        return agent[1].DoRelocateTake( shared_pb2.RelocateCmdTake(
            id=id,
            folder=folder,
            shard=take_shard,
            delete=False) )
    def do_shared_distribution():
        lback_output("Backup with DISTRIBUTION STRATEGY shared")
        def chunked_iterator(agent):
           lback_output("Ready to pack CHUNKS for backup %s"%request.id)
           chunked_file = do_backup_and_fetch_chunks()
           for backup_file_chunk in chunked_file:
              lback_output("Packing CHUNK")
              yield shared_pb2.BackupCmdStream( id=id,folder=folder,raw_data=backup_file_chunk )
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
        for cmd_response in self.RouteToTheseAgents( agents, route_fn ):
            yield cmd_response_handler(cmd_response)
    def do_sharded_distribution():
        lback_output("Backup with DISTRIBUTION STRATEGY sharded")
        shard_count = [ 0 ]
        def chunked_iterator(agent):
           lback_output("Ready to pack shared CHUNKS for backup %s"%request.id)
           shard_start, shard_end = lback_backup_shard_start_end( shard_count[ 0 ], sharded_backup_size )
          
           chunked_file = do_backup_and_fetch_chunks( shard_count )
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

        agents_possible = self.FetchEveryAgentPossible()
        total_shards = len( agents_possible )
        backup.update_field("shards_total", total_shards)
        sharded_backup_size = lback_backup_shard_size( request.temp_id, total_shards )
        for cmd_response in self.RouteToTheseAgents( agents_possible, route_fn ):
            yield cmd_response_handler(cmd_response)
    for folder_name in folders:
        folder = folder_name
        lback_output("ROUTING BACKUP FOR FOLDER %s"%( folder ) )
        if distribution_strategy=="sharded":
            iterator = do_sharded_distribution()
        elif distribution_strategy=="shared":
            iterator = do_shared_distribution()
        for cmd_response in iterator:
            yield cmd_response
    lback_output("REMOVING TEMP BACKUP")
    lback_backup_remove(request.temp_id)

  @WithLock
  def RouteRelocate(self, request, context):  
     lback_output("Received COMMAND RouteRelocate")
     src_agent = self.FindAgent( request.src )
     dst_agent = self.FindAgent( request.dst )
     backup = lback_backup( request.id )
     shard = request.shard
     iterator = None
     def agent_take_fn(agent):
         lback_output("Running Relocate TAKE")
         return agent[1].DoRelocateTake( 
                shared_pb2.RelocateCmdTake(
                    folder=backup.folder,
                    shard=shard,
                    id=request.id))
     def agent_give_fn(agent):
         lback_output("Running Relocate GIVE")
         return agent[1].DoRelocateGive(chunked_iterator())
     def chunked_iterator():
         iterator = self.RouteOnAgent( src_agent, agent_take_fn )
         if not iterator:
             yield None
         else:
             for relocate_take_chunk in  iterator:
                 lback_output("Packing Relocate CHUNK")
                 yield shared_pb2.RelocateCmdGiveStream(
                        id=backup.id,
                        raw_data=relocate_take_chunk.raw_data,
                        shard=shard,
                        folder=backup.folder )
     result = self.RouteOnAgent( dst_agent, agent_give_fn )
     lback_output("COMPLETED RELOCATE")
     return shared_pb2.RelocateCmdStatus(
        errored=result.errored)
 
  @WithLock    
  def RouteRestore(self, request, context):
     lback_output("Received COMMAND RouteRestore")
     db_backup = lback_backup( request.id )
     folder = request.folder
     target = request.target
     lback_output("TARGET %s"%(target))
     restore_kwargs = dict( 
         folder = ( request.folder if request.use_temp_folder else db_backup.folder ),
         run = not request.skip_run ) 
     restore = Restore( request.id, **restore_kwargs )

     def do_restore(iterator):
         def agent_restore_accept_fn(agent):
            return agent[1].DoRestoreAccept(iterator)

         if request.target:
            target_agent = self.FetchAgentById(target)
            result = self.RouteOnAgent(target_agent, agent_restore_accept_fn)
            return shared_pb2.RestoreCmdStatus(errored=result.errored)
         restore.run_chunked(iterator)
         return shared_pb2.RestoreCmdStatus(
            errored=False)
        
     def do_shared_restore():
         lback_output("RUNNING SHARED RESTORE")
         dst_agent = self.FindRestoreCandidate( db_backup )
         if not dst_agent:
            return shared_pb2.RestoreCmdStatus(
                errored=True)
         def agent_restore_fn(agent):
             return agent[1].DoRestore( request )
         def chunked_iterator():
             agent_iterator = self.RouteOnAgent( dst_agent, agent_restore_fn )
             for restore_cmd_chunk in agent_iterator:
               lback_output("Receiving CHUNK")
               if not restore_cmd_chunk:
                  yield None
               else:
                  yield shared_pb2.RestoreAcceptCmd(
                     id=request.id,
                     folder=restore_kwargs['folder'],
                     raw_data=restore_cmd_chunk.raw_data)
         return do_restore( chunked_iterator() )
     def do_sharded_restore():
         lback_output("RUNNING SHARDED RESTORE")
         shard_count = 0
         shards_total = db_backup.shards_total
         sharded_iterator = ShardedIterator( shard_count, shards_total )
         lback_output("TOTAL SHARDS ARE %s"%(shards_total,))

         def agent_restore_fn(agent):
             cmd_request = shared_pb2.RestoreCmd(
                 id=request.id,
                 use_temp_folder=request.use_temp_folder,
                 folder=restore_kwargs['folder'],
                 shard=str( sharded_iterator.get_count() ) )
             for reply in  agent[1].DoRestore( cmd_request ):
                yield reply
         def chunked_iterator():
             agent_iterator = self.RouteWithShard(sharded_iterator, db_backup, agent_restore_fn)
             for restore_cmd_chunk in agent_iterator:
                  lback_output("Receiving CHUNK")
                  if not restore_cmd_chunk:
                      yield None
                  else:
                     yield shared_pb2.RestoreAcceptCmd(
                     id=request.id,
                     folder=request.folder,
                     raw_data=restore_cmd_chunk.raw_data)
         return do_restore(chunked_iterator())
     return do_distribution_switch_return(db_backup.distribution_strategy, 
            shared=do_shared_restore,
            sharded=do_sharded_restore)

  @WithLockStream
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
