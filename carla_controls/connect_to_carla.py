from carla import Cleint

from carla_controls.abstract_command import CMD

class ConnectToCarla(CMD):
    """Establish Carla connection"""
    def execute(self, town = 'Town05'):
        # Connect to the CARLA server
        client = Client('localhost', 2000)
        client.set_timeout(50.0)
        client.load_world(town)
        return client
