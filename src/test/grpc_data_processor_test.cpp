#pragma once 
#include <gtest/gtest.h>
#include <gmock/gmock.h>

#include "opencv2/opencv.hpp"
#include "../grpc_processing_utils/include/grpc_data_processor.h"
#include "../utils/file_utils/include/file_utils.h"


using ::testing::NiceMock;

FileUtils fileutils;
GrpcDataProcessor processor;

class MockFileUtils : public FileUtils {
public:
    MOCK_METHOD(nlohmann::json, readJson, (const char* jsonFilePath));
};

class GrpcDataProcessorTest : public ::testing::Test {
protected:
    NiceMock<MockFileUtils> mockFileUtils;

    void SetUp() override {
        ON_CALL(mockFileUtils, readJson).WillByDefault([](const char* jsonFilePath) {
            FileUtils realFileUtils;
            return realFileUtils.readJson(jsonFilePath);
        });
    }
};

bool createEmptyJsonFileIfNeeded(char* name) {
    std::ifstream file(name);
    if (!file) {
        nlohmann::json jsonData;
        fileutils.saveJsonData(name, jsonData);
    }
    return !file;
}

TEST_F(GrpcDataProcessorTest, LoadWidthAndHeightTest) {
    GrpcDataProcessor mockProcessor(&mockFileUtils);
    mockProcessor.imageDimensions.height = mockProcessor.INVALID_DIMENSION;
    mockProcessor.imageDimensions.width = mockProcessor.INVALID_DIMENSION;

    char jsonFilePath[260];
    snprintf(jsonFilePath, sizeof(jsonFilePath), processor.CAMERA_CONFIGS_FILE, processor.projectPath.c_str());
    EXPECT_CALL(mockFileUtils, readJson(testing::StrEq(jsonFilePath)))
        .WillOnce([](const char*) {
            nlohmann::json jsonData;
            jsonData["pygame_window_dimensions"]["w"] = 800;
            jsonData["pygame_window_dimensions"]["h"] = 600;
            return jsonData;
        });
    mockProcessor.loadWidthAndHeight();
    ASSERT_EQ(mockProcessor.imageDimensions.width, 800);
    ASSERT_EQ(mockProcessor.imageDimensions.height, 600);
}

TEST_F(GrpcDataProcessorTest, SaveImage) {
    processor.nextID = -1;
    cv::Mat blackImage(100, 100, CV_8UC3, cv::Scalar(0, 0, 0));

    bool result = processor.saveImage(blackImage);
    ASSERT_TRUE(result);
    
    std::filesystem::path trainingDataDir = processor.projectPath + "\\training_data";
    if (!std::filesystem::exists(trainingDataDir)) {
        std::filesystem::create_directories(trainingDataDir);
    }

    char jsonFilePath[260];
    snprintf(jsonFilePath, sizeof(jsonFilePath), "%s\\training_data\\%s.jpg", processor.projectPath.c_str(), std::to_string(processor.nextID).c_str());
    remove(jsonFilePath);
}

TEST_F(GrpcDataProcessorTest, SaveEmptyImage) {
    cv::Mat emptyImage;

    bool result = processor.saveImage(emptyImage);
    ASSERT_FALSE(result);
}

TEST_F(GrpcDataProcessorTest, ConvertRGBtoCV2) {
    processor.imageDimensions.height = 2;
    processor.imageDimensions.width = 3;

    google::protobuf::RepeatedField<float> imageBytes;
    for (int i = 0; i < 24; i += 3) {
        imageBytes.Add(255.0f);
        imageBytes.Add(0.0f);
        imageBytes.Add(0.0f);
    }

    cv::Mat resultImage = processor.convertRGBtoCV2(imageBytes);
    ASSERT_FALSE(resultImage.empty());
    ASSERT_EQ(resultImage.rows, processor.imageDimensions.height);
    ASSERT_EQ(resultImage.cols, processor.imageDimensions.width);
}

TEST_F(GrpcDataProcessorTest, ExtractNextImageIdWhenJsonIsEmpty) {
    GrpcDataProcessor mockProcessor(&mockFileUtils);
    mockProcessor.nextID = 0;

    char jsonFilePath[260];
    snprintf(jsonFilePath, sizeof(jsonFilePath), mockProcessor.TRANSFORMS_JSON_FILE, mockProcessor.projectPath.c_str());
    bool emptyFileCreated = createEmptyJsonFileIfNeeded(jsonFilePath);

    EXPECT_CALL(mockFileUtils, readJson(testing::StrEq(jsonFilePath)))
            .WillOnce([](const char*) {
                nlohmann::json jsonData;
                return jsonData;
            });

    mockProcessor.extractNextImageId();
    ASSERT_EQ(mockProcessor.nextID, 0);

    if (emptyFileCreated) {
        remove(jsonFilePath);
    }
}

