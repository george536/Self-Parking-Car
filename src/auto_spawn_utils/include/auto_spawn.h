#ifndef AUTO_SPAWN_UTILS
#define AUTO_SPAWN_UTILS
#define _WIN32_WINNT 0x0601

#include <iostream>
#include <filesystem>
#include <thread>
#include <chrono>
#include <cstdlib>
#include <memory>
#include <Time.h>
#include <vector>
#include <carla/client/Client.h>
#include <carla/client/World.h>
#include <carla/client/ActorList.h>
#include <carla/client/Actor.h>
#include <carla/client/Sensor.h>
#include <carla/client/BlueprintLibrary.h>
#include <carla/geom/Location.h>
#include <carla/geom/Transform.h>
#include <carla/geom/Vector3D.h>
#include <carla/geom/Rotation.h>
#include <carla/sensor/data/CollisionEvent.h>
#include <boost/shared_ptr.hpp>

#include "file_utils.h"
#include "../../grpc_processing_utils/include/grpc_data_processor.h"
#include "../../grpc_server/include/server.h"

class AutoSpawnUtils {
    public:
    AutoSpawnUtils();
    const char* PARKING_LOT_COORDINATES_FILE = "%s\\parking_spot_labeller\\spots_data.json";
    const char* PARKING_LOT_COORDINATES_KEY = "parking lot";
    bool collision = false;
    FileUtils fileutils;
    std::vector<GrpcData> grpcDataList;
    GrpcDataProcessor grpcDataProcessor;
    
    carla::geom::Location parkingLotBottomLeftCorner;
    carla::geom::Location parkingLotTopRightCorner;
    carla::geom::Location parkingLotBottomRightCorner;
    carla::geom::Location parkingLotTopLeftCorner;

    std::shared_ptr<carla::client::Client> client_ptr;
    std::shared_ptr<carla::client::World> world_ptr;
    boost::shared_ptr<carla::client::Actor> vehicle_ptr;

    void connectToCarla();
    void extractVehicleFromWorld();
    void extractParkingLotCoordinates();
    void saveGrpcData(GrpcData grpcData);
    void processGrpcData(carla::geom::Transform targetTransform);
    GrpcData* findClosesTransform(carla::geom::Transform targetTransform);
    void spawnCarAtDifferentLocations();
    void run();
};

#endif