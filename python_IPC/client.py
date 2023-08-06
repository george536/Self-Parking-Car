import grpc
import ipc_configs_pb2
import ipc_configs_pb2_grpc

def run():
    with open('image.jpg', 'rb') as f:
        image_data = f.read()

    channel = grpc.insecure_channel('localhost:50051')
    stub = ipc_configs_pb2_grpc.ImageTransferStub(channel)
    
    image_msg = ipc_configs_pb2.ImageData(image_data=image_data)
    response = stub.SendImage(image_msg)
    
    print(response.message)

if __name__ == '__main__':
    run()
