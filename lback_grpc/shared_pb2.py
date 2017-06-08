# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: shared.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='shared.proto',
  package='lbackgrpc',
  syntax='proto3',
  serialized_pb=_b('\n\x0cshared.proto\x12\tlbackgrpc\">\n\x0f\x42\x61\x63kupCmdStream\x12\n\n\x02id\x18\x01 \x01(\t\x12\x10\n\x08raw_data\x18\x02 \x01(\x0c\x12\r\n\x05shard\x18\x03 \x01(\t\"(\n\tBackupCmd\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07temp_id\x18\x02 \x01(\t\"8\n\x0f\x42\x61\x63kupCmdStatus\x12\x14\n\x0c\x65lapsed_time\x18\x01 \x01(\x05\x12\x0f\n\x07\x65rrored\x18\x02 \x01(\x08\"P\n\nRestoreCmd\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0e\n\x06\x66older\x18\x02 \x01(\t\x12\x17\n\x0fuse_temp_folder\x18\x03 \x01(\x08\x12\r\n\x05shard\x18\x04 \x01(\t\"K\n\x10RestoreCmdStatus\x12\x14\n\x0c\x65lapsed_time\x18\x01 \x01(\x05\x12\x10\n\x08raw_data\x18\x02 \x01(\x0c\x12\x0f\n\x07\x65rrored\x18\x03 \x01(\x08\"3\n\x0bRelocateCmd\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0b\n\x03src\x18\x02 \x01(\t\x12\x0b\n\x03\x64st\x18\x03 \x01(\t\"\x1d\n\x0fRelocateCmdTake\x12\n\n\x02id\x18\x01 \x01(\t\"5\n\x15RelocateCmdGiveStream\x12\n\n\x02id\x18\x01 \x01(\t\x12\x10\n\x08raw_data\x18\x02 \x01(\x0c\")\n\x11RelocateCmdStatus\x12\x14\n\x0c\x65lapsed_time\x18\x01 \x01(\x05\">\n\x15RelocateCmdTakeStatus\x12\x14\n\x0c\x65lapsed_time\x18\x01 \x01(\x05\x12\x0f\n\x07\x65rrored\x18\x02 \x01(\x08\"(\n\x15RelocateCmdGiveStatus\x12\x0f\n\x07\x65rrored\x18\x01 \x01(\x08\"?\n\x05RmCmd\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0e\n\x06target\x18\x02 \x01(\t\x12\x0b\n\x03\x61ll\x18\x03 \x01(\x08\x12\r\n\x05shard\x18\x04 \x01(\t\"4\n\x0bRmCmdStatus\x12\x14\n\x0c\x65lapsed_time\x18\x01 \x01(\x05\x12\x0f\n\x07\x65rrored\x18\x02 \x01(\x08\"%\n\x08\x43heckCmd\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05shard\x18\x02 \x01(\t\"!\n\x0e\x43heckCmdStatus\x12\x0f\n\x07\x65rrored\x18\x01 \x01(\x08\x62\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_BACKUPCMDSTREAM = _descriptor.Descriptor(
  name='BackupCmdStream',
  full_name='lbackgrpc.BackupCmdStream',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='lbackgrpc.BackupCmdStream.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='raw_data', full_name='lbackgrpc.BackupCmdStream.raw_data', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='shard', full_name='lbackgrpc.BackupCmdStream.shard', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=27,
  serialized_end=89,
)


_BACKUPCMD = _descriptor.Descriptor(
  name='BackupCmd',
  full_name='lbackgrpc.BackupCmd',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='lbackgrpc.BackupCmd.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='temp_id', full_name='lbackgrpc.BackupCmd.temp_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=91,
  serialized_end=131,
)


_BACKUPCMDSTATUS = _descriptor.Descriptor(
  name='BackupCmdStatus',
  full_name='lbackgrpc.BackupCmdStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='elapsed_time', full_name='lbackgrpc.BackupCmdStatus.elapsed_time', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='errored', full_name='lbackgrpc.BackupCmdStatus.errored', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=133,
  serialized_end=189,
)


