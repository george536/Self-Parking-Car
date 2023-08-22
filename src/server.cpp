#include <iostream>
#include <memory>
#include <string>
#include <vector>
#include <grpcpp/grpcpp.h>
#include <mutex>
#include "include/ipc_configs.pb.h" // Generated header from your proto file
#include "include/ipc_configs.grpc.pb.h" // Generated header from your proto file
#include "grpc_processing_utils/include/grpc_data_processor.h"

using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::Status;

class ImageTransferServiceImpl final : public image_transfer::Service {

    Status send_data(ServerContext* context, const request_data* request, empty_return* reply) override {
        // Process image and transform data here
        const image_request& image = request->image_data();
        const transform_request& transform = request->car_transform();

        std::cout<<"Client message recieved."<<std::endl;

        GrpcDataProcessor grpcDataProcessor;

        // Process image
        const char* byteList = grpcDataProcessor.convertToBytes(image.data());

        grpcDataProcessor.convertAndSaveImage(byteList);

        // Return a result
        reply->set_result(0); // You can set an appropriate result value
        
        return Status::OK;
    }
};

void RunServer() {
    std::string server_address("0.0.0.0:50051"); // Change to your desired address
    ImageTransferServiceImpl service;

    ServerBuilder builder;
    builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
    builder.RegisterService(&service);

    std::unique_ptr<Server> server(builder.BuildAndStart());
    std::cout << "Server listening on " << server_address << std::endl;
    server->Wait();
}

int main() {
    RunServer();
    return 0;
}
