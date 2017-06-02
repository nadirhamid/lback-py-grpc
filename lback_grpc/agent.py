from lback.backup import Backup
from lback.utils import lback_backup, lback_backup_chunked_file, lback_backup_remove, lback_output, lback_backup_path, lback_id
from lback.restore import Restore
from . import agent_pb2
from . import agent_pb2_grpc
from . import shared_pb2
from . import shared_pb2_grpc
from itertools import tee
from traceback import print_exc
import os

class Agent(agent_pb2_grpc.AgentServicer):
  def DoBackup(self, request_iterator, context):    
    lback_output("Received COMMAND DoBackup")
    request_iterator, iter_copy= tee( request_iterator )
    request = next(iter_copy)
    full_id = lback_id(request.id, shard=request.shard)
    backup_object = lback_backup(request.id)
    lback_output("Running backup on %s"%( request.id ))
    lback_output("Running backup on shard %s"%( request.shard ))
    backup = Backup( full_id, backup_object.folder )
    def backup_chunked_iterator():
        for backup_cmd_chunk in request_iterator:
         yield backup_cmd_chunk.raw_data
    try:
        backup.write_chunked( backup_chunked_iterator() )
    except Exception,ex:
        print_exc(ex)
        return shared_pb2.BackupCmdStatus( errored=True )

    lback_output("BACKUP COMPLETE")
    return shared_pb2.BackupCmdStatus( errored=False )

  def DoRelocateTake(self, request, context):
    lback_output("Received COMMAND DoRelocateTake")
    try:
        iterator = lback_backup_file_chunks( request.id )
        for file_chunk_res in iterator:
            lback_output("PACKING RELOCATE BACKUP CHUNK")
            yield shared_pb2.RelocateCmdGiveStatus( raw_data=file_chunk_res, errored=False)
    except Exception,ex:
        yield shared_pb2.RelocateCmdGiveStatus( errored=True )
  def DoRelocateGive(self, request_iterator, context):
    lback_output("Received COMMAND DoRelocateGive")
    request_iterator, iter_copy = tee( request_iterator )
    request = next(iter_copy)
    db_backup =lback_backup( request.id )
    backup = Backup( request.id, db_backup.folder )
    def relocate_cmd_chunked_iterator():
        for relocate_cmd_chunk in request_iterator:
            lback_output("SAVING RELOCATE BACKUP GIVE CHUNK")
            yield relocate_cmd_chunk.raw_data
    try:
        iterator = backup.run_chunked( relocate_chunked_iterator )
        for relocate_chunk_res in iterator:
            yield shared_pb2.RelocateCmdStatus(errored=False)
    except Exception,ex:
        print_exc(ex)
        yield shared_pb2.RelocateCmdStatus(errored=True )

  def DoRestore(self, request, context):
    lback_output("Received COMMAND DoRestore")
    db_backup =lback_backup( request.id )
     
    try:
        iterator = lback_backup_chunked_file(lback_id(id=db_backup.id, shard=request.shard))
        for restore_file_chunk in iterator:
            lback_output("PACKING RESTORE CHUNK")
            yield shared_pb2.RestoreCmdStatus( 
                errored=False,
               raw_data=restore_file_chunk )
    except Exception,ex:
        print_exc(ex)
        yield shared_pb2.RestoreCmdStatus( errored=True )

  def DoRm(self, request, context):
    lback_output("Received COMMAND DoRm")
    try:
       lback_backup_remove( request.id )
    except Exception,ex:
       print_exc(ex)
       return shared_pb2.RmCmdStatus( errored=True )
    lback_output("REMOVE COMPLETE")
    return shared_pb2.RmCmdStatus( errored=False )
  def DoCheckBackupExists(self, request, context):
     lback_output("Received COMMAND DoCheckBackupExists")
     lback_output("ID %s, SHARD %s"%( request.id, request.shard, ) )
     if  os.path.exists( lback_backup_path( request.id, request.shard ) ):
       return shared_pb2.CheckCmdStatus(
          errored=False)
     lback_output("BACKUP DOES NOT EXIST")
     return shared_pb2.CheckCmdStatus(
        errored=True)
