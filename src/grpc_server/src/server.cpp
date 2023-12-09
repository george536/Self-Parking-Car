#include "../include/server.h"

using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::Status;

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

void ImageTransferServiceImpl::notifyGrpcDataListeners(const GrpcData& newData) {
    std::lock_guard<std::mutex> lock(callbacksMutex);
    for (const auto& callback : ImageTransferServiceImpl::getInstance().callbacks) {
        callback(newData);
    }
    std::cout << "callback size: " << ImageTransferServiceImpl::getInstance().callbacks.size() << std::endl;
}

void ImageTransferServiceImpl::callbackOnGrpcData(const std::function<void(GrpcData)>& callback) {
    std::lock_guard<std::mutex> lock(ImageTransferServiceImpl::getInstance().callbacksMutex);
    ImageTransferServiceImpl::getInstance().callbacks.push_back(callback);
    std::cout << "New callback registered." << std::endl;
}

void RunServer() {
    std::string server_address("0.0.0.0:50051"); // Change to your desired address

    ServerBuilder builder;
    builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
    builder.RegisterService(&ImageTransferServiceImpl::getInstance());

    std::unique_ptr<Server> server(builder.BuildAndStart());
    std::cout << "Server listening on " << server_address << std::endl;
    server->Wait();
}