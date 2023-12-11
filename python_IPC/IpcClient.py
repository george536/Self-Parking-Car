from threading import Thread
from threading import Semaphore
import time

from grpc import RpcError
from grpc import insecure_channel
from grpc import StatusCode
from python_ipc.ipc_configs_pb2 import image_request
from python_ipc.ipc_configs_pb2 import transform_request
from python_ipc.ipc_configs_pb2 import request_data
from python_ipc.ipc_configs_pb2_grpc import image_transferStub

class IpcClient(Thread):
    """Responsible for sending images and transform data"""
    __instance = None
    semaphore1 = Semaphore(1)
    semaphore2 = Semaphore(0)

    @staticmethod
    def get_instance():
        """Static method to get the only single instance of this client"""
        return IpcClient.__instance

    def __init__(self):
        IpcClient.__instance = self
        super().__init__()
        self.channel = insecure_channel('localhost:50051')  # Update with your server address
        print("GRPC client is initalized.")
        self.stub = image_transferStub(self.channel)
        self.image_data = None
        self.transform = None

    def set_image_data(self, image_data):
        self.image_data = image_data

    def set_transform_data(self, transform):
        self.transform = transform

    def run(self):
        while True:
            IpcClient.semaphore2.acquire()

            if self.transform is None:
                continue

            image_stub = image_request(data=self.image_data)
            car_transform = transform_request(
                x=self.transform.location.x,
                y=self.transform.location.y,
                z=self.transform.location.z,
                pitch= self.transform.rotation.pitch,
                yaw= self.transform.rotation.yaw,
                roll= self.transform.rotation.roll)

            try:
                # Create request
                request = request_data(
                    image_data=image_stub,
                    car_transform=car_transform
                )

                # Make the gRPC call
                self.stub.send_data(request)

            except RpcError as e:
                # Handle gRPC errors
                print('Error:', e.details())
                if e.code() == StatusCode.UNKNOWN:
                    print('Unknown error occurred')
                elif e.code() == StatusCode.INVALID_ARGUMENT:
                    print('Invalid argument provided')
                # Handle more error codes as needed

            time.sleep(0.1)
            IpcClient.semaphore1.release()
