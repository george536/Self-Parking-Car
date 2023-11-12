#include "gui_app.h"
#include "imgui/imgui.h"
#include "imgui/imgui_impl_glfw.h"
#include "imgui/imgui_impl_opengl3.h"
#include <memory>

//#define STB_IMAGE_IMPLEMENTATION 1 

#include "stb_image.h"

bool imgui_init = false;
bool show_demo_window = true;

std::shared_ptr<GuiApp> app;

std::unique_ptr<ImageTexture2DStatic> texture;

std::unique_ptr<ImageTexture2DDynamic> texture_dynamic;

unsigned char* cat1;

int cat1_width;
int cat1_height;
int cat1_nrchannels;

unsigned char * cat2;
int cat2_width;
int cat2_height;
int cat2_nrchannels;

bool cat1_flag = true;

int frame_counter = 0;

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

    if(!texture)
    {
        texture = std::make_unique<ImageTexture2DStatic>("cat.jpg");
    }

    if(!texture_dynamic)
    {
        cat1_flag = true;
        cat1 = stbi_load("cat.jpg", &cat1_width, &cat1_height, &cat1_nrchannels , 0);   
        cat2 = stbi_load("cat2.jpg", &cat2_width, &cat2_height, &cat2_nrchannels , 0);
        texture_dynamic = std::make_unique<ImageTexture2DDynamic>(cat1_width, cat1_height, GL_RGB, GL_UNSIGNED_BYTE, cat1);
    }



    ImGui_ImplOpenGL3_NewFrame();
    ImGui_ImplGlfw_NewFrame();
    ImGui::NewFrame();

    ImGui::ShowDemoWindow(&show_demo_window);

    ImGui::Begin("OpenGL Texture Test Static");
        ImGui::Text("pointer = %p", texture->texture_id);
        ImGui::Text("size = %d x %d", texture ->width, texture->height);
        ImGui::Image((void*)(intptr_t)texture->texture_id, ImVec2(texture->width, texture->height));
    ImGui::End();

    frame_counter++;
    if(frame_counter == 100)
    {
        frame_counter = 0;
    }
    if(frame_counter % 10 == 0)
    {
        if(cat1_flag)
        {
            texture_dynamic->update(cat1);
            cat1_flag = false;
        }else{
            texture_dynamic->update(cat2);
            cat1_flag = true;
        }
    }

    ImGui::Begin("OpenGL Texture Test Dynamic");
        ImGui::Text("pointer = %p", texture_dynamic->texture_id);
        ImGui::Text("size = %d x %d", texture_dynamic ->width, texture_dynamic->height);
        ImGui::Image((void*)(intptr_t)texture_dynamic->texture_id, ImVec2(texture_dynamic->width, texture_dynamic->height));
    ImGui::End();

    ImGui::Render();
    ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());
}

void terminate_callback()
{
    texture_dynamic.reset();
    texture.reset();
    stbi_image_free(cat2);
    stbi_image_free(cat1);
    ImGui_ImplOpenGL3_Shutdown();
    ImGui_ImplGlfw_Shutdown();
    ImGui::DestroyContext();
}

int main()
{

    app = std::make_shared<GuiApp>(800, 600, "Test App");

    app->register_draw_callback(test_callback);

    app->register_terminate_callback(terminate_callback);

    app->start_app();
    
    return 0;

}