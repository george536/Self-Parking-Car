
file(GLOB IMGUI_SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/../include/imgui/*.cpp)

add_executable(test_gui test_app.cpp ${IMGUI_SOURCES})
target_include_directories(test_gui PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/../include/ ${CMAKE_CURRENT_SOURCE_DIR}/../include/gui_app/)
target_link_libraries(test_gui PUBLIC gui_lib)

file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/cat.jpg ${CMAKE_CURRENT_SOURCE_DIR}/cat2.jpg DESTINATION ${CMAKE_CURRENT_BINARY_DIR})