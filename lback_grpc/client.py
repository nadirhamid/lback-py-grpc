import grpc
import shutil
import os
from . import server_pb2
from . import server_pb2_grpc
from . import shared_pb2
from . import shared_pb2_grpc
from . import server_connection
from lback.operation_backup import OperationBackup
from lback.operation_restore import OperationRestore
from lback.operation_mv import OperationMv
from lback.operation_relocate import OperationRelocate
from lback.operation_rm import OperationRm
from lback.restore import Restore, RestoreException
from lback.utils import lback_settings, lback_output, lback_id_temp, lback_backup_path, lback_make_temp_backup, lback_backup_remove,  lback_backup_move

class Client( object ):
    def __init__(self):
        self.server = server_connection()
    def _run_backup( self, operation_instance, backup ):
        msg = shared_pb2.BackupCmd(
           id=backup.id,
           target=operation_instance.args.target,
           folder=operation_instance.args.folder,
           encryption_key=operation_instance.args.encryption_key,
           diff=operation_instance.args.diff,
           distribution_strategy=operation_instance.args.distribution_strategy )
        replies = self.server.RouteBackup( msg )
        for reply in replies:
           if not reply.errored:
                lback_output("BACKUP propagated")
           else:
                lback_output("BACKUP could not be propagated")
    def _run_restore( self, operation_instance, backup ):
        lback_output("Routing RESTORE")
        cmd = shared_pb2.RestoreCmd( 
            id=backup.id, 
            target=operation_instance.args.target )
        if operation_instance.args.folder:
            cmd = shared_pb2.RestoreCmd( 
                id=backup.id, 
                use_temp_folder=True, 
                folder=operation_instance.args.folder,
                target=operation_instance.args.target ) 
        reply = self.server.RouteRestore( 
            cmd )
        if not reply.errored:
            lback_output("RESTORE successful")
        else:
            lback_output("RESTORE could not be performed")
        return reply
    def _run_relocate( self, operation_instance, backup ):
        lback_output("Routing RELOCATE")
        reply = self.server.RouteRelocate( 
        shared_pb2.RelocateCmd( 
                id=backup.id,
                src=operation_instance.args.src,
                dst=operation_instance.args.dst ) )
        if not reply.errored:
           lback_output("RELOCATE successful")
        else:
           lback_output("RELOCATE could not be performed")
        return reply
    def _run_remove( self, operation_instance, backup ):
        lback_output("Routing REMOVE")

        def handle_replies( replies ):
            for reply in replies:
                if not reply.errored:
                    lback_output("REMOVE propagated")
                else:
                    lback_output("REMOVE could not be propagated")
        if operation_instance.args.all:
             replies = self.server.RouteRm( 
                 shared_pb2.RmCmd( 
                    id=backup.id,
                    all=operation_instance.args.all))
             handle_replies(replies)
                
        else:
             target = operation_instance.args.target
             replies = self.server.RouteRm( 
                 shared_pb2.RmCmd( 
                    id=backup.id,
                     target=target))
             handle_replies( replies )
    def _run( self, operation_instance, backup ):
        resp= None
        if isinstance(operation_instance, OperationBackup ):
            resp = self._run_backup( operation_instance, backup )
        elif isinstance(operation_instance, OperationRestore ):
            resp = self._run_restore( operation_instance, backup )
        elif isinstance(operation_instance, OperationRelocate ):
            resp = self._run_relocate( operation_instance, backup )
        elif isinstance(operation_instance, OperationRm ):
            resp = self._run_remove( operation_instance, backup )
        return resp
