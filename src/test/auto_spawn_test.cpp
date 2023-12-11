#pragma once 
#define _WIN32_WINNT 0x0601

#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include <carla/geom/Location.h>
#include "../grpc_server/include/ipc_configs.pb.h"
#include "../auto_spawn_utils/include/auto_spawn.h"
#include "../utils/structs/GrpcData.h"

using namespace carla;
AutoSpawnUtils autoSpawnUtils;

TEST(AutoSpawnUtilsTest, FindGrpcDataWithClosestLocationTest) {
    geom::Location targetLocation;
    targetLocation.x = 10.0;
    targetLocation.y = 20.0;
    targetLocation.z = 30.0;

    GrpcData grpcData1;
    transform_request transform1;
    transform1.set_x(5.0);
    transform1.set_y(15.0);
    transform1.set_z(25.0);
    transform1.set_pitch(0.0);
    transform1.set_roll(0.0);
    transform1.set_yaw(0.0);
    grpcData1.transform = std::make_shared<transform_request>(transform1); 
    autoSpawnUtils.saveGrpcData(grpcData1);

    GrpcData grpcData2;
    transform_request transform2;
    transform2.set_x(12.0);
    transform2.set_y(22.0);
    transform2.set_z(32.0);
    transform2.set_pitch(0.0);
    transform2.set_roll(0.0);
    transform2.set_yaw(0.0);
    grpcData2.transform = std::make_shared<transform_request>(transform2); 
    autoSpawnUtils.saveGrpcData(grpcData2);

    GrpcData grpcData3;
    transform_request transform3;
    transform3.set_x(8.0);
    transform3.set_y(18.0);
    transform3.set_z(27.0);
    transform3.set_pitch(0.0);
    transform3.set_roll(0.0);
    transform3.set_yaw(0.0);
    grpcData3.transform = std::make_shared<transform_request>(transform3); 
    autoSpawnUtils.saveGrpcData(grpcData3);

    GrpcData* closestGrpcData = autoSpawnUtils.findGrpcDataWithClosestLocation(targetLocation);

    ASSERT_NE(closestGrpcData, nullptr);

    EXPECT_FLOAT_EQ(closestGrpcData->transform->x(), 12.0);
    EXPECT_FLOAT_EQ(closestGrpcData->transform->y(), 22.0);
    EXPECT_FLOAT_EQ(closestGrpcData->transform->z(), 32.0);
}

TEST(AutoSpawnUtilsTest, FindGrpcDataWithClosestLocationEmptyListTest) {
    autoSpawnUtils.grpcDataList.clear();
    
    geom::Location targetLocation;
    targetLocation.x = 10.0;
    targetLocation.y = 20.0;
    targetLocation.z = 30.0;

    GrpcData* closestGrpcData = autoSpawnUtils.findGrpcDataWithClosestLocation(targetLocation);

    ASSERT_EQ(closestGrpcData, nullptr);
}