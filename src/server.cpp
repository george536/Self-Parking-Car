#include <iostream>
#include <memory>
#include <string>
#include <grpcpp/grpcpp.h>
#include "include/ipc_configs.pb.h" // Generated header from your proto file
#include "include/ipc_configs.grpc.pb.h" // Generated header from your proto file

using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::Status;

class ImageTransferServiceImpl final : public image_transfer::Service {
    Status send_data(ServerContext* context, const request_data* request, empty_return* reply) override {
        // Process image and location data here
        const image_request& image = request->image_data();
        const location_request& location = request->car_location();

        // Do something with image.data(), location.x(), location.y(), etc.

        std::cout<<location.x()<<std::endl;

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
    printf("hello world");
    return 0;
}