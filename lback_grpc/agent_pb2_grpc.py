# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc
from grpc.framework.common import cardinality
from grpc.framework.interfaces.face import utilities as face_utilities

import shared_pb2 as shared__pb2


class AgentStub(object):
  """Interface exported by the server.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.DoBackup = channel.stream_unary(
        '/lbackgrpc.Agent/DoBackup',
        request_serializer=shared__pb2.BackupCmdStream.SerializeToString,
        response_deserializer=shared__pb2.BackupCmdStatus.FromString,
        )
    self.DoBackupAcceptFull = channel.unary_unary(
        '/lbackgrpc.Agent/DoBackupAcceptFull',
        request_serializer=shared__pb2.BackupCmdAcceptFull.SerializeToString,
        response_deserializer=shared__pb2.BackupCmdAcceptStatus.FromString,
        )
    self.DoBackupAcceptDiff = channel.stream_unary(
        '/lbackgrpc.Agent/DoBackupAcceptDiff',
        request_serializer=shared__pb2.BackupCmdAcceptDiff.SerializeToString,
        response_deserializer=shared__pb2.BackupCmdAcceptStatus.FromString,
        )
    self.DoShardedBackup = channel.stream_unary(
        '/lbackgrpc.Agent/DoShardedBackup',
        request_serializer=shared__pb2.BackupCmdStream.SerializeToString,
        response_deserializer=shared__pb2.BackupCmdStatus.FromString,
        )
    self.DoRelocateTake = channel.unary_stream(
        '/lbackgrpc.Agent/DoRelocateTake',
        request_serializer=shared__pb2.RelocateCmdTake.SerializeToString,
        response_deserializer=shared__pb2.RelocateCmdTakeStatus.FromString,
        )
    self.DoRelocateGive = channel.stream_unary(
        '/lbackgrpc.Agent/DoRelocateGive',
        request_serializer=shared__pb2.RelocateCmdGiveStream.SerializeToString,
        response_deserializer=shared__pb2.RelocateCmdGiveStatus.FromString,
        )
    self.DoRestore = channel.unary_stream(
        '/lbackgrpc.Agent/DoRestore',
        request_serializer=shared__pb2.RestoreCmd.SerializeToString,
        response_deserializer=shared__pb2.RestoreCmdStatus.FromString,
        )
    self.DoRestoreAccept = channel.stream_unary(
        '/lbackgrpc.Agent/DoRestoreAccept',
        request_serializer=shared__pb2.RestoreAcceptCmd.SerializeToString,
        response_deserializer=shared__pb2.RestoreAcceptCmdStatus.FromString,
        )
    self.DoRm = channel.unary_unary(
        '/lbackgrpc.Agent/DoRm',
        request_serializer=shared__pb2.RmCmd.SerializeToString,
        response_deserializer=shared__pb2.RmCmdStatus.FromString,
        )
    self.DoCheckBackupExists = channel.unary_unary(
        '/lbackgrpc.Agent/DoCheckBackupExists',
        request_serializer=shared__pb2.CheckCmd.SerializeToString,
        response_deserializer=shared__pb2.CheckCmdStatus.FromString,
        )


class AgentServicer(object):
  """Interface exported by the server.
  """

  def DoBackup(self, request_iterator, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def DoBackupAcceptFull(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def DoBackupAcceptDiff(self, request_iterator, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def DoShardedBackup(self, request_iterator, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def DoRelocateTake(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def DoRelocateGive(self, request_iterator, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def DoRestore(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def DoRestoreAccept(self, request_iterator, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def DoRm(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def DoCheckBackupExists(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_AgentServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'DoBackup': grpc.stream_unary_rpc_method_handler(
          servicer.DoBackup,
          request_deserializer=shared__pb2.BackupCmdStream.FromString,
          response_serializer=shared__pb2.BackupCmdStatus.SerializeToString,
      ),
      'DoBackupAcceptFull': grpc.unary_unary_rpc_method_handler(
          servicer.DoBackupAcceptFull,
          request_deserializer=shared__pb2.BackupCmdAcceptFull.FromString,
          response_serializer=shared__pb2.BackupCmdAcceptStatus.SerializeToString,
      ),
      'DoBackupAcceptDiff': grpc.stream_unary_rpc_method_handler(
          servicer.DoBackupAcceptDiff,
          request_deserializer=shared__pb2.BackupCmdAcceptDiff.FromString,
          response_serializer=shared__pb2.BackupCmdAcceptStatus.SerializeToString,
      ),
      'DoShardedBackup': grpc.stream_unary_rpc_method_handler(
          servicer.DoShardedBackup,
          request_deserializer=shared__pb2.BackupCmdStream.FromString,
          response_serializer=shared__pb2.BackupCmdStatus.SerializeToString,
      ),
      'DoRelocateTake': grpc.unary_stream_rpc_method_handler(
          servicer.DoRelocateTake,
          request_deserializer=shared__pb2.RelocateCmdTake.FromString,
          response_serializer=shared__pb2.RelocateCmdTakeStatus.SerializeToString,
      ),
      'DoRelocateGive': grpc.stream_unary_rpc_method_handler(
          servicer.DoRelocateGive,
          request_deserializer=shared__pb2.RelocateCmdGiveStream.FromString,
          response_serializer=shared__pb2.RelocateCmdGiveStatus.SerializeToString,
      ),
      'DoRestore': grpc.unary_stream_rpc_method_handler(
          servicer.DoRestore,
          request_deserializer=shared__pb2.RestoreCmd.FromString,
          response_serializer=shared__pb2.RestoreCmdStatus.SerializeToString,
      ),
      'DoRestoreAccept': grpc.stream_unary_rpc_method_handler(
          servicer.DoRestoreAccept,
          request_deserializer=shared__pb2.RestoreAcceptCmd.FromString,
          response_serializer=shared__pb2.RestoreAcceptCmdStatus.SerializeToString,
      ),
      'DoRm': grpc.unary_unary_rpc_method_handler(
          servicer.DoRm,
          request_deserializer=shared__pb2.RmCmd.FromString,
          response_serializer=shared__pb2.RmCmdStatus.SerializeToString,
      ),
      'DoCheckBackupExists': grpc.unary_unary_rpc_method_handler(
          servicer.DoCheckBackupExists,
          request_deserializer=shared__pb2.CheckCmd.FromString,
          response_serializer=shared__pb2.CheckCmdStatus.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'lbackgrpc.Agent', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
