#ifndef auto_spawn_utils
#define auto_spawn_utils

#include <iostream>
#include <filesystem>
#include <chrono>
#include <Time.h>
#include <cstdlib>
#include <carla/client/Client.h>
#include <carla/client/World.h>
#include <carla/client/ActorList.h>
#include <carla/client/Actor.h>
#include <carla/geom/Location.h>
#include <carla/geom/Transform.h>
#include <carla/geom/Vector3D.h>
#include <carla/geom/Rotation.h>

#include "file_utils.h"

class AutoSpawnUtils {
    public:
    const char* PARKING_LOT_COORDINATES_FILE = "%s\\parking_spot_labeller\\spots_data.json";
    const char* PARKING_LOT_COORDINATES_KEY = "parking lot";
    FileUtils fileutils;
    carla::geom::Location parkingLotBottomLeftCorner;
    carla::geom::Location parkingLotTopRightCorner;
    carla::geom::Location parkingLotBottomRightCorner;
    carla::geom::Location parkingLotTopLeftCorner;

    carla::client::Client client;
    carla::client::World world;
    carla::client::Actor vehicle;

    void connectToCarla();
    void extractVehicleFromWorld();
    void extractParkingLotCoordinates();
    void spawnCarAtDifferentLocations();
    void run();
};

#endif