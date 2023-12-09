#pragma once 

#include "include/auto_spawn.h"

namespace fs = std::filesystem;
using namespace std::chrono;
using namespace carla;

AutoSpawnUtils::AutoSpawnUtils() {
    client_ptr = std::make_shared<carla::client::Client>("localhost", 2000);
}

void AutoSpawnUtils::connectToCarla() {
    std::cout << "Connecting to Carla..." << std::endl;
    client_ptr->SetTimeout(seconds(50));
    world_ptr = std::make_shared<carla::client::World>(client_ptr->GetWorld());
    std::cout << "Connected to Carla." << std::endl;
}

void AutoSpawnUtils::extractVehicleFromWorld() {
    std::cout << "Extracting vehicle ..." << std::endl;
    auto vehicles = world_ptr->GetActors()->Filter("vehicle.*");
    if (!vehicles->empty()) {
        vehicle_ptr = vehicles->at(0);
    } else {
        std::cout << "No vehicles found." << std::endl;
        exit(EXIT_FAILURE);
    }
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

GrpcData* AutoSpawnUtils::findClosesTransform(geom::Transform targetTransform) {
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
    }
    return closestGrpcData;
}

void AutoSpawnUtils::processGrpcData(geom::Transform targetTransform) {
    GrpcData& matchingGrpcData = *findClosesTransform(targetTransform);
    if (&matchingGrpcData == nullptr) {
        std::cout << "No matching transform found." << std::endl;
        return;
    }
    grpcDataProcessor.convertAndSaveImage(matchingGrpcData.image->data());
    grpcDataProcessor.saveTransformData(*matchingGrpcData.transform);
}

void AutoSpawnUtils::spawnCarAtDifferentLocations() {
    std::cout << "Spawning car at different locations..." << std::endl;  
    auto sensor_blueprints = world_ptr->GetBlueprintLibrary();     
    auto sensor_blueprint = (*(sensor_blueprints->Filter("sensor.other.collision")))[0];        
    collision = false;

    if (&vehicle_ptr != nullptr && &world_ptr != nullptr && &sensor_blueprint != nullptr) {
        auto sensor_transform = carla::geom::Transform(carla::geom::Location(0, 0, 0));
        auto sensor = boost::static_pointer_cast<carla::client::Sensor>(world_ptr->SpawnActor(sensor_blueprint, sensor_transform, vehicle_ptr.get()));

        sensor->Listen([this](auto data) {
            auto collision_data = boost::static_pointer_cast<const carla::sensor::data::CollisionEvent>(data);
            collision = true;
            std::cout << "Collision detected. Failed to spawn the vehicle" << std::endl;
        });

        ImageTransferServiceImpl::callbackOnGrpcData([=](GrpcData grpcData) { saveGrpcData(grpcData); });

        for(float x=parkingLotBottomLeftCorner.x; x>=parkingLotTopLeftCorner.x; x--) {
            for(float y=parkingLotBottomLeftCorner.y; y>=parkingLotBottomRightCorner.y; y--) {
                geom::Location newLocation(x, y, 2.0f);
                //for (float i=-180; i<=180; i+=10) {
                    geom::Rotation newRotation(0.0f, 0.0f, 0.0f);
                    geom::Transform newTransform(newLocation, newRotation);
                    vehicle_ptr->SetTransform(newTransform);

                    world_ptr->Tick(seconds(1));
                    std::this_thread::sleep_for (std::chrono::milliseconds(1000));

                    if (vehicle_ptr->GetLocation().Distance(newLocation) <= 5.0f && !collision) {
                        std::cout << "Vehicle is spawned successfully into location x:" << x << ", y: "<< y<< std::endl;
                        processGrpcData(newTransform);
                        grpcDataList.clear();
                    }

                    collision = false;
                //}
            }
        }
        sensor->Stop();  
        sensor->Destroy();
        // unsubscribe from callback
    }
}

void AutoSpawnUtils::run() {
    // pre-run sets
    connectToCarla();
    extractVehicleFromWorld();
    extractParkingLotCoordinates();

    // run
    spawnCarAtDifferentLocations();
}

int main() {
    AutoSpawnUtils autoSpawn;
    autoSpawn.run();
    return 0;
}