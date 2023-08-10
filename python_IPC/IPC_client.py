from threading import Thread
from threading import Semaphore
import time

import grpc
import ipc_configs_pb2
import ipc_configs_pb2_grpc

class IPC_client(Thread):

    __instance = None
    semaphore = Semaphore(1)

    @staticmethod
    def get_instance():
        return IPC_client.__instance

    def __init__(self):
        IPC_client.__instance = self
        super().__init__()
        self.channel = grpc.insecure_channel('localhost:50051')  # Update with your server address
        self.stub = ipc_configs_pb2_grpc.image_transferStub(self.channel)
        self.image_data = None
        self.location = None

    def set_image_data(self, image_data):
        self.image_data = image_data

    def set_location(self, location):
        self.location = location

    def get_semaphore(self):
        return IPC_client.semaphore

    def run(self):
        while True:
            IPC_client.semaphore.acquire()
            if(self.image_data == None or self.location == None):
                return
            
            image_stub = ipc_configs_pb2.image_request(data=self.image_data)
            car_location = ipc_configs_pb2.location_request(
                x=self.location.transform.x, 
                y=self.location.transform.y, 
                z=self.location.transform.z, 
                pitch= self.location.rotation.pitch,
                yaw= self.location.rotation.yaw, 
                roll= self.location.rotation.roll)  # Sample location values

            # Create request
            request = ipc_configs_pb2.request_data(
                image_data=image_stub,
                car_location=car_location
            )

            # Make the gRPC call
            self.stub.send_data(request)

            time.sleep(0.1)
            IPC_client.semaphore.release()