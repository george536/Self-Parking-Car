from carla_controls.abstract_command import CMD
import carla

class AddVehicle(CMD):
        def __init__(self, world, spawn_point):
            self.world = world
            self.spawn_point = spawn_point
        
        def execute(self):
            blueprint_library = self.world.get_blueprint_library()
            vehicle_bp = blueprint_library.filter('vehicle.dodge.charger_police_2020')[0]
            # Spawn the vehicle at a given location
            vehicle = self.world.spawn_actor(vehicle_bp, self.spawn_point, attach_to=None)
            vehicle.apply_control(carla.VehicleControl(brake=1.0, steer=0.0))
            return vehicle