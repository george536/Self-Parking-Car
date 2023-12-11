#ifndef CARLA_UTILS
#define CARLA_UTILS
#define _WIN32_WINNT 0x0601

#include <chrono>
#include <boost/shared_ptr.hpp>
#include <carla/client/Client.h>
#include <carla/client/World.h>
#include <carla/client/ActorList.h>
#include <carla/client/Actor.h>
#include <carla/sensor/data/CollisionEvent.h>
#include <carla/client/BlueprintLibrary.h>
#include <carla/client/Sensor.h>

class CarlaUtils {
public:
    void createCarlaClient();
    std::shared_ptr<carla::client::Client> getClient();
    std::shared_ptr<carla::client::World> getWorld();
    boost::shared_ptr<carla::client::Actor> getVehicle();
    void connectToCarla();
    void extractVehicleFromWorld();
    boost::shared_ptr<carla::client::Sensor> attachCollisionSensorToVehcile();

private:
    std::shared_ptr<carla::client::Client> client_ptr;
    std::shared_ptr<carla::client::World> world_ptr;
    boost::shared_ptr<carla::client::Actor> vehicle_ptr;
};

#endif