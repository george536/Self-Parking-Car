import json
import pygame

from carla_controls.connect_to_carla import ConnectToCarla
from carla_controls.add_labeller_camera import LabellerCamera
from parking_spot_labeller.utils_labeller import get_3d_points
from parking_spot_labeller.utils_labeller import PARKING_SPOTS_FILE_PATH
from parking_spot_labeller.utils_labeller import load_parking_spots
from parking_spot_labeller.utils_labeller import draw_bounding_box

from carla import Location
from pygame import K_BACKSPACE
from pygame import KEYDOWN
from pygame import MOUSEBUTTONUP
from pygame import QUIT

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FOV = 110

class ParkingSpotLabeller:
    """Starts a GUI for adding parking spots"""
    def __init__(self):
        pygame.init()
        window_width, window_height = 1280, 720
        self.screen = pygame.display.set_mode([window_width, window_height])
        self.button_width = 200
        self.button_height = 50
        self.button_x = window_width - self.button_width
        self.button_y = self.button_height // 2
        self.button_color = (0, 255, 0)  # Green color
        button_text = "Save spot"
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.text = self.font.render(button_text, True, (0, 0, 0))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (self.button_x + self.button_width // 2,
                                  self.button_y + self.button_height // 2)
        self.spot_id_oinput_box_text = ""
        self.id_field_font = pygame.font.SysFont(None, 100)

        self.running = True
        self.client = ConnectToCarla().execute()

        self.world = self.client.get_world()
        self.camera = LabellerCamera(self.world, width=WINDOW_WIDTH, height=WINDOW_HEIGHT,
                                      fov=FOV, camera_type="rgb").execute()
        self.depth_camera = LabellerCamera(self.world, width=WINDOW_WIDTH, height=WINDOW_HEIGHT,
                                      fov=FOV, camera_type="depth").execute()
        self.draw_debug_points = []

    def is_save_spot_button_clicked(self, mouse_pos):
        """Checks for save button clicks"""
        if self.button_x <= mouse_pos[0] <= self.button_x + self.button_width and \
        self.button_y <= mouse_pos[1] <= self.button_y + self.button_height:
            return True
        return False

    # write function that saves to json file these data as map
    def save_spot(self, spot_id, spot_corners_list):
        """Saves spots data to json file"""
        try:
            # Check if the file exists
            with open(PARKING_SPOTS_FILE_PATH, "r", encoding="utf-8") as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            # If the file doesn't exist, create an empty dictionary
            data = {}

        # Update or add the spot data in the dictionary
        data[spot_id] = spot_corners_list

        # Convert the data to JSON format
        json_data = json.dumps(data, indent=4)

        # Write the JSON data to the file
        with open(PARKING_SPOTS_FILE_PATH, "w", encoding="utf-8") as json_file:
            json_file.write(json_data)

        print(f"Spot with id: {spot_id} has been saved.")

        draw_bounding_box(self.world, spot_corners_list)

    def destroy_cameras(self):
        """Delete all added cameras"""
        self.camera.camera_actor.destroy()
        self.depth_camera.camera_actor.destroy()

    def process_events(self, event):
        """Process all pygame events"""
        if event.type == MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if self.is_save_spot_button_clicked(mouse_pos):
                self.save_spot(self.spot_id_oinput_box_text,self.draw_debug_points[-4:])
                self.spot_id_oinput_box_text = ""

            else:
                self.draw_debug_points.append(get_3d_points(self.camera, self.depth_camera))
                self.world.debug.draw_point(Location(x=self.draw_debug_points[-1][0],
                                                        y=self.draw_debug_points[-1][1],
                                                        z=self.draw_debug_points[-1][2]),
                                                        size=0.1, life_time=1000)

        if event.type == QUIT:
            self.running = False

        if event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                self.spot_id_oinput_box_text =  self.spot_id_oinput_box_text[:-1]
            else:
                self.spot_id_oinput_box_text += event.unicode

    def run(self):
        """Starts the GUI thread"""
        load_parking_spots(world=self.world)
        while self.running:
            for event in pygame.event.get():
                self.process_events(event)

            if self.camera.pygame_surface is not None:
                self.screen.blit(self.camera.pygame_surface, (0, 0))
            else:
                self.screen.fill([255, 255, 255])

            pygame.draw.rect(self.screen, self.button_color,
                             (self.button_x, self.button_y, self.button_width, self.button_height))
            self.screen.blit(self.text, self.text_rect)
            text_surf = self.id_field_font.render(self.spot_id_oinput_box_text, True, (255, 0, 0))
            self.screen.blit(text_surf, text_surf.get_rect(center = self.screen.get_rect().center))

            pygame.display.flip()

        self.destroy_cameras()
        pygame.quit()
