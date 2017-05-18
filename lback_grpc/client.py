import grpc
import shutil
import os
from . import server_pb2
from . import server_pb2_grpc
from . import shared_pb2
from . import shared_pb2_grpc
from lback.operation_backup import OperationBackup
from lback.operation_restore import OperationRestore
from lback.operation_mv import OperationMv
from lback.operation_relocate import OperationRelocate
from lback.operation_rm import OperationRm
from lback.restore import Restore, RestoreException
from lback.utils import lback_settings, lback_output, lback_id_temp, lback_backup_path

class Client( object ):
    def __init__(self):
        settings = lback_settings()
        channel = grpc.insecure_channel(settings['server']['host']+":"+settings['server']['port'])
        self.server =  server_pb2_grpc.ServerStub( channel )
    def _run_backup( self, operation_instance, backup ):
        lback_output("Routing BACKUP")
        lback_output("Creating TEMP backup snapshot")
        temp_backup_id = lback_id_temp( backup.id )
        real_backup_path = lback_backup_path( backup.id )
        temp_backup_path = lback_backup_path( temp_backup_id )
        shutil.move( real_backup_path, temp_backup_path )
        msg = shared_pb2.BackupCmd(
           id=backup.id,
           temp_id=temp_backup_id )
        replies = self.server.RouteBackup( msg )
        for reply in replies:
           if not reply.errored:
                lback_output("BACKUP propagated")
           else:
                lback_output("BACKUP could not be propagated")
        lback_output("Removing TEMP backup")
        os.remove( temp_backup_path )
    def _run_restore( self, operation_instance, backup ):
        lback_output("Routing RESTORE")
        cmd = shared_pb2.RestoreCmd( id=backup.id )
        if operation_instance.args.folder:
            cmd = shared_pb2.RestoreCmd( id=backup.id, use_temp_folder=True, folder=operation_instance.args.folder ) 
        reply = self.server.RouteRestore( 
            cmd )
        if not reply.errored:
            lback_output("RESTORE successful")
        else:
            lback_output("RESTORE could not be performed")
    def _run_relocate( self, operation_instance ):
        lback_output("Routing RELOCATE")
        reply = self.server.RouteRelocate( 
        shared_pb2.RelocateCmd( 
                id=id,
                src=operation_instance.args.src,
                dst=operation_instance.args.dst ) )
        if not reply.errored:
           lback_output("RELOCATE successful")
        else:
           lback_output("RELOCATE could not be performed")
    def _run_remove( self, operation_instance, backup ):
        lback_output("Routing REMOVE")
        if operation_instance.args.all:
             replies = self.server.RouteRm( 
                 shared_pb2.RmCmd( 
                    id=backup.id,
                    all=operation_instance.args.all))
        else:
             target = operation_instance.args.target
             replies = self.server.RouteRm( 
                 shared_pb2.RmCmd( 
                    id=backup.id,
                     target=target))
             for reply in replies:
                if not reply.errored:
                    lback_output("REMOVE propagated")
                else:
                    lback_output("REMOVE could not be propagated")
    def _run( self, operation_instance, backup ):
        if isinstance(operation_instance, OperationBackup ):
            self._run_backup( operation_instance, backup )
        elif isinstance(operation_instance, OperationRestore ):
            self._run_restore( operation_instance, backup )
        elif isinstance(operation_instance, OperationRelocate ):
            self._run_relocate( operation_instance, backup )
        elif isinstance(operation_instance, OperationRm ):
            self._run_remove( operation_instance, backup )
