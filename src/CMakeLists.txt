cmake_minimum_required(VERSION 3.23)
set(CMAKE_CXX_STANDARD 17)
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

set(CARLA_LIB_PATH ${CMAKE_CURRENT_LIST_DIR}/libcarla)

set(FileUtilsLib_DIR ${CMAKE_CURRENT_LIST_DIR}/utils/file_utils/build)
find_package(FileUtilsLib REQUIRED)
target_include_directories(FileUtilsLib PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)

LINK_DIRECTORIES(libcarla)

include_directories(include/ipc_configs.pb.h)
include_directories(grpc_processing_utils/include/grpc_data_processor.h)
include_directories(include/ipc_configs.grpc.pb.h)
include_directories(${CMAKE_CURRENT_LIST_DIR}/build_grpc/install_grpc/include)
include_directories(${CMAKE_CURRENT_LIST_DIR}/libcarla/include)
include_directories(${CMAKE_CURRENT_LIST_DIR}/libcarla/include/system)

add_executable(ipc_server server.cpp ./include/ipc_configs.pb.cc ./grpc_processing_utils/grpc_data_processor.cpp ./include/ipc_configs.grpc.pb.cc)
add_executable(grpc_test ./test/grpc_data_processor_test.cpp ./grpc_processing_utils/grpc_data_processor.cpp ./include/ipc_configs.grpc.pb.cc ./include/ipc_configs.pb.cc)
add_executable(file_utils_test ./test/file_utils_test.cpp)

message(PROJECT_SOURCE_DIR="${OpenCV_LIBS}")

target_link_libraries(ipc_server gRPC::grpc++ ${OpenCV_LIBS} carla_client_debug 
debugutils detour detourcrowd detourTileCache libboost_atomic-vc142-mt-x64-1_80 libboost_date_time-vc142-mt-x64-1_80 
libboost_filesystem-vc142-mt-x64-1_80 libboost_numpy39-vc142-mt-x64-1_80 libboost_python39-vc142-mt-x64-1_80 
libboost_system-vc142-mt-x64-1_80 libpng proj recast rpc sqlite3 xerces-c_3 zlibstatic)

target_link_libraries(grpc_test GTest::gtest gmock gmock_main GTest::gtest_main gRPC::grpc++ ${OpenCV_LIBS})
target_link_libraries(file_utils_test GTest::gtest gmock gmock_main GTest::gtest_main)