from carla_controls.abstract_command import CMD
import carla

class ConnectToCarla(CMD):
    
    def execute(self):
        # Connect to the CARLA server
        client = carla.Client('localhost', 2000)
        client.set_timeout(50.0)
        current_world = client.get_world()
        if current_world.get_map().name != 'Carla/Maps/Town05':
            client.load_world('Town05')
        return client
