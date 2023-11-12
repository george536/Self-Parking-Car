from threading import Semaphore

combined_surface = None
combined_surface_semaphore = Semaphore(1)

def get_combined_surface():
    return combined_surface

def set_combined_surface(surface):
    global combined_surface
    combined_surface = surface
