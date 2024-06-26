import tkinter as tk
import json
from threading import Thread
import atexit

class CameraPropertiesCalibration(Thread):
    __instance = None

    def __init__(self):
        if CameraPropertiesCalibration.__instance is None:
            super().__init__()
            CameraPropertiesCalibration.__instance = self
            self.camera_locations = None
            self.cameras = []
            self.load_json_data()
            self.root = None

    @staticmethod
    def get_instance():
        if CameraPropertiesCalibration.__instance is None:
            CameraPropertiesCalibration()
        return CameraPropertiesCalibration.__instance

    def load_json_data(self):
        print("loading camera locations configurations..")
        # Load camera locations from JSON file
        with open('birds_eye_view/camera_locations.json', encoding="utf-8") as config_file:
            self.camera_locations = json.load(config_file)

    def save_camera_properties(self):
        for camera in self.cameras:
            self.camera_locations[camera.location.name]["x"] = float(camera.get_x())
            self.camera_locations[camera.location.name]["y"] = float(camera.get_y())
            self.camera_locations[camera.location.name]["z"] = float(camera.get_z())
            self.camera_locations[camera.location.name]["pitch"] = float(camera.get_pitch())
            self.camera_locations[camera.location.name]["yaw"] = float(camera.get_yaw())
            self.camera_locations[camera.location.name]["roll"] = float(camera.get_roll())

        print("Saving camera properties configurations")

        with open('birds_eye_view/camera_locations.json', 'w', encoding="utf-8") as config_file:
            json.dump(self.camera_locations, config_file, indent=4)

    def get_camera_locations_dictionary(self):
        return self.camera_locations

    def generate_fields(self, camera):
        return [
            ("x",camera.get_x(), camera.set_x, -50, 50, 0.1),
            ("y",camera.get_y(), camera.set_y, -50, 50, 0.1),
            ("z",camera.get_z(), camera.set_z, -50, 50, 0.1),
            ("pitch",camera.get_pitch(), camera.set_pitch, -360, 360, 1),
            ("yaw",camera.get_yaw(), camera.set_yaw, -360, 360, 1),
            ("roll",camera.get_roll(), camera.set_roll, -360, 360, 1)
        ]

    def add_camera(self, camera):
        self.cameras.append(camera)

    def run(self):
        self.root = tk.Tk()
        self.root.title("Camera Properties Calibration")
        self.root.resizable(True, True)

        count = 0

        for camera in self.cameras:
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
                    label=str(camera.location.name) + " " + label,
                    command=command,
                    orient="horizontal"
                )
                slider.set(value)
                slider.grid(row=(i+count)//2, column=(i+count)%2)


            count+=len(fields)

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

        self.root.mainloop()


atexit.register(CameraPropertiesCalibration.get_instance().save_camera_properties)
