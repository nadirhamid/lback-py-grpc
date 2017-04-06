import grpc
import server_pb2
import server_pb2_grpc
from lback.utils 
from lback.operation_backup import OperationBackup
from lback.operation_restore import OperationRestore
from lback.operation_mv import OperationMv
from lback.operation_relocate import OperationRelocate
from lback.operation_rm import OperationRm
from lback.restore import Restore, RestoreException

class Client( object ):
	def __init__(self):
		channel = grpc.InsecureChannel("localhost:4500")
		self.server =  server_pb2_grpc.ServerStub( channel )
	def _run( self, operation_instance ):
	    id = operation_instance.get_id()
	    if isinstance(operation_instance, OperationBackup ):
		backup = lback_backup_file( id )
		replies = self.server.RouteBackup( server_pb2.BackupCmd(
			 id=id ))
		for reply in replies:
		   if not reply.errored:
		      lback_output("BACKUP propagated")
		   else:
		      lback_output("BACKUP could not be propagated")
	    elif isinstance(operation_instance, OperationRestore ):
		reply = self.server.RouteRestore( 
			server_pb2.RestoreCmd( id=id ) )
		if not reply.errored:
		    lback_output("RESTORE successful")
		else:
		    lback_output("RESTORE could not be performed")
	    elif isinstance(operation_instance, OperationRelocate ):
		 reply = self.server.RouteRelocate( 
			 server_pb2.RelocateCmd( 
				id=id,
				src=operation_instance.get_arg("src"),
				dst=operation_instance.get_arg("dst") ) )
		 if not not reply.errored:
		    lback_output("RELOCATE successful")
		 else:
		    lback_output("RELOCATE could not be performed")
	    elif isinstance(operation_instance, OperationRm ):
		 is_all = operation_instance.get_arg("all")
		 if is_all:
			 reply = self.server.RouteRm( 
				 server_pb2.RmCmd( 
					id=id,
					all=is_all))
		 else:
			target = operation_instance.get_arg("target")
		 	reply = self.server.RouteRm( 
				 server_pb2.RmCmd( 
					id=id,
				 	target=target))
		 if not not reply.errored:
		    lback_output("REMOVE propagated")
		 else:
		    lback_output("REMOVE could not be propagated")
