pip install grpcio-tools

#Execute for Python
python -m grpc_tools.protoc -I. --python_out=./python_IPC --grpc_python_out=./python_IPC ipc_configs.proto

# Execute for C++
src/build_grpc/third_party/protobuf/protoc --proto_path=./ --cpp_out=./src/include/ ./ipc_configs.proto

# Execute for gRPC C++, only after grpc++ has been build using CMake
# Give full path for protos folder like below
src/build_grpc/third_party/protobuf/protoc --proto_path=./ -I "$pwd\src\build_grpc\protos" --grpc_out=./src/include/ --plugin=protoc-gen-grpc="$pwd\src\build_grpc\grpc_cpp_plugin.exe" ./ipc_configs.proto

mkdir src/build
cd src/build
cmake ../ -G "Ninja" -DCMAKE_BUILD_TYPE=Debug

cmake --build . --config Debug
cd ../..

# Copying all .dll files needed for opencv
$sourcePath = "$pwd/src/build_opencv/bin"
$destinationPath = "$pwd/src/build"

# Copy all .dll files from the source to the destination folder
Get-ChildItem -Path $sourcePath -Filter "*.dll" | ForEach-Object {
    Copy-Item -Path $_.FullName -Destination $destinationPath
}

Write-Host "Copying .dll files to build folder has completed."