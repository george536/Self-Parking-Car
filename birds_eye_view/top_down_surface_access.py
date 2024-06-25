from threading import Semaphore

top_down_surface = None
top_down_surface_semaphore = Semaphore(1)

def get_top_down_surface():
    return top_down_surface

def set_top_down_surface(surface):
    global top_down_surface
    top_down_surface = surface
