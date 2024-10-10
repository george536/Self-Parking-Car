from threading import Thread
from threading import Semaphore
import time

from grpc import RpcError
from grpc import insecure_channel
from grpc import StatusCode
from python_IPC.ipc_configs_pb2 import image_request
from python_IPC.ipc_configs_pb2 import transform_request
from python_IPC.ipc_configs_pb2 import BEV_bounding_box_cord_request
from python_IPC.ipc_configs_pb2 import request_data
from python_IPC.ipc_configs_pb2_grpc import image_transferStub

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
        self.BEV_bounding_box_cord = None

    def set_image_data(self, image_data):
        self.image_data = image_data

    def set_transform_data(self, transform):
        self.transform = transform

    def set_BEV_bounding_box_cord(self, BEV_bounding_box_cord):
        self.BEV_bounding_box_cord = BEV_bounding_box_cord

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
            BEV_bounding_box_cord_stub = BEV_bounding_box_cord_request(
                left_bottom_x = self.BEV_bounding_box_cord[0][0],
                left_bottom_y = self.BEV_bounding_box_cord[0][1],
                left_top_x = self.BEV_bounding_box_cord[1][0],
                left_top_y = self.BEV_bounding_box_cord[1][1],
                right_top_x = self.BEV_bounding_box_cord[2][0],
                right_top_y = self.BEV_bounding_box_cord[2][1],
                right_bottom_x = self.BEV_bounding_box_cord[3][0],
                right_bottom_y = self.BEV_bounding_box_cord[3][1]
            )

            try:
                # Create request
                request = request_data(
                    image_data=image_stub,
                    car_transform=car_transform,
                    BEV_bounding_box_cord=BEV_bounding_box_cord_stub
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
