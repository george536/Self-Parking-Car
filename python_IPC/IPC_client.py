from threading import Thread
from threading import Semaphore
import time

import grpc
from python_IPC.ipc_configs_pb2 import *
from python_IPC.ipc_configs_pb2_grpc import *

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
        print("GRPC client is initalized.")
        self.stub = image_transferStub(self.channel)
        self.image_data = None
        self.transform = None

    def set_image_data(self, image_data):
        self.image_data = image_data

    def set_transform(self, transform):
        self.transform = transform

    def get_semaphore(self):
        return IPC_client.semaphore

    def run(self):
        while True:
            IPC_client.semaphore.acquire()
            if(self.image_data == None or self.transform == None):
                return
            
            image_stub = image_request(data=self.image_data)
            car_location = location_request(
                x=self.transform.location.x, 
                y=self.transform.location.y, 
                z=self.transform.location.z, 
                pitch= self.transform.rotation.pitch,
                yaw= self.transform.rotation.yaw, 
                roll= self.transform.rotation.roll)  # Sample location values

            # Create request
            request = request_data(
                image_data=image_stub,
                car_location=car_location
            )

            # Make the gRPC call
            self.stub.send_data(request)

            time.sleep(0.1)
            IPC_client.semaphore.release()