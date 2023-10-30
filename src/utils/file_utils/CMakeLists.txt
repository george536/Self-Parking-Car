cmake_minimum_required(VERSION 3.23)
set(CMAKE_CXX_STANDARD 17)
project(FileUtilsLib CXX)

include(FetchContent)

set(SOURCES
    src/file_utils.cpp
)

add_library(FileUtilsLib ${SOURCES})

FetchContent_Declare(json URL https://github.com/nlohmann/json/releases/download/v3.11.2/json.tar.xz)
FetchContent_MakeAvailable(json)

target_include_directories(FileUtilsLib PUBLIC include)
target_link_libraries(FileUtilsLib PRIVATE nlohmann_json)


install(TARGETS FileUtilsLib DESTINATION lib)
install(DIRECTORY include/ DESTINATION include)

export(TARGETS FileUtilsLib nlohmann_json FILE FileUtilsLibConfig.cmake)