#include "../include/server.h"

using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::Status;

std::vector<std::function<void(GrpcData)>> ImageTransferServiceImpl::callbacks;

Status ImageTransferServiceImpl::send_data(ServerContext* context, const request_data* request, empty_return* reply) {
    const image_request& image = request->image_data();
    const transform_request& transform = request->car_transform();

    std::cout << "Client message received." << std::endl;

    GrpcData newData;
    newData.image = std::make_shared<image_request>(image);
    newData.transform = std::make_shared<transform_request>(transform); 

    notifyGrpcDataListeners(newData);

    // Return a result
    reply->set_result(0); // You can set an appropriate result value

    return Status::OK;
}

void ImageTransferServiceImpl::callbackOnGrpcData(const std::function<void(GrpcData)>& callback) {
    ImageTransferServiceImpl::callbacks.push_back(callback);
}

void ImageTransferServiceImpl::notifyGrpcDataListeners(const GrpcData& newData) {
    for (const auto& callback : callbacks) {
        callback(newData);
    }
}

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