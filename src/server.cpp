#include <iostream>
#include <string>
#include <memory>
#include <grpcpp/grpcpp.h>
#include "image.grpc.pb.h"

using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::Status;
using image_transfer::ImageData;
using image_transfer::ImageTransfer;

class ImageTransferServiceImpl final : public ImageTransfer::Service {
    Status SendImage(ServerContext* context, const ImageData* request, ImageTransfer::ImageResponse* response) override {
        std::ofstream image_file("received_image.jpg", std::ios::binary);
        if (image_file.is_open()) {
            image_file.write(request->image_data().data(), request->image_data().size());
            image_file.close();
            response->set_message("Image received successfully.");
        } else {
            response->set_message("Failed to save the received image.");
        }
        return Status::OK;
    }
};

void RunServer() {
    std::string server_address("0.0.0.0:50051");
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
