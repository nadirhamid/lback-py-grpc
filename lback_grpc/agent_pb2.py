# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: agent.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import shared_pb2 as shared__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='agent.proto',
  package='lbackgrpc',
  syntax='proto3',
  serialized_pb=_b('\n\x0b\x61gent.proto\x12\tlbackgrpc\x1a\x0cshared.proto2\xdf\x04\n\x05\x41gent\x12\x46\n\x08\x44oBackup\x12\x1a.lbackgrpc.BackupCmdStream\x1a\x1a.lbackgrpc.BackupCmdStatus\"\x00(\x01\x12M\n\x0f\x44oShardedBackup\x12\x1a.lbackgrpc.BackupCmdStream\x1a\x1a.lbackgrpc.BackupCmdStatus\"\x00(\x01\x12R\n\x0e\x44oRelocateTake\x12\x1a.lbackgrpc.RelocateCmdTake\x1a .lbackgrpc.RelocateCmdTakeStatus\"\x00\x30\x01\x12X\n\x0e\x44oRelocateGive\x12 .lbackgrpc.RelocateCmdGiveStream\x1a .lbackgrpc.RelocateCmdGiveStatus\"\x00(\x01\x12\x43\n\tDoRestore\x12\x15.lbackgrpc.RestoreCmd\x1a\x1b.lbackgrpc.RestoreCmdStatus\"\x00\x30\x01\x12O\n\x0f\x44oRestoreAccept\x12\x1b.lbackgrpc.RestoreAcceptCmd\x1a\x1b.lbackgrpc.RestoreCmdStatus\"\x00(\x01\x12\x32\n\x04\x44oRm\x12\x10.lbackgrpc.RmCmd\x1a\x16.lbackgrpc.RmCmdStatus\"\x00\x12G\n\x13\x44oCheckBackupExists\x12\x13.lbackgrpc.CheckCmd\x1a\x19.lbackgrpc.CheckCmdStatus\"\x00\x42\x1d\n\x12io.grpc.lback.grpcB\x05\x41gentP\x01\x62\x06proto3')
  ,
  dependencies=[shared__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)





DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\022io.grpc.lback.grpcB\005AgentP\001'))
try:
  # THESE ELEMENTS WILL BE DEPRECATED.
  # Please use the generated *_pb2_grpc.py files instead.
  import grpc
  from grpc.framework.common import cardinality
  from grpc.framework.interfaces.face import utilities as face_utilities
  from grpc.beta import implementations as beta_implementations
  from grpc.beta import interfaces as beta_interfaces


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
          response_deserializer=shared__pb2.RestoreCmdStatus.FromString,
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
            response_serializer=shared__pb2.RestoreCmdStatus.SerializeToString,
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


  class BetaAgentServicer(object):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This class was generated
    only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0."""
    """Interface exported by the server.
    """
    def DoBackup(self, request_iterator, context):
      context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)
    def DoShardedBackup(self, request_iterator, context):
      context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)
    def DoRelocateTake(self, request, context):
      context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)
    def DoRelocateGive(self, request_iterator, context):
      context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)
    def DoRestore(self, request, context):
      context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)
    def DoRestoreAccept(self, request_iterator, context):
      context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)
    def DoRm(self, request, context):
      context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)
    def DoCheckBackupExists(self, request, context):
      context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)


  class BetaAgentStub(object):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This class was generated
    only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0."""
    """Interface exported by the server.
    """
    def DoBackup(self, request_iterator, timeout, metadata=None, with_call=False, protocol_options=None):
      raise NotImplementedError()
    DoBackup.future = None
    def DoShardedBackup(self, request_iterator, timeout, metadata=None, with_call=False, protocol_options=None):
      raise NotImplementedError()
    DoShardedBackup.future = None
    def DoRelocateTake(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
      raise NotImplementedError()
    def DoRelocateGive(self, request_iterator, timeout, metadata=None, with_call=False, protocol_options=None):
      raise NotImplementedError()
    DoRelocateGive.future = None
    def DoRestore(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
      raise NotImplementedError()
    def DoRestoreAccept(self, request_iterator, timeout, metadata=None, with_call=False, protocol_options=None):
      raise NotImplementedError()
    DoRestoreAccept.future = None
    def DoRm(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
      raise NotImplementedError()
    DoRm.future = None
    def DoCheckBackupExists(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
      raise NotImplementedError()
    DoCheckBackupExists.future = None


  def beta_create_Agent_server(servicer, pool=None, pool_size=None, default_timeout=None, maximum_timeout=None):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This function was
    generated only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0"""
    request_deserializers = {
      ('lbackgrpc.Agent', 'DoBackup'): shared__pb2.BackupCmdStream.FromString,
      ('lbackgrpc.Agent', 'DoCheckBackupExists'): shared__pb2.CheckCmd.FromString,
      ('lbackgrpc.Agent', 'DoRelocateGive'): shared__pb2.RelocateCmdGiveStream.FromString,
      ('lbackgrpc.Agent', 'DoRelocateTake'): shared__pb2.RelocateCmdTake.FromString,
      ('lbackgrpc.Agent', 'DoRestore'): shared__pb2.RestoreCmd.FromString,
      ('lbackgrpc.Agent', 'DoRestoreAccept'): shared__pb2.RestoreAcceptCmd.FromString,
      ('lbackgrpc.Agent', 'DoRm'): shared__pb2.RmCmd.FromString,
      ('lbackgrpc.Agent', 'DoShardedBackup'): shared__pb2.BackupCmdStream.FromString,
    }
    response_serializers = {
      ('lbackgrpc.Agent', 'DoBackup'): shared__pb2.BackupCmdStatus.SerializeToString,
      ('lbackgrpc.Agent', 'DoCheckBackupExists'): shared__pb2.CheckCmdStatus.SerializeToString,
      ('lbackgrpc.Agent', 'DoRelocateGive'): shared__pb2.RelocateCmdGiveStatus.SerializeToString,
      ('lbackgrpc.Agent', 'DoRelocateTake'): shared__pb2.RelocateCmdTakeStatus.SerializeToString,
      ('lbackgrpc.Agent', 'DoRestore'): shared__pb2.RestoreCmdStatus.SerializeToString,
      ('lbackgrpc.Agent', 'DoRestoreAccept'): shared__pb2.RestoreCmdStatus.SerializeToString,
      ('lbackgrpc.Agent', 'DoRm'): shared__pb2.RmCmdStatus.SerializeToString,
      ('lbackgrpc.Agent', 'DoShardedBackup'): shared__pb2.BackupCmdStatus.SerializeToString,
    }
    method_implementations = {
      ('lbackgrpc.Agent', 'DoBackup'): face_utilities.stream_unary_inline(servicer.DoBackup),
      ('lbackgrpc.Agent', 'DoCheckBackupExists'): face_utilities.unary_unary_inline(servicer.DoCheckBackupExists),
      ('lbackgrpc.Agent', 'DoRelocateGive'): face_utilities.stream_unary_inline(servicer.DoRelocateGive),
      ('lbackgrpc.Agent', 'DoRelocateTake'): face_utilities.unary_stream_inline(servicer.DoRelocateTake),
      ('lbackgrpc.Agent', 'DoRestore'): face_utilities.unary_stream_inline(servicer.DoRestore),
      ('lbackgrpc.Agent', 'DoRestoreAccept'): face_utilities.stream_unary_inline(servicer.DoRestoreAccept),
      ('lbackgrpc.Agent', 'DoRm'): face_utilities.unary_unary_inline(servicer.DoRm),
      ('lbackgrpc.Agent', 'DoShardedBackup'): face_utilities.stream_unary_inline(servicer.DoShardedBackup),
    }
    server_options = beta_implementations.server_options(request_deserializers=request_deserializers, response_serializers=response_serializers, thread_pool=pool, thread_pool_size=pool_size, default_timeout=default_timeout, maximum_timeout=maximum_timeout)
    return beta_implementations.server(method_implementations, options=server_options)


  def beta_create_Agent_stub(channel, host=None, metadata_transformer=None, pool=None, pool_size=None):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This function was
    generated only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0"""
    request_serializers = {
      ('lbackgrpc.Agent', 'DoBackup'): shared__pb2.BackupCmdStream.SerializeToString,
      ('lbackgrpc.Agent', 'DoCheckBackupExists'): shared__pb2.CheckCmd.SerializeToString,
      ('lbackgrpc.Agent', 'DoRelocateGive'): shared__pb2.RelocateCmdGiveStream.SerializeToString,
      ('lbackgrpc.Agent', 'DoRelocateTake'): shared__pb2.RelocateCmdTake.SerializeToString,
      ('lbackgrpc.Agent', 'DoRestore'): shared__pb2.RestoreCmd.SerializeToString,
      ('lbackgrpc.Agent', 'DoRestoreAccept'): shared__pb2.RestoreAcceptCmd.SerializeToString,
      ('lbackgrpc.Agent', 'DoRm'): shared__pb2.RmCmd.SerializeToString,
      ('lbackgrpc.Agent', 'DoShardedBackup'): shared__pb2.BackupCmdStream.SerializeToString,
    }
    response_deserializers = {
      ('lbackgrpc.Agent', 'DoBackup'): shared__pb2.BackupCmdStatus.FromString,
      ('lbackgrpc.Agent', 'DoCheckBackupExists'): shared__pb2.CheckCmdStatus.FromString,
      ('lbackgrpc.Agent', 'DoRelocateGive'): shared__pb2.RelocateCmdGiveStatus.FromString,
      ('lbackgrpc.Agent', 'DoRelocateTake'): shared__pb2.RelocateCmdTakeStatus.FromString,
      ('lbackgrpc.Agent', 'DoRestore'): shared__pb2.RestoreCmdStatus.FromString,
      ('lbackgrpc.Agent', 'DoRestoreAccept'): shared__pb2.RestoreCmdStatus.FromString,
      ('lbackgrpc.Agent', 'DoRm'): shared__pb2.RmCmdStatus.FromString,
      ('lbackgrpc.Agent', 'DoShardedBackup'): shared__pb2.BackupCmdStatus.FromString,
    }
    cardinalities = {
      'DoBackup': cardinality.Cardinality.STREAM_UNARY,
      'DoCheckBackupExists': cardinality.Cardinality.UNARY_UNARY,
      'DoRelocateGive': cardinality.Cardinality.STREAM_UNARY,
      'DoRelocateTake': cardinality.Cardinality.UNARY_STREAM,
      'DoRestore': cardinality.Cardinality.UNARY_STREAM,
      'DoRestoreAccept': cardinality.Cardinality.STREAM_UNARY,
      'DoRm': cardinality.Cardinality.UNARY_UNARY,
      'DoShardedBackup': cardinality.Cardinality.STREAM_UNARY,
    }
    stub_options = beta_implementations.stub_options(host=host, metadata_transformer=metadata_transformer, request_serializers=request_serializers, response_deserializers=response_deserializers, thread_pool=pool, thread_pool_size=pool_size)
    return beta_implementations.dynamic_stub(channel, 'lbackgrpc.Agent', cardinalities, options=stub_options)
except ImportError:
  pass
# @@protoc_insertion_point(module_scope)
