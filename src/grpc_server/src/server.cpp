#include "../include/server.h"

using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::Status;

Status GrpcServer::send_data(ServerContext* context, const request_data* request, empty_return* reply) {
    const image_request& image = request->image_data();
    const transform_request& transform = request->car_transform();
    const BEV_bounding_box_cord_request& BEV_bounding_box_cord = request->bev_bounding_box_cord();

    std::cout << "Client message received." << std::endl;

    GrpcData newData;
    newData.image = std::make_shared<image_request>(image);
    newData.transform = std::make_shared<transform_request>(transform); 
    newData.BEV_bounding_box_cord = std::make_shared<BEV_bounding_box_cord_request>(BEV_bounding_box_cord); 

    notifyGrpcDataListeners(newData);

    // Return a result
    reply->set_result(0); // You can set an appropriate result value

    return Status::OK;
}

void GrpcServer::notifyGrpcDataListeners(const GrpcData& newData) {
    std::lock_guard<std::mutex> lock(callbacksMutex);
    for (const auto& callback : callbacks) {
        callback(newData);
    }
}

void GrpcServer::callbackOnGrpcData(const std::function<void(GrpcData)>& callback) {
    std::lock_guard<std::mutex> lock(GrpcServer::getInstance().callbacksMutex);
    GrpcServer::getInstance().callbacks.push_back(callback);
    std::cout << "New callback registered." << std::endl;
}

void GrpcServer::unsubscribeCallback(const std::function<void(GrpcData)>& callbackToRemove) {
    std::lock_guard<std::mutex> lock(GrpcServer::getInstance().callbacksMutex);
    auto& callbacks = GrpcServer::getInstance().callbacks;

    auto it = std::remove_if(callbacks.begin(), callbacks.end(),
                             [&callbackToRemove](const auto& callback) {
                                 return callback.target_type() == callbackToRemove.target_type();
                             });
    if (it != callbacks.end()) {
        callbacks.erase(it, callbacks.end());
        std::cout << "Callback unsubscribed." << std::endl;
    } else {
        std::cout << "Callback not found." << std::endl;
    }
}

void GrpcServer::RunServer() {
    std::string server_address("0.0.0.0:50051"); // Change to your desired address

    ServerBuilder builder;
    builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
    builder.RegisterService(&GrpcServer::getInstance());

    std::unique_ptr<Server> server(builder.BuildAndStart());
    std::cout << "Server listening on " << server_address << std::endl;
    server->Wait();
}