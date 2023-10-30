cmake_minimum_required(VERSION 3.23)
project(IPC_lib CXX C)

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

#add_subdirectory(libcarla)

LINK_DIRECTORIES(libcarla)
link_directories(glfw)

include_directories(include/ipc_configs.pb.h)
include_directories(grpc_processing_utils/include/grpc_data_processor.h)
include_directories(include/ipc_configs.grpc.pb.h)
include_directories(${CMAKE_CURRENT_LIST_DIR}/build_grpc/install_grpc/include)
include_directories(${CMAKE_CURRENT_LIST_DIR}/libcarla/include)
include_directories(${CMAKE_CURRENT_LIST_DIR}/libcarla/include/system)
include_directories(${CMAKE_CURRENT_LIST_DIR}/glfw)

add_subdirectory(gui_app)

FetchContent_Declare(json URL https://github.com/nlohmann/json/releases/download/v3.11.2/json.tar.xz)
FetchContent_MakeAvailable(json)

set(protobuf_carla_dependency "gRPC::grpc++" "nlohmann_json::nlohmann_json" 
"carla_client_debug" "debugutils" "detour" "detourcrowd" "detourTileCache" "libboost_atomic-vc142-mt-x64-1_80" 
"libboost_date_time-vc142-mt-x64-1_80" "libboost_filesystem-vc142-mt-x64-1_80" "libboost_numpy39-vc142-mt-x64-1_80" 
"libboost_python39-vc142-mt-x64-1_80" "libboost_system-vc142-mt-x64-1_80" "libpng" "proj" "recast" 
"rpc" "sqlite3" "xerces-c_3" "zlibstatic")

set(protobuf_source "./include/ipc_configs.pb.cc" "./grpc_processing_utils/grpc_data_processor.cpp" "./include/ipc_configs.grpc.pb.cc")

add_executable(ipc_server server.cpp ${protobuf_source})
add_executable(grpc_test ./test/grpc_data_processor_test.cpp ${protobuf_source})



target_link_libraries(ipc_server ${OpenCV_LIBS} ${protobuf_carla_dependency})

target_link_libraries(grpc_test GTest::gtest gmock gmock_main GTest::gtest_main gRPC::grpc++ ${OpenCV_LIBS} nlohmann_json::nlohmann_json)