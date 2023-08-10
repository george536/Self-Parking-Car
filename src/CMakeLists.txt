cmake_minimum_required(VERSION 3.15)
project(IPC_lib CXX)

include(FetchContent)

set(ABSL_ENABLE_INSTALL ON)

FetchContent_Declare(
  gRPC
  GIT_REPOSITORY https://github.com/grpc/grpc
  GIT_TAG        v1.56.0
)
set(FETCHCONTENT_QUIET OFF)
FetchContent_MakeAvailable(gRPC)

include_directories(include/ipc_configs.pb.h)

add_executable(ipc_server server.cpp ipc_configs.pb.cc)

target_link_libraries(ipc_server grpc++)
