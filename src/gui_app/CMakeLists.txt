link_directories(../glfw)



add_library(gui_lib STATIC gui_app.cpp ../glfw/glad/glad.c)
target_include_directories(gui_lib PUBLIC ../glfw ../glfw/glad ../include/gui_app)
target_link_libraries(gui_lib glfw3.lib)