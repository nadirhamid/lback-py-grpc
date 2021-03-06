from lback.backup import Backup
from lback.utils import lback_backup, lback_backup_chunked_file, lback_backup_remove, lback_output, lback_backup_path, lback_id, lback_temp_file, lback_backup_shard_size, lback_backup_shard_start_end, lback_temp_path
from lback.restore import Restore
from . import agent_pb2
from . import agent_pb2_grpc
from . import shared_pb2
from . import shared_pb2_grpc
from . import protobuf_empty_to_none
from itertools import tee
from traceback import print_exc
import shutil
import os

class Agent(agent_pb2_grpc.AgentServicer):
  def DoBackup(self, request_iterator, context):    
    lback_output("Received COMMAND DoBackup")
    request_iterator, iter_copy= tee( request_iterator )
    request = next(iter_copy)
    full_id = lback_id(request.id, shard=protobuf_empty_to_none(request.shard))
    lback_output("Running backup on %s"%( request.id ))
    lback_output("Running backup on shard %s"%( request.shard ))
    backup = Backup( full_id, request.folder )
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

  def DoBackupAcceptFull(self, request, context):
    lback_output("Received COMMAND DoBackupAcceptFull")
    lback_output("ID %s"%( request.id ) )
    folder = request.folder
    id = request.id
    bkp = Backup(id, folder, diff=False, encryption_key=request.encryption_key, compression=request.compression)

    try:
        lback_output("RUNNING FULL BACKUP AT %s" % ( bkp.get_file() ))
        bkp.run()
        if request.remove:
          shutil.rmtree(folder)
          lback_output("Directory successfully deleted..")
    except Exception,ex:
        print_exc(ex)
        return shared_pb2.BackupCmdAcceptStatus(
            errored=True)
    backup_size = os.stat( bkp.get_file() ).st_size
    return shared_pb2.BackupCmdAcceptStatus(
            backup_size=backup_size,
            errored=False)


  def DoBackupAcceptDiff(self, request_iterator, context):
    lback_output("Received COMMAND DoBackupAcceptDiff")
    request_iterator, iter_copy = tee( request_iterator )
    request = next(iter_copy)
    id = request.id
    folder = request.folder
    lback_output("ID %s"%( request.id ) )

    bkp = Backup(id, folder, diff=True, encryption_key=request.encryption_key, compression=request.compression)
    def chunked_restore_iterator():
        for res in request_iterator:
            yield res.raw_data
    try:
        restore_path = lback_temp_path()
        os.makedirs( restore_path )
        lback_output("Running DIFF RESTORE")
        restore = Restore(id, folder=restore_path)
        restore.run_chunked(chunked_restore_iterator()) 
        lback_output("Running DIFF BACKUP")
        bkp.run_diff(restore_path)  
        os.remove( restore_path )
    except Exception,ex:
        return shared_pb2.BackupCmdAcceptStatus(
            errored=True)
    backup_size = os.stat( bkp.get_file() ).st_size
    return shared_pb2.BackupCmdAcceptStatus(
            backup_size=backup_size,
            errored=False)
     
  def DoRelocateTake(self, request, context):
    lback_output("Received COMMAND DoRelocateTake")
    lback_output("ID %s, SHARD %s"%( request.id, request.shard, ) )
    shard = protobuf_empty_to_none(request.shard)
    shard_iterator = protobuf_empty_to_none(request.shard_iterator)
    lback_output("SHARD ITERATOR: %s"%( shard_iterator ) )
    full_id = lback_id(request.id, shard=shard)
    lback_output("FULL ID %s"%( full_id ) )
    backup_full_path = lback_backup_path( full_id )
    shard_size = None

    try:
        if request.delete:
            temp_file = lback_temp_file()
            shutil.move( lback_backup_path( full_id ), temp_file.name )
            backup_full_path = temp_file.name
        backup_size = os.stat( backup_full_path ).st_size
        if not shard_iterator is None:
            shard_size = lback_backup_shard_size( backup_size, int( request.total_shards ) )
            shard_start, shard_end = lback_backup_shard_start_end( int( shard_iterator ), shard_size )
            iterator = lback_backup_chunked_file( backup_full_path, chunk_start=shard_start, chunk_end=shard_end, use_backup_path=False)
        else:
            iterator = lback_backup_chunked_file( backup_full_path, use_backup_path=False )
        for file_chunk_res in iterator:
            lback_output("PACKING RELOCATE BACKUP CHUNK")
            yield shared_pb2.RelocateCmdTakeStatus( 
                raw_data=file_chunk_res, 
                errored=False)
    except Exception,ex:
        print_exc(ex)
        yield shared_pb2.RelocateCmdTakeStatus( errored=True )
  def DoRelocateGive(self, request_iterator, context):
    lback_output("Received COMMAND DoRelocateGive")
    lback_output("ID %s, SHARD %s"%( request.id, request.shard, ) )
    request_iterator, iter_copy = tee( request_iterator )
    request = next(iter_copy)
    full_id = lback_id(request.id, shard=protobuf_empty_to_none(request.shard))
    backup = Backup( full_id, request.folder )
    def relocate_cmd_chunked_iterator():
        for relocate_cmd_chunk in request_iterator:
            lback_output("SAVING RELOCATE BACKUP GIVE CHUNK")
            yield relocate_cmd_chunk.raw_data
    try:
        backup.write_chunked( relocate_cmd_chunked_iterator() )
    except Exception,ex:
        print_exc(ex)
        return shared_pb2.RelocateCmdGiveStatus(errored=True )
    return shared_pb2.RelocateCmdGiveStatus(errored=False)

  def DoRestore(self, request, context):
    lback_output("Received COMMAND DoRestore")
    try:
        iterator = lback_backup_chunked_file(lback_id(id=request.id, shard=protobuf_empty_to_none(request.shard)))
        for restore_file_chunk in iterator:
            lback_output("PACKING RESTORE CHUNK")
            yield shared_pb2.RestoreCmdStatus( 
                errored=False,
               raw_data=restore_file_chunk )
    except Exception,ex:
        print_exc(ex)
        yield shared_pb2.RestoreCmdStatus( errored=True )

  def DoRestoreAccept(self, request_iterator, context):
    lback_output("Received COMMAND DoRestoreAccept")
    request_iterator, iter_copy= tee( request_iterator )
    request = next(iter_copy)
    def chunked_iterator():
        for chunk in request_iterator:
            lback_output("STORING RESTORE CHUNK")
            yield chunk.raw_data
    try:
       restore =Restore( request.id, folder=request.folder )
       restore.run_chunked(chunked_iterator())
       lback_output("RESTORE SUCCESSFULL")
    except Exception,ex:
       print_exc(ex)
       return shared_pb2.RestoreAcceptCmdStatus(
            errored=True)
    return shared_pb2.RestoreAcceptCmdStatus(
            errored=False)



  def DoRm(self, request, context):
    lback_output("Received COMMAND DoRm")
    try:
       lback_backup_remove( request.id, shard=protobuf_empty_to_none(request.shard) )
    except Exception,ex:
       print_exc(ex)
       return shared_pb2.RmCmdStatus( errored=True )
    lback_output("REMOVE COMPLETE")
    return shared_pb2.RmCmdStatus( errored=False )

  def DoCheckBackupExists(self, request, context):
     lback_output("Received COMMAND DoCheckBackupExists")
     lback_output("ID %s, SHARD %s"%( request.id, request.shard, ) )
     if  os.path.exists( lback_backup_path( request.id, shard=protobuf_empty_to_none(request.shard) ) ):
       return shared_pb2.CheckCmdStatus(
          errored=False)
     lback_output("BACKUP DOES NOT EXIST")
     return shared_pb2.CheckCmdStatus(
        errored=True)
