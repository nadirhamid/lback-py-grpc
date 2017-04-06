import grpc
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
from lback.utils import lback_settings, lback_output

class Client( object ):
	def __init__(self):
		settings = lback_settings()
		channel = grpc.insecure_channel(settings['server']['host']+":"+settings['server']['port'])
		self.server =  server_pb2_grpc.ServerStub( channel )
	def _run( self, operation_instance, backup=None):
	    if isinstance(operation_instance, OperationBackup ):
	  	lback_output("Routing BACKUP")
	  	msg = shared_pb2.BackupCmd(
			id=backup.id )
		replies = self.server.RouteBackup( msg )
		for reply in replies:
		   if not reply.errored:
		      lback_output("BACKUP propagated")
		   else:
		      lback_output("BACKUP could not be propagated")
	    elif isinstance(operation_instance, OperationRestore ):
	  	lback_output("Routing RESTORE")
		reply = self.server.RouteRestore( 
			shared_pb2.RestoreCmd( id=backup.id ) )
		if not reply.errored:
		    lback_output("RESTORE successful")
		else:
		    lback_output("RESTORE could not be performed")
	    elif isinstance(operation_instance, OperationRelocate ):
	  	 lback_output("Routing RELOCATE")
		 reply = self.server.RouteRelocate( 
			 shared_pb2.RelocateCmd( 
				id=id,
				src=operation_instance.args.src,
				dst=operation_instance.args.dst ) )
		 if not not reply.errored:
		    lback_output("RELOCATE successful")
		 else:
		    lback_output("RELOCATE could not be performed")
	    elif isinstance(operation_instance, OperationRm ):
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
		    if not not reply.errored:
		       lback_output("REMOVE propagated")
		    else:
		       lback_output("REMOVE could not be propagated")
