from carla_controls.abstract_command import CMD
import carla

class ConnectToCarla(CMD):
    
    def execute(self, town = 'Town05'):
        # Connect to the CARLA server
        client = carla.Client('localhost', 2000)
        client.set_timeout(50.0)
        client.load_world(town)
        return client
