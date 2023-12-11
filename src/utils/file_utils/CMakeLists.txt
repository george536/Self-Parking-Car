cmake_minimum_required(VERSION 3.23)
include(FetchContent)

set(SOURCES
    src/file_utils.cpp
    include/file_utils.h
)

add_library(FileUtilsLib STATIC ${SOURCES})

FetchContent_Declare(json URL https://github.com/nlohmann/json/releases/download/v3.11.2/json.tar.xz)
FetchContent_MakeAvailable(json)

target_include_directories(FileUtilsLib PUBLIC include)
target_link_libraries(FileUtilsLib PUBLIC nlohmann_json::nlohmann_json)