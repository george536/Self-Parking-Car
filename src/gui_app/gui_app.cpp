#include "gui_app.h"
#include <iostream>
#include <thread>

GuiApp::GuiApp(int window_width, int window_height, const char* window_title){
    width = window_width;
    height = window_height;
    window = NULL;
    title = window_title;
    draw_callback_fn = NULL;
    
}

GuiApp::~GuiApp()
{
}

void GuiApp::start_app()
{
    std::thread t(&GuiApp::run, this);
    t.detach();
}

void GuiApp::register_draw_callback(void(*callback_fn)())
{
    draw_callback_fn = callback_fn;
}

bool GuiApp::initialize()
{
    if(!glfwInit())
    {
        std::cout << "Failed to initialize GLFW" << std::endl;
        return false;
    }

    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 6);

    window = glfwCreateWindow(width, height, title, NULL, NULL);

    if(!window)
    {
        std::cout << "Failed to create GLFW window" << std::endl;
        glfwTerminate();
        return false;
    }

    glfwMakeContextCurrent(window);
    //help
    gladLoadGLLoader((GLADloadproc) glfwGetProcAddress);

    return true;
}

void GuiApp::run()
{
    // all in the same thread
    initialize();
    while(!glfwWindowShouldClose(window))
    {
        update();
        glfwSwapBuffers(window);
        glfwPollEvents();
    }


}

void GuiApp::terminate()
{
    glfwTerminate();
}

void GuiApp::update()
{
    if(draw_callback_fn != NULL)
    {
        draw_callback_fn();
    }
}

void GuiApp::key_callback(GLFWwindow *window, int key, int scancode, int action, int mods)
{
}

void GuiApp::mouse_button_callback(GLFWwindow *window, int button, int action, int mods)
{
}
