#ifndef GRPC_DATA_H
#define GRPC_DATA_H

#include "../../grpc_server/include/ipc_configs.pb.h" // Generated header from your proto file
#include "../../grpc_server/include/ipc_configs.grpc.pb.h" // Generated header from your proto file

struct GrpcData {
    std::shared_ptr<image_request> image;
    std::shared_ptr<transform_request> transform;
};

#endif
