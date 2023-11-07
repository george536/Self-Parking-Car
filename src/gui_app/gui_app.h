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
#endif