cmake_minimum_required(VERSION 3.23)
project(IPC_lib CXX C)

include(FetchContent)

set(OpenCV_DIR ${CMAKE_CURRENT_LIST_DIR}/build_opencv)
set(gRPC_DIR ${CMAKE_CURRENT_LIST_DIR}/build_grpc/install_grpc/lib/cmake/grpc)
set(absl_DIR ${CMAKE_CURRENT_LIST_DIR}/build_grpc/install_grpc/lib/cmake/absl)
set(protobuf_DIR ${CMAKE_CURRENT_LIST_DIR}/build_grpc/install_grpc/cmake)
set(utf8_range_DIR ${CMAKE_CURRENT_LIST_DIR}/build_grpc/install_grpc/lib/cmake/utf8_range)
set(CARLA_LIB_PATH ${CMAKE_CURRENT_LIST_DIR}/libcarla)
set(protobuf_carla_dependency "gRPC::grpc++" "nlohmann_json::nlohmann_json" 
"carla_client_debug" "debugutils" "detour" "detourcrowd" "detourTileCache" "libboost_atomic-vc142-mt-x64-1_80" 
"libboost_date_time-vc142-mt-x64-1_80" "libboost_filesystem-vc142-mt-x64-1_80" "libboost_numpy39-vc142-mt-x64-1_80" 
"libboost_python39-vc142-mt-x64-1_80" "libboost_system-vc142-mt-x64-1_80" "libpng" "proj" "recast" 
"rpc" "sqlite3" "xerces-c_3" "zlibstatic")

set(protobuf_source "./include/ipc_configs.pb.cc" "./grpc_processing_utils/grpc_data_processor.cpp" "./include/ipc_configs.grpc.pb.cc")

FIND_PACKAGE(OpenCV REQUIRED)
find_package(utf8_range CONFIG REQUIRED)
FIND_PACKAGE(protobuf CONFIG)
FIND_PACKAGE(gRPC CONFIG REQUIRED)
add_subdirectory(googletest)

add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/utils/file_utils)
add_subdirectory(gui_app)
add_subdirectory(test_app)
LINK_DIRECTORIES(libcarla)
link_directories(glfw)

include_directories(grpc_server/include/ipc_configs.pb.h)
include_directories(grpc_server/include/ipc_configs.grpc.pb.h)
include_directories(grpc_processing_utils/include/grpc_data_processor.h)
include_directories(${CMAKE_CURRENT_LIST_DIR}/build_grpc/install_grpc/include)
include_directories(${CMAKE_CURRENT_LIST_DIR}/libcarla/include)
include_directories(${CMAKE_CURRENT_LIST_DIR}/libcarla/include/system)
include_directories(${CMAKE_CURRENT_LIST_DIR}/glfw)
include_directories(auto_spawn_utils/include/auto_spawn.h)

add_executable(ipc_server ./grpc_server/run_server.cpp ./grpc_server/include/ipc_configs.pb.cc ./grpc_server/include/ipc_configs.grpc.pb.cc)
add_executable(grpc_test ./test/grpc_data_processor_test.cpp ./grpc_processing_utils/grpc_data_processor.cpp ./grpc_server/include/ipc_configs.grpc.pb.cc ./grpc_server/include/ipc_configs.pb.cc)
add_executable(file_utils_test ./test/file_utils_test.cpp)
add_executable(auto_spawn ./auto_spawn_utils/run_auto_spawn.cpp ./grpc_processing_utils/grpc_data_processor.cpp ./grpc_server/src/server.cpp ./grpc_server/include/ipc_configs.pb.cc ./grpc_server/include/ipc_configs.grpc.pb.cc)

message(PROJECT_SOURCE_DIR="${OpenCV_LIBS}")

target_link_libraries(ipc_server FileUtilsLib gRPC::grpc++ ${OpenCV_LIBS})

target_link_libraries(grpc_test FileUtilsLib GTest::gtest gmock gmock_main GTest::gtest_main gRPC::grpc++ ${OpenCV_LIBS})
target_link_libraries(file_utils_test FileUtilsLib GTest::gtest gmock gmock_main GTest::gtest_main)

target_link_options(auto_spawn PRIVATE "/NODEFAULTLIB:MSVCRT")

<<<<<<< HEAD
target_link_libraries(auto_spawn FileUtilsLib ${OpenCV_LIBS} carla_client_debug Shlwapi
debugutils-d detour-d detourcrowd-d detourTileCache-d libboost_atomic-vc142-mt-x64-1_83 libboost_date_time-vc142-mt-x64-1_83 
libboost_numpy39-vc142-mt-x64-1_80 libboost_python39-vc142-mt-x64-1_80 
<<<<<<< HEAD
libboost_system-vc142-mt-x64-1_83 libpng proj recast-d rpc sqlite3 xerces-c_3 zlibstatic)
=======
libboost_system-vc142-mt-x64-1_83 libpng proj recast-d rpc sqlite3 xerces-c_3 zlibstatic gRPC::grpc++)
>>>>>>> 17fbcbe0 (Added callback, not yet working)
=======
target_link_libraries(auto_spawn FileUtilsLib ${OpenCV_LIBS} CarlaUtils gRPC::grpc++)
>>>>>>> 7e9a250c (Moved carla functions into Carla Lib)
