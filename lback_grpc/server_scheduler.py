
import shutil
from . import shared_pb2
from . import make_connection_string
from . import server_connection
from lback.utils import lback_agent_is_available, lback_make_temp_backup, lback_backup_remove, lback_backup_move, lback_backup_path, lback_output

class ServerScheduler(object):
    ## find agents without
    ## this backup and schedule
    def ScheduleSharedBackup(self, backup_obj):
        if self.locked:
            return
        server = server_connection()
        def filter_fn( agent ):
            if not lback_agent_is_available( agent[0] ):
                return False
            check_cmd = shared_pb2.CheckCmd(id=backup_obj.id, shard=None)
            lback_output("CHECKING IF AGENT {} NEEDS BACKUP {}".format(
                make_connection_string(agent[0]),
                backup_obj.id ))
            cmd_result = agent[1].DoCheckBackupExists(check_cmd)
            return cmd_result.errored
        def map_fn( agent ):
            return agent[0].id
        needs_scheduling = map(map_fn, filter(filter_fn, self.agents))
        if not len( needs_scheduling ) > 0:
           return

        reply = server.RouteRestore(shared_pb2.RestoreCmd(
            id=backup_obj.id,
            skip_run=True))
        if reply.errored:
            lback_output("COULD NOT DO SCHEDULED BACKUP PROPAGATION")
            lback_output("EITHER NO AGENTS HAVE THIS BACKUP OR AN ERROR OCCURED")
            return

        lback_output("LOCAL SCHEDULED RESTORE COMPLETE")
        lback_output("MOVING SCHEDULED PARTITION")
        lback_backup_move(
            lback_backup_path(backup_obj.id, suffix="R"),
            lback_backup_path(backup_obj.id)
        )
        lback_output("ROUTING BACKUP TO AGENTS NEEDING SCHEDULING")
        lback_output(needs_scheduling)
        temp_backup_id = lback_make_temp_backup( backup_obj )
        server.RouteBackup(shared_pb2.BackupCmd(
            id=backup_obj.id,
           temp_id=temp_backup_id,
           agent_ids=needs_scheduling
        ))
        lback_output("SCHEDULED BACKUP COMPLETE")