_RESTORECMD = _descriptor.Descriptor(
  name='RestoreCmd',
  full_name='lbackgrpc.RestoreCmd',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='lbackgrpc.RestoreCmd.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='folder', full_name='lbackgrpc.RestoreCmd.folder', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='use_temp_folder', full_name='lbackgrpc.RestoreCmd.use_temp_folder', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='shard', full_name='lbackgrpc.RestoreCmd.shard', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=191,
  serialized_end=271,
)


_RESTORECMDSTATUS = _descriptor.Descriptor(
  name='RestoreCmdStatus',
  full_name='lbackgrpc.RestoreCmdStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='elapsed_time', full_name='lbackgrpc.RestoreCmdStatus.elapsed_time', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='raw_data', full_name='lbackgrpc.RestoreCmdStatus.raw_data', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='errored', full_name='lbackgrpc.RestoreCmdStatus.errored', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=273,
  serialized_end=348,
)


_RELOCATECMD = _descriptor.Descriptor(
  name='RelocateCmd',
  full_name='lbackgrpc.RelocateCmd',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='lbackgrpc.RelocateCmd.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='src', full_name='lbackgrpc.RelocateCmd.src', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dst', full_name='lbackgrpc.RelocateCmd.dst', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=350,
  serialized_end=401,
)


_RELOCATECMDTAKE = _descriptor.Descriptor(
  name='RelocateCmdTake',
  full_name='lbackgrpc.RelocateCmdTake',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='lbackgrpc.RelocateCmdTake.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=403,
  serialized_end=432,
)


_RELOCATECMDGIVESTREAM = _descriptor.Descriptor(
  name='RelocateCmdGiveStream',
  full_name='lbackgrpc.RelocateCmdGiveStream',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='lbackgrpc.RelocateCmdGiveStream.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='raw_data', full_name='lbackgrpc.RelocateCmdGiveStream.raw_data', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=434,
  serialized_end=487,
)


_RELOCATECMDSTATUS = _descriptor.Descriptor(
  name='RelocateCmdStatus',
  full_name='lbackgrpc.RelocateCmdStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='elapsed_time', full_name='lbackgrpc.RelocateCmdStatus.elapsed_time', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=489,
  serialized_end=530,
)


_RELOCATECMDTAKESTATUS = _descriptor.Descriptor(
  name='RelocateCmdTakeStatus',
  full_name='lbackgrpc.RelocateCmdTakeStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='elapsed_time', full_name='lbackgrpc.RelocateCmdTakeStatus.elapsed_time', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='errored', full_name='lbackgrpc.RelocateCmdTakeStatus.errored', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=532,
  serialized_end=594,
)


_RELOCATECMDGIVESTATUS = _descriptor.Descriptor(
  name='RelocateCmdGiveStatus',
  full_name='lbackgrpc.RelocateCmdGiveStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='errored', full_name='lbackgrpc.RelocateCmdGiveStatus.errored', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=596,
  serialized_end=636,
)


_RMCMD = _descriptor.Descriptor(
  name='RmCmd',
  full_name='lbackgrpc.RmCmd',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='lbackgrpc.RmCmd.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='target', full_name='lbackgrpc.RmCmd.target', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='all', full_name='lbackgrpc.RmCmd.all', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='shard', full_name='lbackgrpc.RmCmd.shard', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=638,
  serialized_end=701,
)


_RMCMDSTATUS = _descriptor.Descriptor(
  name='RmCmdStatus',
  full_name='lbackgrpc.RmCmdStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='elapsed_time', full_name='lbackgrpc.RmCmdStatus.elapsed_time', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='errored', full_name='lbackgrpc.RmCmdStatus.errored', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=703,
  serialized_end=755,
)


_CHECKCMD = _descriptor.Descriptor(
  name='CheckCmd',
  full_name='lbackgrpc.CheckCmd',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='lbackgrpc.CheckCmd.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='shard', full_name='lbackgrpc.CheckCmd.shard', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=757,
  serialized_end=794,
)


