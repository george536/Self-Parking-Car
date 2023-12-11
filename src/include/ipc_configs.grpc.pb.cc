// Generated by the gRPC C++ plugin.
// If you make any local change, they will be lost.
// source: ipc_configs.proto

#include "ipc_configs.pb.h"
#include "ipc_configs.grpc.pb.h"

#include <functional>
#include <grpcpp/support/async_stream.h>
#include <grpcpp/support/async_unary_call.h>
#include <grpcpp/impl/channel_interface.h>
#include <grpcpp/impl/client_unary_call.h>
#include <grpcpp/support/client_callback.h>
#include <grpcpp/support/message_allocator.h>
#include <grpcpp/support/method_handler.h>
#include <grpcpp/impl/rpc_service_method.h>
#include <grpcpp/support/server_callback.h>
#include <grpcpp/impl/server_callback_handlers.h>
#include <grpcpp/server_context.h>
#include <grpcpp/impl/service_type.h>
#include <grpcpp/support/sync_stream.h>

static const char* image_transfer_method_names[] = {
  "/image_transfer/send_data",
};

std::unique_ptr< image_transfer::Stub> image_transfer::NewStub(const std::shared_ptr< ::grpc::ChannelInterface>& channel, const ::grpc::StubOptions& options) {
  (void)options;
  std::unique_ptr< image_transfer::Stub> stub(new image_transfer::Stub(channel, options));
  return stub;
}

image_transfer::Stub::Stub(const std::shared_ptr< ::grpc::ChannelInterface>& channel, const ::grpc::StubOptions& options)
  : channel_(channel), rpcmethod_send_data_(image_transfer_method_names[0], options.suffix_for_stats(),::grpc::internal::RpcMethod::NORMAL_RPC, channel)
  {}

::grpc::Status image_transfer::Stub::send_data(::grpc::ClientContext* context, const ::request_data& request, ::empty_return* response) {
  return ::grpc::internal::BlockingUnaryCall< ::request_data, ::empty_return, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(channel_.get(), rpcmethod_send_data_, context, request, response);
}

void image_transfer::Stub::async::send_data(::grpc::ClientContext* context, const ::request_data* request, ::empty_return* response, std::function<void(::grpc::Status)> f) {
  ::grpc::internal::CallbackUnaryCall< ::request_data, ::empty_return, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(stub_->channel_.get(), stub_->rpcmethod_send_data_, context, request, response, std::move(f));
}

void image_transfer::Stub::async::send_data(::grpc::ClientContext* context, const ::request_data* request, ::empty_return* response, ::grpc::ClientUnaryReactor* reactor) {
  ::grpc::internal::ClientCallbackUnaryFactory::Create< ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(stub_->channel_.get(), stub_->rpcmethod_send_data_, context, request, response, reactor);
}

::grpc::ClientAsyncResponseReader< ::empty_return>* image_transfer::Stub::PrepareAsyncsend_dataRaw(::grpc::ClientContext* context, const ::request_data& request, ::grpc::CompletionQueue* cq) {
  return ::grpc::internal::ClientAsyncResponseReaderHelper::Create< ::empty_return, ::request_data, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(channel_.get(), cq, rpcmethod_send_data_, context, request);
}

::grpc::ClientAsyncResponseReader< ::empty_return>* image_transfer::Stub::Asyncsend_dataRaw(::grpc::ClientContext* context, const ::request_data& request, ::grpc::CompletionQueue* cq) {
  auto* result =
    this->PrepareAsyncsend_dataRaw(context, request, cq);
  result->StartCall();
  return result;
}

image_transfer::Service::Service() {
  AddMethod(new ::grpc::internal::RpcServiceMethod(
      image_transfer_method_names[0],
      ::grpc::internal::RpcMethod::NORMAL_RPC,
      new ::grpc::internal::RpcMethodHandler< image_transfer::Service, ::request_data, ::empty_return, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(
          [](image_transfer::Service* service,
             ::grpc::ServerContext* ctx,
             const ::request_data* req,
             ::empty_return* resp) {
               return service->send_data(ctx, req, resp);
             }, this)));
}

image_transfer::Service::~Service() {
}

::grpc::Status image_transfer::Service::send_data(::grpc::ServerContext* context, const ::request_data* request, ::empty_return* response) {
  (void) context;
  (void) request;
  (void) response;
  return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
}


