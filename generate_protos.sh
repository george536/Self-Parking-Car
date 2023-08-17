#!/bin/bash

# Execute for Python
python -m grpc_tools.protoc -I. --python_out=./python_IPC --grpc_python_out=./python_IPC ipc_configs.proto

# Execute for C++
protoc --proto_path=./ --cpp_out=./src/include/ ./ipc_configs.proto

# Execute for gRPC C++, only after grpc++ has been build using CMake
# Give full path for protos folder like below
# protoc --proto_path=./ -I "D:\CARLA_0.9.14\Self-Parking-Car\src\build\protos" --grpc_out=./src/include/ --plugin=protoc-gen-grpc="D:\CARLA_0.9.14\Self-Parking-Car\src\build\_deps\grpc-build\grpc_cpp_plugin.exe" ./ipc_configs.proto