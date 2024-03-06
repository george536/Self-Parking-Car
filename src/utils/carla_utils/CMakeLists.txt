cmake_minimum_required(VERSION 3.23)

set(SOURCES
    src/carla_utils.cpp
    include/carla_utils.h
)

set(CARLA_LIB_PATH ${CMAKE_CURRENT_LIST_DIR}/../../libcarla)

add_library(CarlaUtils STATIC ${SOURCES})
LINK_DIRECTORIES(libcarla)

include_directories(${CARLA_LIB_PATH}/include)
include_directories(${CARLA_LIB_PATH}/include/system)

target_include_directories(CarlaUtils PUBLIC include)
target_link_libraries(CarlaUtils PUBLIC carla_client_debug Shlwapi
debugutils-d detour-d detourcrowd-d detourTileCache-d libboost_atomic-vc142-mt-x64-1_83 libboost_date_time-vc142-mt-x64-1_83 
libboost_numpy39-vc142-mt-x64-1_80 libboost_python39-vc142-mt-x64-1_80 
libboost_system-vc142-mt-x64-1_83 libpng proj recast-d rpc sqlite3 xerces-c_3 zlibstatic)