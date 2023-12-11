param(
    [switch]$generate = $false,
    [switch]$compile_proto = $false
)


if($generate){
    Write-Host "Generating project files"
}else
{
    Write-Host "Skipping generation of project files"
}


if($compile_proto){
    Write-Host "Compiling proto files"

    #Execute for Python
    python -m grpc_tools.protoc -I. --python_out=./python_IPC --grpc_python_out=./python_IPC ipc_configs.proto

    # Execute for C++
    src/build_grpc/third_party/protobuf/protoc --proto_path=./ --cpp_out=./src/include/ ./ipc_configs.proto

    # Execute for gRPC C++, only after grpc++ has been build using CMake
    # Give full path for protos folder like below
    src/build_grpc/third_party/protobuf/protoc --proto_path=./ -I "$pwd\src\build_grpc\protos" --grpc_out=./src/include/ --plugin=protoc-gen-grpc="$pwd\src\build_grpc\grpc_cpp_plugin.exe" ./ipc_configs.proto
}else{
    Write-Host "Skipping compilation of proto files"
}

mkdir src/build
cd src/build

if($generate){
    cmake ../ -G "Ninja" -DCMAKE_BUILD_TYPE=Debug
}

cmake --build . --config Debug
cd ../..

