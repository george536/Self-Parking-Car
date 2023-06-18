from Carla_Controls.abstract_command import CMD
import carla

class ConnectToCarla(CMD):
    
    def execute(self):
        # Connect to the CARLA server
        client = carla.Client('localhost', 2000)
        client.set_timeout(25.0)
        return client
