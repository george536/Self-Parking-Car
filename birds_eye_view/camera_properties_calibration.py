import tkinter as tk
import json
from threading import Thread

class CameraPropertiesCalibration(Thread):
    __instance = None

    def __init__(self):
        super().__init__()
        if CameraPropertiesCalibration.__instance is None:
            CameraPropertiesCalibration.__instance = self
            self.camera_locations = None
            self.load_json_data()
            self.root = tk.Tk()
            self.root.title("Camera Properties Calibration")
            self.root.resizable(True, True)

    @staticmethod
    def get_instance():
        if CameraPropertiesCalibration.__instance == None:
            CameraPropertiesCalibration()
        return CameraPropertiesCalibration.__instance

    def load_json_data(self):
        print("loading camera locations configurations..")
        # Load camera locations from JSON file
        with open('birds_eye_view/camera_locations.json') as config_file:
            self.camera_locations = json.load(config_file)

    def get_camera_locations_dictionary(self):
        return self.camera_locations
    
    def generate_fields(self, camera):
        return [
            ("x",camera.get_x(), camera.set_x, -50, 50, 0.1),
            ("y",camera.get_y(), camera.set_y, -50, 50, 0.1),
            ("z",camera.get_z(), camera.set_z, -50, 50, 0.1),
            ("pitch",camera.get_pitch(), camera.set_pitch, -50, 50, 0.1),
            ("yaw",camera.get_yaw(), camera.set_yaw, -50, 50, 0.1),
            ("roll",camera.get_roll(), camera.set_roll, -50, 50, 0.1)
        ]
    
    def add_camera(self, camera):
        fields = self.generate_fields(camera)

        for i, (label, value, command, from_val, to_val, step) in enumerate(fields):
            var = tk.DoubleVar(value=value)
            slider = tk.Scale(
                self.root,
                from_=from_val,
                to=to_val,
                length=500,
                resolution=step,
                variable=var,
                label=str(camera.location.name) + label,
                command=command,
                orient="horizontal"
            )
            slider.set(value)
            slider.grid(row=i//2, column=i%2)

    def run(self):

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

        self.root.mainloop()


