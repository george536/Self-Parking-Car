pip install grpcio-tools

#Execute for Python
python -m grpc_tools.protoc -I. --python_out=./python_IPC --grpc_python_out=./python_IPC ipc_configs.proto

cd src

mkdir build_grpc
cd build_grpc
cmake ../grpc -G "Ninja" -DCMAKE_BUILD_TYPE=Debug


cmake --build . --config Debug

mkdir install_grpc
cmake --install . --config Debug --prefix "$pwd/install_grpc"

cd ..

mkdir build_opencv
cd build_opencv
cmake ../opencv -G "Ninja" -DCMAKE_BUILD_TYPE=Debug -DOpenCV_STATIC=ON

cmake --build . --config Debug

mkdir install_opencv
cmake --install . --prefix "$pwd/install_opencv" --config Debug

cd ..

mkdir build_carla


cd ..

cd carla
make setup
make LibCarla

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