@echo off

pip install grpcio-tools

REM Execute for Python
REM python -m grpc_tools.protoc -I. --python_out=./python_IPC --grpc_python_out=./python_IPC ipc_configs.proto

cd src

copy ".\cmakeFiles\cmake1.txt" ".\CMakeLists.txt"

mkdir build
cd build
cmake ../ -G "Ninja"

cmake --build .

cd ..

copy ".\cmakeFiles\cmake2.txt" ".\CMakeLists.txt"

cd ..

REM Execute for C++
protoc --proto_path=./ --cpp_out=./src/include/ ./ipc_configs.proto

REM Execute for gRPC C++, only after grpc++ has been build using CMake
REM Give full path for protos folder like below
protoc --proto_path=./ -I "%current_path%src\build\protos" --grpc_out=./src/include/ --plugin=protoc-gen-grpc="%current_path%src\build\_deps\grpc-build\grpc_cpp_plugin.exe" ./ipc_configs.proto

cd src/build
cmake ../ -G "Ninja"

cmake --build .