_CHECKCMDSTATUS = _descriptor.Descriptor(
  name='CheckCmdStatus',
  full_name='lbackgrpc.CheckCmdStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='errored', full_name='lbackgrpc.CheckCmdStatus.errored', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=796,
  serialized_end=829,
)

DESCRIPTOR.message_types_by_name['BackupCmdStream'] = _BACKUPCMDSTREAM
DESCRIPTOR.message_types_by_name['BackupCmd'] = _BACKUPCMD
DESCRIPTOR.message_types_by_name['BackupCmdStatus'] = _BACKUPCMDSTATUS
DESCRIPTOR.message_types_by_name['RestoreCmd'] = _RESTORECMD
DESCRIPTOR.message_types_by_name['RestoreCmdStatus'] = _RESTORECMDSTATUS
DESCRIPTOR.message_types_by_name['RelocateCmd'] = _RELOCATECMD
DESCRIPTOR.message_types_by_name['RelocateCmdTake'] = _RELOCATECMDTAKE
DESCRIPTOR.message_types_by_name['RelocateCmdGiveStream'] = _RELOCATECMDGIVESTREAM
DESCRIPTOR.message_types_by_name['RelocateCmdStatus'] = _RELOCATECMDSTATUS
DESCRIPTOR.message_types_by_name['RelocateCmdTakeStatus'] = _RELOCATECMDTAKESTATUS
DESCRIPTOR.message_types_by_name['RelocateCmdGiveStatus'] = _RELOCATECMDGIVESTATUS
DESCRIPTOR.message_types_by_name['RmCmd'] = _RMCMD
DESCRIPTOR.message_types_by_name['RmCmdStatus'] = _RMCMDSTATUS
DESCRIPTOR.message_types_by_name['CheckCmd'] = _CHECKCMD
DESCRIPTOR.message_types_by_name['CheckCmdStatus'] = _CHECKCMDSTATUS

BackupCmdStream = _reflection.GeneratedProtocolMessageType('BackupCmdStream', (_message.Message,), dict(
  DESCRIPTOR = _BACKUPCMDSTREAM,
  __module__ = 'shared_pb2'
  # @@protoc_insertion_point(class_scope:lbackgrpc.BackupCmdStream)
  ))
_sym_db.RegisterMessage(BackupCmdStream)

BackupCmd = _reflection.GeneratedProtocolMessageType('BackupCmd', (_message.Message,), dict(
  DESCRIPTOR = _BACKUPCMD,
  __module__ = 'shared_pb2'
  # @@protoc_insertion_point(class_scope:lbackgrpc.BackupCmd)
  ))
_sym_db.RegisterMessage(BackupCmd)

BackupCmdStatus = _reflection.GeneratedProtocolMessageType('BackupCmdStatus', (_message.Message,), dict(
  DESCRIPTOR = _BACKUPCMDSTATUS,
  __module__ = 'shared_pb2'
  # @@protoc_insertion_point(class_scope:lbackgrpc.BackupCmdStatus)
  ))
_sym_db.RegisterMessage(BackupCmdStatus)

RestoreCmd = _reflection.GeneratedProtocolMessageType('RestoreCmd', (_message.Message,), dict(
  DESCRIPTOR = _RESTORECMD,
  __module__ = 'shared_pb2'
  # @@protoc_insertion_point(class_scope:lbackgrpc.RestoreCmd)
  ))
_sym_db.RegisterMessage(RestoreCmd)

RestoreCmdStatus = _reflection.GeneratedProtocolMessageType('RestoreCmdStatus', (_message.Message,), dict(
  DESCRIPTOR = _RESTORECMDSTATUS,
  __module__ = 'shared_pb2'
  # @@protoc_insertion_point(class_scope:lbackgrpc.RestoreCmdStatus)
  ))
_sym_db.RegisterMessage(RestoreCmdStatus)

RelocateCmd = _reflection.GeneratedProtocolMessageType('RelocateCmd', (_message.Message,), dict(
  DESCRIPTOR = _RELOCATECMD,
  __module__ = 'shared_pb2'
  # @@protoc_insertion_point(class_scope:lbackgrpc.RelocateCmd)
  ))
_sym_db.RegisterMessage(RelocateCmd)

