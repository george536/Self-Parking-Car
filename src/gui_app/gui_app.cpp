#include "gui_app.h"
#include <iostream>
#include <thread>
#include <assert.h>

#define STB_IMAGE_IMPLEMENTATION 1 

#include "stb_image.h"

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
    assert(draw_callback_fn != NULL);
    assert(terminate_callback_fn != NULL);
    std::thread t(&GuiApp::run, this);
    t.join();
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

ImageTexture::ImageTexture(int width, int height, GLenum format, GLenum type, void *data, bool init_texture)
{
    this->width = width;
    this->height = height;
    this->data = data;
    this->format = format;
    this->type = type;

    if(init_texture)
        initialize();
}

ImageTexture::~ImageTexture()
{
    glDeleteTextures(1, &texture_id);
}

void ImageTexture::initialize()
{

    glGenTextures(1, &texture_id);
    glBindTexture(GL_TEXTURE_2D, texture_id);

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
    
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

    
    glTexImage2D(GL_TEXTURE_2D, 0, format, width, height, 0, format, type, (data==nullptr)? NULL : data);

    if(data)
    {
        glGenerateMipmap(GL_TEXTURE_2D);
    }

    glBindTexture(GL_TEXTURE_2D, 0);

}

void ImageTexture::bind()
{
    glBindTexture(GL_TEXTURE_2D, texture_id);
}

void ImageTexture::unbind()
{
    glBindTexture(GL_TEXTURE_2D, 0);
}

ImageTexture2DStatic::ImageTexture2DStatic(const char *filename):ImageTexture(0, 0, GL_RGB, GL_UNSIGNED_BYTE, nullptr, false)
{
    int width, height, nrChannels;
    unsigned char *data = stbi_load(filename, &width, &height, &nrChannels, 0);

    if(data)
    {
        this->width = width;
        this->height = height;
        this->format = (nrChannels == 3)? GL_RGB : GL_RGBA;
        this->type = GL_UNSIGNED_BYTE;
        this->data = data;
        initialize();
    }
    else
    {
        std::cout << "Failed to load texture" << std::endl;
    }
    
    
}

ImageTexture2DStatic::~ImageTexture2DStatic()
{
    stbi_image_free(data);
}

ImageTexture2DDynamic::ImageTexture2DDynamic(int width, int height, GLenum format, GLenum type, void *data, bool init_texture): ImageTexture(width, height, format, type, data, init_texture)
{

}

ImageTexture2DDynamic::~ImageTexture2DDynamic()
{
}

void ImageTexture2DDynamic::update(void *data)
{
    glBindTexture(GL_TEXTURE_2D, texture_id);
    glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, width, height, format, type, data);
    glBindTexture(GL_TEXTURE_2D, 0);
}
