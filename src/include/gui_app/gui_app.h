#ifndef GUI_APP_H
#include "glad/glad.h"
#include "GLFW/glfw3.h"

class GuiApp{

public:
    GuiApp(int window_width, int window_height, const char* window_title);
    ~GuiApp();

    void register_draw_callback(void (*callback_fn)());
    void register_terminate_callback(void (*callback_fn)());
    
    void update();
    void start_app();
    GLFWwindow* get_window();

private:
    GLFWwindow* window;
    void (*draw_callback_fn)();
    void (*terminate_callback_fn)();
    int width;
    int height;
    const char* title;

    bool initialize();
    void run();

    void terminate();
};

class ImageTexture
{

public:
    GLuint texture_id;
    GLuint width;
    GLuint height;
    GLenum format;
    GLenum type;

    void* data;

    ImageTexture(int width, int height, GLenum format, GLenum type, void* data=nullptr, bool init_texture=true);
    ~ImageTexture();

    virtual void initialize();

    virtual void bind();
    virtual void unbind();

};

class ImageTexture2DStatic : public ImageTexture
{

public:
    ImageTexture2DStatic(const char* filename);
    ~ImageTexture2DStatic();

};

class ImageTexture2DDynamic : public ImageTexture
{

public:
    ImageTexture2DDynamic(int width, int height, GLenum format, GLenum type, void* data=nullptr, bool init_texture=true);
    ~ImageTexture2DDynamic();


    void update(void* data);
};

#endif