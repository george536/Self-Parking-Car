from threading import Semaphore, Event

combined_surface = None
combined_surface_semaphore = Semaphore(1)
composition_event = Event()
image_sync_preserving_semaphores = [Semaphore(0) for _ in range(4)]
cameras_waiting_states = [False, False, False, False]

def get_combined_surface():
    return combined_surface

def set_combined_surface(surface):
    global combined_surface
    combined_surface = surface
