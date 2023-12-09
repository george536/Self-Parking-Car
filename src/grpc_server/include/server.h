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

class ImageTransferServiceImpl final : public image_transfer::Service {
public:
    static std::vector<std::function<void(GrpcData)>> callbacks;

    grpc::Status send_data(grpc::ServerContext* context, const request_data* request, empty_return* reply) override;
    static void callbackOnGrpcData(const std::function<void(GrpcData)>& callback);
    void ImageTransferServiceImpl::notifyGrpcDataListeners(const GrpcData& newData);
};

#endif