# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: python_IPC/ipc_configs.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1cpython_IPC/ipc_configs.proto\x12\x12\x42\x45V_image_transfer\"\x81\x01\n\x0crequest_data\x12\x35\n\nimage_data\x18\x01 \x01(\x0b\x32!.BEV_image_transfer.image_request\x12:\n\x0c\x63\x61r_location\x18\x02 \x01(\x0b\x32$.BEV_image_transfer.location_request\"\x1d\n\rimage_request\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x0c\"]\n\x10location_request\x12\t\n\x01x\x18\x01 \x01(\x05\x12\t\n\x01y\x18\x02 \x01(\x05\x12\t\n\x01z\x18\x03 \x01(\x05\x12\r\n\x05pitch\x18\x04 \x01(\x05\x12\x0b\n\x03yaw\x18\x05 \x01(\x05\x12\x0c\n\x04roll\x18\x06 \x01(\x05\"\x1e\n\x0c\x65mpty_return\x12\x0e\n\x06result\x18\x01 \x01(\x05\x32\x61\n\x0eimage_transfer\x12O\n\tsend_data\x12 .BEV_image_transfer.request_data\x1a .BEV_image_transfer.empty_returnb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'python_IPC.ipc_configs_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_REQUEST_DATA']._serialized_start=53
  _globals['_REQUEST_DATA']._serialized_end=182
  _globals['_IMAGE_REQUEST']._serialized_start=184
  _globals['_IMAGE_REQUEST']._serialized_end=213
  _globals['_LOCATION_REQUEST']._serialized_start=215
  _globals['_LOCATION_REQUEST']._serialized_end=308
  _globals['_EMPTY_RETURN']._serialized_start=310
  _globals['_EMPTY_RETURN']._serialized_end=340
  _globals['_IMAGE_TRANSFER']._serialized_start=342
  _globals['_IMAGE_TRANSFER']._serialized_end=439
# @@protoc_insertion_point(module_scope)
