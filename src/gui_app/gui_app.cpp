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

GLFWwindow* GuiApp::get_window()
{
    return window;
}

void GuiApp::register_draw_callback(void(*callback_fn)())
{
    draw_callback_fn = callback_fn;
}

void GuiApp::register_terminate_callback(void(*callback_fn)())
{
    terminate_callback_fn = callback_fn;
}

bool GuiApp::initialize()
{
    if(!glfwInit())
    {
        std::cout << "Failed to initialize GLFW" << std::endl;
        return false;
    }

    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 2);

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
    glfwSwapInterval(1);

    return true;
}

void GuiApp::run()
{
    // all in the same thread
    initialize();
    while(!glfwWindowShouldClose(window))
    {
        glfwPollEvents();
        

        int display_w, display_h;
        glfwGetFramebufferSize(window, &display_w, &display_h);

        glViewport(0, 0, display_w, display_h);
        glClearColor(0, 0, 0, 1);
        glClear(GL_COLOR_BUFFER_BIT);
        update();
        glfwSwapBuffers(window);
        
    }


}

void GuiApp::terminate()
{

    if(!terminate_callback_fn){
        std::cout << "No terminate callback registered" << std::endl;
    }
    else{
        terminate_callback_fn();
    }
    glfwDestroyWindow(window);
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
