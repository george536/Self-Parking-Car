#include "gui_app.h"
#include "imgui/imgui.h"
#include "imgui/imgui_impl_glfw.h"
#include "imgui/imgui_impl_opengl3.h"
#include <memory>

bool imgui_init = false;
bool show_demo_window = true;

std::shared_ptr<GuiApp> app;

void test_callback()
{
    if(!imgui_init)
    {
        ImGui::CreateContext();
        ImGuiIO& io = ImGui::GetIO(); (void)io;
        ImGui::StyleColorsDark();
        imgui_init = true;

        ImGui_ImplGlfw_InitForOpenGL(app->get_window(), true);
        ImGui_ImplOpenGL3_Init("#version 150");
    }

    ImGui_ImplOpenGL3_NewFrame();
    ImGui_ImplGlfw_NewFrame();
    ImGui::NewFrame();

    ImGui::ShowDemoWindow(&show_demo_window);

    ImGui::Render();
    ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());
}

void terminate_callback()
{
    ImGui_ImplOpenGL3_Shutdown();
    ImGui_ImplGlfw_Shutdown();
    ImGui::DestroyContext();
}

int main()
{

    app = std::make_shared<GuiApp>(800, 600, "Test App");

    app->start_app();

    app->register_draw_callback(test_callback);

    app->register_terminate_callback(terminate_callback);

    while(true)
    {

    }

    return 0;

}