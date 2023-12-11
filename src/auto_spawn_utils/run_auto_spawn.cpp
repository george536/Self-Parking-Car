#include <thread>

#include "src/auto_spawn.cpp"
#include "../grpc_server/include/server.h"

int main() {
    std::thread autoSpawnThread(AutoSpawnUtils::startAutoSpawn);
    std::thread serverThread(GrpcServer::RunServer);

    autoSpawnThread.join();
    serverThread.join();

    return 0;
}