RelocateCmdTake = _reflection.GeneratedProtocolMessageType('RelocateCmdTake', (_message.Message,), dict(
  DESCRIPTOR = _RELOCATECMDTAKE,
  __module__ = 'shared_pb2'
  # @@protoc_insertion_point(class_scope:lbackgrpc.RelocateCmdTake)
  ))
_sym_db.RegisterMessage(RelocateCmdTake)

RelocateCmdGiveStream = _reflection.GeneratedProtocolMessageType('RelocateCmdGiveStream', (_message.Message,), dict(
  DESCRIPTOR = _RELOCATECMDGIVESTREAM,
  __module__ = 'shared_pb2'
  # @@protoc_insertion_point(class_scope:lbackgrpc.RelocateCmdGiveStream)
  ))
_sym_db.RegisterMessage(RelocateCmdGiveStream)

RelocateCmdStatus = _reflection.GeneratedProtocolMessageType('RelocateCmdStatus', (_message.Message,), dict(
  DESCRIPTOR = _RELOCATECMDSTATUS,
  __module__ = 'shared_pb2'
  # @@protoc_insertion_point(class_scope:lbackgrpc.RelocateCmdStatus)
  ))
_sym_db.RegisterMessage(RelocateCmdStatus)

RelocateCmdTakeStatus = _reflection.GeneratedProtocolMessageType('RelocateCmdTakeStatus', (_message.Message,), dict(
  DESCRIPTOR = _RELOCATECMDTAKESTATUS,
  __module__ = 'shared_pb2'
  # @@protoc_insertion_point(class_scope:lbackgrpc.RelocateCmdTakeStatus)
  ))
_sym_db.RegisterMessage(RelocateCmdTakeStatus)

RelocateCmdGiveStatus = _reflection.GeneratedProtocolMessageType('RelocateCmdGiveStatus', (_message.Message,), dict(
  DESCRIPTOR = _RELOCATECMDGIVESTATUS,
  __module__ = 'shared_pb2'
  # @@protoc_insertion_point(class_scope:lbackgrpc.RelocateCmdGiveStatus)
  ))
_sym_db.RegisterMessage(RelocateCmdGiveStatus)

RmCmd = _reflection.GeneratedProtocolMessageType('RmCmd', (_message.Message,), dict(
  DESCRIPTOR = _RMCMD,
  __module__ = 'shared_pb2'
  # @@protoc_insertion_point(class_scope:lbackgrpc.RmCmd)
  ))
_sym_db.RegisterMessage(RmCmd)

RmCmdStatus = _reflection.GeneratedProtocolMessageType('RmCmdStatus', (_message.Message,), dict(
  DESCRIPTOR = _RMCMDSTATUS,
  __module__ = 'shared_pb2'
  # @@protoc_insertion_point(class_scope:lbackgrpc.RmCmdStatus)
  ))
_sym_db.RegisterMessage(RmCmdStatus)

CheckCmd = _reflection.GeneratedProtocolMessageType('CheckCmd', (_message.Message,), dict(
  DESCRIPTOR = _CHECKCMD,
  __module__ = 'shared_pb2'
  # @@protoc_insertion_point(class_scope:lbackgrpc.CheckCmd)
  ))
_sym_db.RegisterMessage(CheckCmd)

CheckCmdStatus = _reflection.GeneratedProtocolMessageType('CheckCmdStatus', (_message.Message,), dict(
  DESCRIPTOR = _CHECKCMDSTATUS,
  __module__ = 'shared_pb2'
  # @@protoc_insertion_point(class_scope:lbackgrpc.CheckCmdStatus)
  ))
_sym_db.RegisterMessage(CheckCmdStatus)


try:
  # THESE ELEMENTS WILL BE DEPRECATED.
  # Please use the generated *_pb2_grpc.py files instead.
  import grpc
  from grpc.framework.common import cardinality
  from grpc.framework.interfaces.face import utilities as face_utilities
  from grpc.beta import implementations as beta_implementations
  from grpc.beta import interfaces as beta_interfaces
except ImportError:
  pass
# @@protoc_insertion_point(module_scope)
