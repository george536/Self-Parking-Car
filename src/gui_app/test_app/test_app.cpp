#include "gui_app.h"

int main()
{
    GuiApp app(800, 600, "Test App");

    app.start_app();

    while(true)
    {
        // do something
    }

    return 0;

}