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

    char jsonFilePath[260];
    snprintf(jsonFilePath, sizeof(jsonFilePath), PARKING_LOT_COORDINATES_FILE, fs::current_path().c_str());
    nlohmann::json jsonData = fileutils.readJson(jsonFilePath);
    jsonData = jsonData[PARKING_LOT_COORDINATES_KEY];
    parkingLotBottomLeftCorner = geom::Location(jsonData[0][0], jsonData[0][1], jsonData[0][2]);
    parkingLotTopLeftCorner = geom::Location(jsonData[1][0], jsonData[1][1], jsonData[1][2]);
    parkingLotTopRightCorner = geom::Location(jsonData[2][0], jsonData[2][1], jsonData[2][2]);
    parkingLotBottomRightCorner = geom::Location(jsonData[3][0], jsonData[3][1], jsonData[3][2]);
}

void AutoSpawnUtils::spawnCarAtDifferentLocations() {
    std::cout << "Spawning car at different locations..." << std::endl;
    for(float x=parkingLotBottomLeftCorner.x; x>=parkingLotTopLeftCorner.x; x--) {
        for(float y=parkingLotBottomLeftCorner.y; y>=parkingLotBottomRightCorner.y; y--) {
            // Define the new location and rotation for the vehicle.
            geom::Location newLocation(x, y, 2.0f);
            for (float i=-180; i<=180; i++) {
                geom::Rotation newRotation(0.0f, i, 0.0f);
                
                if (&vehicle_ptr != nullptr) {
                    // Set the new transform for the vehicle.
                    geom::Transform NewTransform(newLocation, newRotation);
                    vehicle_ptr->SetTransform(NewTransform);

                    // Check for collisions or failures.
                    world_ptr->Tick(seconds(1));
                    if (vehicle_ptr->GetLocation().Distance(newLocation) <= 1.0f) {
                        // release server semaphore to save picture
                    } else {
                        std::cout << "EVehicle is not at rest, collision detected!" << std::endl;
                    }
                }
            }
            
        }
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
    // No need to delete; the destructor will be called automatically when autoSpawn goes out of scope
    return 0;
}