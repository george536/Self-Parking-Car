#ifndef IMAGE_DATA_TRANSFER_SERVICE_H
#define IMAGE_DATA_TRANSFER_SERVICE_H

#include <iostream>
#include <memory>
#include <string>
#include <vector>
#include <grpcpp/grpcpp.h>
#include <mutex>
#include "ipc_configs.pb.h" // Generated header from your proto file
#include "ipc_configs.grpc.pb.h" // Generated header from your proto file
#include "../../utils/structs/GrpcData.h"

class GrpcServer final : public image_transfer::Service {
public:
    static GrpcServer& getInstance() {
        static GrpcServer instance;
        return instance;
    }
    std::vector<std::function<void(GrpcData)>> callbacks;

    grpc::Status send_data(grpc::ServerContext* context, const request_data* request, empty_return* reply) override;
    void GrpcServer::notifyGrpcDataListeners(const GrpcData& newData);
    static void callbackOnGrpcData(const std::function<void(GrpcData)>& callback);
    static void unsubscribeCallback(const std::function<void(GrpcData)>& callbackToRemove) ;
    static void RunServer();

private:   
    std::mutex callbacksMutex;
    GrpcServer() {}
    GrpcServer(const GrpcServer&) = delete;
    GrpcServer& operator=(const GrpcServer&) = delete;
};

#endif