TEST_F(GrpcDataProcessorTest, ExtractNextImageIdWhenJsonIsNotEmpty) {
    GrpcDataProcessor mockProcessor(&mockFileUtils);
    mockProcessor.nextID = 0;

    char jsonFilePath[260];
    snprintf(jsonFilePath, sizeof(jsonFilePath), mockProcessor.TRANSFORMS_JSON_FILE, mockProcessor.projectPath.c_str());
    bool emptyFileCreated = createEmptyJsonFileIfNeeded(jsonFilePath);

    EXPECT_CALL(mockFileUtils, readJson(testing::StrEq(jsonFilePath)))
            .WillOnce([](const char*) {
                nlohmann::json jsonData;
                jsonData["5"] = {};
                return jsonData;
            });

    mockProcessor.extractNextImageId();
    ASSERT_EQ(mockProcessor.nextID, 6);

    if (emptyFileCreated) {
        remove(jsonFilePath);
    }
}

TEST_F(GrpcDataProcessorTest, SaveTransformAndInViewSpotsData) {
    GrpcDataProcessor mockProcessor(&mockFileUtils);
    mockProcessor.nextID = 0;
    mockProcessor.projectPath = "";
    mockProcessor.TRANSFORMS_JSON_FILE = "test.json";

    char jsonFilePath[260];
    snprintf(jsonFilePath, sizeof(jsonFilePath), mockProcessor.TRANSFORMS_JSON_FILE, mockProcessor.projectPath.c_str());
    bool emptyFileCreated = createEmptyJsonFileIfNeeded(jsonFilePath);

    EXPECT_CALL(mockFileUtils, readJson(testing::StrEq(jsonFilePath)))
            .WillOnce([](const char*) {
                nlohmann::json jsonData;
                return jsonData;
            });

    transform_request transform;
    transform.set_x(0.1);
    transform.set_y(0.1);
    transform.set_z(0.1);
    transform.set_pitch(0.1);
    transform.set_roll(0.1);
    transform.set_yaw(0.1);

    BEV_bounding_box_cord_request BEV_bounding_box_cord;
    BEV_bounding_box_cord.set_left_bottom_x(-6.9);
    BEV_bounding_box_cord.set_left_bottom_y(-22.25);
    BEV_bounding_box_cord.set_left_top_x(-5.3);
    BEV_bounding_box_cord.set_left_top_y(-31.3);
    BEV_bounding_box_cord.set_right_top_x(-19.1);
    BEV_bounding_box_cord.set_right_top_y(-33.7);
    BEV_bounding_box_cord.set_right_bottom_x(-20.7);
    BEV_bounding_box_cord.set_right_bottom_y(-24.68);

    auto inViewSpotsResult = mockProcessor.getAllIntersectingBoundingBoxes(BEV_bounding_box_cord);

    mockProcessor.saveTransformAndInViewSpotsData(transform, inViewSpotsResult);
    ASSERT_EQ(mockProcessor.nextID, 1);
    
    nlohmann::json jsonData = fileutils.readJson(jsonFilePath);
    ASSERT_EQ(jsonData["0"]["x"], transform.x());
    ASSERT_EQ(jsonData["0"]["y"], transform.y());
    ASSERT_EQ(jsonData["0"]["z"], transform.z());
    ASSERT_EQ(jsonData["0"]["pitch"], transform.pitch());
    ASSERT_EQ(jsonData["0"]["roll"], transform.roll());
    ASSERT_EQ(jsonData["0"]["yaw"], transform.yaw());
    ASSERT_EQ(jsonData["0"]["in_view_spots"], "17,18,19,22,23,24,25,32,");

    if (emptyFileCreated) {
        remove(jsonFilePath);
    }
}

TEST_F(GrpcDataProcessorTest, GetAllIntersectingBoundingBoxes) {
    GrpcDataProcessor mockProcessor(&mockFileUtils);

    BoundingBox BEVBoundingBox;
    BEVBoundingBox.x1 = -11.355608940124512;
    BEVBoundingBox.y1 = -21.181715011596680;
    BEVBoundingBox.x2 = -6.9846453666687012;
    BEVBoundingBox.y2 = -26.390810012817383;
    BEVBoundingBox.x3 = -14.645079612731934;
    BEVBoundingBox.y3 = -32.818698883056641;
    BEVBoundingBox.x4 = -19.016042709350586;
    BEVBoundingBox.y4 = -27.609601974487305;

    BEV_bounding_box_cord_request BEV_bounding_box_cord;
    BEV_bounding_box_cord.set_left_bottom_x(BEVBoundingBox.x1);
    BEV_bounding_box_cord.set_left_bottom_y(BEVBoundingBox.y1);
    BEV_bounding_box_cord.set_left_top_x(BEVBoundingBox.x2);
    BEV_bounding_box_cord.set_left_top_y(BEVBoundingBox.y2);
    BEV_bounding_box_cord.set_right_top_x(BEVBoundingBox.x3);
    BEV_bounding_box_cord.set_right_top_y(BEVBoundingBox.y3);
    BEV_bounding_box_cord.set_right_bottom_x(BEVBoundingBox.x4);
    BEV_bounding_box_cord.set_right_bottom_y(BEVBoundingBox.y4);

    auto inViewSpotsResult = mockProcessor.getAllIntersectingBoundingBoxes(BEV_bounding_box_cord);
    ASSERT_EQ(std::get<1>(inViewSpotsResult),  "18,22,23,24,25,");
}