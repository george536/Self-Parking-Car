cmake_minimum_required(VERSION 3.23)
project(IPC_lib CXX)

include(FetchContent)

set(OpenCV_DIR ${CMAKE_CURRENT_LIST_DIR}/build_opencv)
set(gRPC_DIR ${CMAKE_CURRENT_LIST_DIR}/build_grpc/install_grpc/lib/cmake/grpc)
set(absl_DIR ${CMAKE_CURRENT_LIST_DIR}/build_grpc/install_grpc/lib/cmake/absl)
set(protobuf_DIR ${CMAKE_CURRENT_LIST_DIR}/build_grpc/install_grpc/cmake)
set(utf8_range_DIR ${CMAKE_CURRENT_LIST_DIR}/build_grpc/install_grpc/lib/cmake/utf8_range)

FIND_PACKAGE(OpenCV REQUIRED)
find_package(utf8_range CONFIG REQUIRED)
FIND_PACKAGE(protobuf CONFIG)
FIND_PACKAGE(gRPC CONFIG REQUIRED)
add_subdirectory(googletest)

set(LIBCARLA_BUILD_DEBUG ON)
set(LIBCARLA_BUILD_RELEASE OFF)
set(LIBCARLA_BUILD_TEST OFF)


include_directories(include/ipc_configs.pb.h)
include_directories(grpc_processing_utils/include/grpc_data_processor.h)
include_directories(include/ipc_configs.grpc.pb.h)
include_directories(${CMAKE_CURRENT_LIST_DIR}/build_grpc/install_grpc/include)

FetchContent_Declare(json URL https://github.com/nlohmann/json/releases/download/v3.11.2/json.tar.xz)
FetchContent_MakeAvailable(json)

add_executable(ipc_server server.cpp ./include/ipc_configs.pb.cc ./grpc_processing_utils/grpc_data_processor.cpp ./include/ipc_configs.grpc.pb.cc)
add_executable(grpc_test ./test/grpc_data_processor_test.cpp ./grpc_processing_utils/grpc_data_processor.cpp)

message(PROJECT_SOURCE_DIR="${OpenCV_LIBS}")

target_link_libraries(ipc_server gRPC::grpc++ ${OpenCV_LIBS} nlohmann_json::nlohmann_json)
target_link_libraries(grpc_test GTest::gtest gmock gmock_main GTest::gtest_main gRPC::grpc++ ${OpenCV_LIBS} nlohmann_json::nlohmann_json)