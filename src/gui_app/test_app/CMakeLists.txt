
file(GLOB IMGUI_SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/../../include/imgui/*.cpp)

add_executable(test_gui test_app.cpp ${IMGUI_SOURCES})
target_include_directories(test_gui PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/.. ${CMAKE_CURRENT_SOURCE_DIR}/../../include/)
target_link_libraries(test_gui PUBLIC gui_lib)