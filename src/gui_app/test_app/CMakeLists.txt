add_executable(test_gui test_app.cpp)
target_include_directories(test_gui PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/..)
target_link_libraries(test_gui PUBLIC gui_lib)