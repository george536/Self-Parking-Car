#include "../include/carla_utils.h"

using namespace carla;
using namespace std::chrono;

void CarlaUtils::createCarlaClient() {
    std::cout << "Initalizing Carla client..." << std::endl;
    client_ptr = std::make_shared<carla::client::Client>("localhost", 2000);
}

void CarlaUtils::connectToCarla() {
    std::cout << "Connecting to Carla..." << std::endl;
    client_ptr->SetTimeout(seconds(50));
    world_ptr = std::make_shared<carla::client::World>(client_ptr->GetWorld());
    std::cout << "Connected to Carla." << std::endl;
}

void CarlaUtils::extractVehicleFromWorld() {
    std::cout << "Extracting vehicle ..." << std::endl;
    auto vehicles = world_ptr->GetActors()->Filter("vehicle.*");
    if (!vehicles->empty()) {
        vehicle_ptr = vehicles->at(0);
    } else {
        std::cout << "No vehicles found." << std::endl;
        exit(EXIT_FAILURE);
    }
}

boost::shared_ptr<carla::client::Actor> CarlaUtils::getVehicle() {
    return vehicle_ptr;
}

std::shared_ptr<carla::client::World> CarlaUtils::getWorld() {
    return world_ptr;
}

std::shared_ptr<carla::client::Client> CarlaUtils::getClient() {
    return client_ptr;
}

boost::shared_ptr<carla::client::Sensor> CarlaUtils::attachCollisionSensorToVehcile() {
    auto sensor_blueprints = world_ptr->GetBlueprintLibrary();     
    auto sensor_blueprint = (*(sensor_blueprints->Filter("sensor.other.collision")))[0];  

    auto sensor_transform = carla::geom::Transform(carla::geom::Location(0, 0, 0));
    auto sensor = boost::static_pointer_cast<carla::client::Sensor>(world_ptr->SpawnActor(sensor_blueprint, sensor_transform, vehicle_ptr.get()));

    return sensor;
}