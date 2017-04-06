import grpc
import server_pb2
import server_pb2_grpc
from lback.utils 
from lback.operation_backup import OperationBackup
from lback.operation_restore import OperationRestore
from lback.operation_mv import OperationMv
from lback.operation_rm import OperationRm
from lback.restore import Restore, RestoreException

class Client( object ):
	def __init__(self):
		self.channel = grpc.InsecureChannel("localhost:4500")
		self.server =  server_pb2_grpc.ServerStub()
	def _run( self, operation_instance ):
	    id = operation_instance.get_id()
	    if isinstance(operation_instance, OperationBackup ):
	        def read_in_chunks(chunk_size=1024):
		    while True:
			chunk = backup.read( chunk_size )
		 	if not chunk:
			    break
			yield chunk
		backup = lback_backup_file( id )
		replies = self.server.RouteBackup( read_in_chunks() )
		for reply in replies:
		   if not reply.errored:
		      lback_output("CHUNK delivered")
		   else:
		      lback_output("CHUNK undelivered")
	    elif isinstance(operation_instance, OperationRestore ):
		replies = self.server.RouteRestore( 
			server_pb2.RestoreCmd( id=id ) )
		for reply in replies:
		   if not reply.errored:
		      lback_output("CHUNK delivered")
		   else:
		      lback_output("CHUNK undelivered")
		   if reply.final:
		       pass
	    elif isinstance(operation_instance, OperationMv ):
		 reply = self.server.RouteMv( 
			 server_pb2.MvCmd( 
				id=id,
				src=operation_instance.get_arg("src"),
				dst=operation_instance.get_arg("dst") ) )
		 if not not reply.errored:
		    lback_output("Moved compartment")
		 else:
		    lback_output("Unable to MOVE compartment")
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
		    lback_output("Removed compartment")
		 else:
		    lback_output("Unable to REMOVE compartment")
		
