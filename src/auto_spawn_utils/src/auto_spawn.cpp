#pragma once 

#include "../include/auto_spawn.h"

namespace fs = std::filesystem;
using namespace std::chrono;
using namespace carla;

AutoSpawnUtils::AutoSpawnUtils() {
    carlaUtils.createCarlaClient();
    carlaUtils.connectToCarla();
    carlaUtils.extractVehicleFromWorld();
}

void AutoSpawnUtils::extractParkingLotCoordinates() {
    std::cout << "Extracting parking lot coordinates..." << std::endl;
    std::string projectPath = fs::current_path().string(); 
    char jsonFilePath[260];
    snprintf(jsonFilePath, sizeof(jsonFilePath), PARKING_LOT_COORDINATES_FILE, projectPath.c_str());
    nlohmann::json jsonData = fileutils.readJson(jsonFilePath);
    jsonData = jsonData[PARKING_LOT_COORDINATES_KEY];
    parkingLotBottomLeftCorner = geom::Location(jsonData[0][0], jsonData[0][1], jsonData[0][2]);
    parkingLotTopLeftCorner = geom::Location(jsonData[1][0], jsonData[1][1], jsonData[1][2]);
    parkingLotTopRightCorner = geom::Location(jsonData[2][0], jsonData[2][1], jsonData[2][2]);
    parkingLotBottomRightCorner = geom::Location(jsonData[3][0], jsonData[3][1], jsonData[3][2]);
}

void AutoSpawnUtils::saveGrpcData(GrpcData grpcData) {
    grpcDataList.push_back(grpcData);
}

GrpcData* AutoSpawnUtils::findClosestTransform(geom::Transform targetTransform) {
    GrpcData* closestGrpcData = nullptr;
    float closestDistance = std::numeric_limits<float>::max();

    for (auto& grpcData : grpcDataList) {
        if (grpcData.transform != nullptr) {
            float distance = std::abs(grpcData.transform->x() - targetTransform.location.x) +
                             std::abs(grpcData.transform->y() - targetTransform.location.y) +
                             std::abs(grpcData.transform->z() - targetTransform.location.z);

            if (distance < closestDistance) {
                closestDistance = distance;
                closestGrpcData = &grpcData;
            }
        }
    }
    if (closestGrpcData == nullptr) {
        std::cout << "Grpc data list is empty!! \n No data was recieved from server." << std::endl;
        std::cout << "Target Transform: (" << targetTransform.location.x << ", "
            << targetTransform.location.y << ", " << targetTransform.location.z << ")" << std::endl;

        exit(0);
    }
    return closestGrpcData;
}

void AutoSpawnUtils::processGrpcData(geom::Transform targetTransform) {
    GrpcData& matchingGrpcData = *findClosestTransform(targetTransform);
    if (&matchingGrpcData == nullptr) {
        std::cout << "No matching transform found." << std::endl;
        return;
    }
    grpcDataProcessor.convertAndSaveImage(matchingGrpcData.image->data());
    grpcDataProcessor.saveTransformData(*matchingGrpcData.transform);
}

void AutoSpawnUtils::waitForGrpcClient() {
    std::cout << "Waiting for grpc client..." << std::endl;
    while (grpcDataList.size() == 0) {
        std::this_thread::sleep_for (std::chrono::milliseconds(100));
    }
    std::cout << "Grpc client is connected." << std::endl;
}

void AutoSpawnUtils::spawnCarAtDifferentLocations() {
    std::cout << "Spawning car at different locations..." << std::endl;         
    collision = false;

    if (&carlaUtils.getVehicle() != nullptr && &carlaUtils.getWorld() != nullptr) {
        boost::shared_ptr<client::Sensor> sensor = carlaUtils.attachCollisionSensorToVehcile();

        sensor->Listen([this](auto data) {
            auto collision_data = boost::static_pointer_cast<const sensor::data::CollisionEvent>(data);
            collision = true;
            std::cout << "Collision detected. Failed to spawn the vehicle" << std::endl;
        });

        const std::function<void(GrpcData)>& callback = [=](GrpcData grpcData) { saveGrpcData(grpcData); };
        GrpcServer::callbackOnGrpcData(callback);

        waitForGrpcClient();
 
        for(float x=parkingLotBottomLeftCorner.x; x>=parkingLotTopLeftCorner.x; x--) {
            for(float y=parkingLotBottomLeftCorner.y; y>=parkingLotBottomRightCorner.y; y--) {
                geom::Location newLocation(x, y, 0.2f);
                for (float yaw=-180; yaw<=180; yaw+=10) {
                    geom::Rotation newRotation(0.0f, yaw, 0.0f);
                    geom::Transform newTransform(newLocation, newRotation);
                    carlaUtils.getVehicle()->SetTransform(newTransform);

                    carlaUtils.getWorld()->Tick(seconds(1));
                    std::this_thread::sleep_for (std::chrono::milliseconds(1000));

                    if (carlaUtils.getVehicle()->GetLocation().Distance(newLocation) <= 3.0f && !collision) {
                        std::cout << "Vehicle is spawned successfully into location x:" << x << ", y: "<< y<< std::endl;
                        processGrpcData(newTransform);
                        grpcDataList.clear();
                    }

                    collision = false;
                }
            }
        }
        sensor->Stop();  
        sensor->Destroy();
        GrpcServer::unsubscribeCallback(callback);
    }
}

void AutoSpawnUtils::startAutoSpawn() {
    AutoSpawnUtils autoSpawn;
    // pre-run
    autoSpawn.extractParkingLotCoordinates();

    // run
    autoSpawn.spawnCarAtDifferentLocations();
}