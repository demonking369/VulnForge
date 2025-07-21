#include <X11/Xlib.h>
#include <X11/extensions/XTest.h>
#include <unistd.h>

extern "C" {
    // Moves the mouse pointer to the specified X and Y coordinates.
    void move_mouse_cpp(int x, int y) {
        Display* display = XOpenDisplay(NULL);
        if (display == NULL) return;

        XWarpPointer(display, None, DefaultRootWindow(display), 0, 0, 0, 0, x, y);
        XFlush(display);
        XCloseDisplay(display);
    }
} 