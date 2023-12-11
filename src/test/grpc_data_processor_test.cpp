#pragma once 
#include <gtest/gtest.h>
#include <gmock/gmock.h>

#include "opencv2/opencv.hpp"
#include "../grpc_processing_utils/include/grpc_data_processor.h"

using ::testing::NiceMock;

FileUtils fileutils;
GrpcDataProcessor processor;

class MockFileUtils : public FileUtils {
public:
    MOCK_METHOD(nlohmann::json, readJson, (const char* jsonFilePath), (override));
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

TEST_F(GrpcDataProcessorTest, SaveTransformData) {
    GrpcDataProcessor mockProcessor(&mockFileUtils);
    mockProcessor.nextID = 0;
    mockProcessor.projectPath = "";
    mockProcessor.TRANSFORMS_JSON_FILE = "test.json";

    char jsonFilePath[260];
    snprintf(jsonFilePath, sizeof(jsonFilePath), mockProcessor.TRANSFORMS_JSON_FILE, mockProcessor.projectPath.c_str());
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

    mockProcessor.saveTransformData(transform);
    ASSERT_EQ(mockProcessor.nextID, 1);
    
    nlohmann::json jsonData = fileutils.readJson(jsonFilePath);
    ASSERT_EQ(jsonData["0"]["x"], transform.x());
    ASSERT_EQ(jsonData["0"]["y"], transform.y());
    ASSERT_EQ(jsonData["0"]["z"], transform.z());
    ASSERT_EQ(jsonData["0"]["pitch"], transform.pitch());
    ASSERT_EQ(jsonData["0"]["roll"], transform.roll());
    ASSERT_EQ(jsonData["0"]["yaw"], transform.yaw());

    remove(jsonFilePath);
}