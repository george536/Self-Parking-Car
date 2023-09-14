#pragma once 
#include <gtest/gtest.h>
#include <gmock/gmock.h>

#include "opencv2/opencv.hpp"
#include "../grpc_processing_utils/include/grpc_data_processor.h"

GrpcDataProcessor processor;

class MockGrpcDataProcessor : public GrpcDataProcessor {
public:
    MOCK_METHOD(nlohmann::json, readJson, (const char* jsonFilePath), (override));
};

TEST(GrpcDataProcessorTest, GetCurrentDirectoryTest) {
    std::string currentDirectory = processor.getCurrentDirectory();

    ASSERT_FALSE(currentDirectory.empty()) << "Current directory should not be empty.";
    ASSERT_TRUE(currentDirectory.find("src\\grpc_processing_utils") != std::string::npos) << "instead found: " << currentDirectory.c_str();
}

TEST(GrpcDataProcessorTest, ReadJsonTest) {
    // Create a temporary JSON file for testing
    const char* testJsonFile = "test_data.json";
    std::ofstream testJsonStream(testJsonFile);
    testJsonStream << R"({"1": "5"})";
    testJsonStream.close();

    // Call the readJson function
    nlohmann::json jsonData = processor.readJson(testJsonFile);

    // Remove the temporary file
    remove(testJsonFile);

    // Check if JSON data was read correctly
    ASSERT_FALSE(jsonData.empty());
    ASSERT_EQ(jsonData["1"], "5");
}

TEST(GrpcDataProcessorTest, ReadEmptyJsonTest) {
    // Create a temporary JSON file for testing
    const char* testJsonFile = "test_data.json";

    // Call the readJson function
    nlohmann::json jsonData = processor.readJson(testJsonFile);

    // Check that jsonData is null
    ASSERT_TRUE(jsonData == nullptr);
}

TEST(GrpcDataProcessorTest, LoadWidthAndHeightTest) {
    MockGrpcDataProcessor mockProcessor;
    mockProcessor.imageDimensions.height = mockProcessor.INVALID_DIMENSION;
    mockProcessor.imageDimensions.width = mockProcessor.INVALID_DIMENSION;
    // Create a mock JSON file with the expected structure
    char jsonFilePath[260];
    snprintf(jsonFilePath, sizeof(jsonFilePath), mockProcessor.CAMERA_CONFIGS_FILE, mockProcessor.currentDirectory.c_str());
    EXPECT_CALL(mockProcessor, readJson(testing::StrEq(jsonFilePath)))
            .WillOnce([](const char*) {
                // Return your mock JSON data here
                nlohmann::json jsonData;
                jsonData["pygame_window_dimensions"]["w"] = 800;
                jsonData["pygame_window_dimensions"]["h"] = 600;
                return jsonData;
            });

    // Call the loadWidthAndHeight function
    mockProcessor.loadWidthAndHeight();

    // Check if the imageDimensions were updated correctly
    ASSERT_EQ(mockProcessor.imageDimensions.width, 800);
    ASSERT_EQ(mockProcessor.imageDimensions.height, 600);
}

TEST(GrpcDataProcessorTest, SaveImage) {
    processor.nextID = -1;
    // Create an empty black image (all pixels are black)
    cv::Mat blackImage(100, 100, CV_8UC3, cv::Scalar(0, 0, 0));

    bool result = processor.saveImage(blackImage);
    ASSERT_TRUE(result);
    
    // Remove the temporary file
    char jsonFilePath[260];
    snprintf(jsonFilePath, sizeof(jsonFilePath), "%s/../..\\training_data\\%s.jpg", processor.currentDirectory.c_str(), std::to_string(processor.nextID).c_str());
    
    remove(jsonFilePath);
}

TEST(GrpcDataProcessorTest, SaveEmptyImage) {
    // Create an empty black image (all pixels are black)
    cv::Mat emptyImage;

    bool result = processor.saveImage(emptyImage);
    ASSERT_FALSE(result);
}

TEST(GrpcDataProcessorTest, ConvertRGBtoCV2) {
    processor.imageDimensions.height = 2;
    processor.imageDimensions.width = 3;

    google::protobuf::RepeatedField<float> imageBytes;
    for (int i = 0; i < 24; i += 3) {
        imageBytes.Add(255.0f);  // Red component
        imageBytes.Add(0.0f);    // Green component
        imageBytes.Add(0.0f);    // Blue component
        }

    cv::Mat resultImage = processor.convertRGBtoCV2(imageBytes);

    ASSERT_FALSE(resultImage.empty());

    ASSERT_EQ(resultImage.rows, processor.imageDimensions.height);
    ASSERT_EQ(resultImage.cols, processor.imageDimensions.width);
}

TEST(GrpcDataProcessorTest, ExtractNextImageIdWhenJsonIsEmpty) {
    MockGrpcDataProcessor mockProcessor;
    mockProcessor.nextID = 0;

    char jsonFilePath[260];
    snprintf(jsonFilePath, sizeof(jsonFilePath), mockProcessor.TRANSFORMS_JSON_FILE, mockProcessor.currentDirectory.c_str());
    
    std::ifstream file(jsonFilePath);
    bool notFound = !file;
    if (notFound) {
        nlohmann::json jsonData;
        mockProcessor.saveJsonData(jsonFilePath, jsonData);
    }

    EXPECT_CALL(mockProcessor, readJson(testing::StrEq(jsonFilePath)))
            .WillOnce([](const char*) {
                // Return your mock JSON data here
                nlohmann::json jsonData;
                return jsonData;
            });
    mockProcessor.extractNextImageId();
    ASSERT_EQ(mockProcessor.nextID, 0);

    if (notFound) {
        remove(jsonFilePath);
    }
}

TEST(GrpcDataProcessorTest, ExtractNextImageIdWhenJsonIsNotEmpty) {
    MockGrpcDataProcessor mockProcessor;
    mockProcessor.nextID = 0;
    char jsonFilePath[260];
    snprintf(jsonFilePath, sizeof(jsonFilePath), mockProcessor.TRANSFORMS_JSON_FILE, mockProcessor.currentDirectory.c_str());
    
    std::ifstream file(jsonFilePath);
    bool notFound = !file;
    if (notFound) {
        nlohmann::json jsonData;
        mockProcessor.saveJsonData(jsonFilePath, jsonData);
    }

    EXPECT_CALL(mockProcessor, readJson(testing::StrEq(jsonFilePath)))
            .WillOnce([](const char*) {
                // Return your mock JSON data here
                nlohmann::json jsonData;
                jsonData["5"] = {};
                return jsonData;
            });
    mockProcessor.extractNextImageId();
    ASSERT_EQ(mockProcessor.nextID, 6);

    if (notFound) {
        remove(jsonFilePath);
    }
}

TEST(GrpcDataProcessorTest, SaveTransformData) {
    MockGrpcDataProcessor mockProcessor;
    mockProcessor.nextID = 0;
    mockProcessor.currentDirectory = "";
    mockProcessor.TRANSFORMS_JSON_FILE = "test.json";

    char jsonFilePath[260];
    snprintf(jsonFilePath, sizeof(jsonFilePath), mockProcessor.TRANSFORMS_JSON_FILE, mockProcessor.currentDirectory.c_str());
    EXPECT_CALL(mockProcessor, readJson(testing::StrEq(jsonFilePath)))
            .WillOnce([](const char*) {
                // Return your mock JSON data here
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
    
    nlohmann::json jsonData = processor.readJson(jsonFilePath);
    ASSERT_EQ(jsonData["0"]["x"], transform.x());
    ASSERT_EQ(jsonData["0"]["y"], transform.y());
    ASSERT_EQ(jsonData["0"]["z"], transform.z());
    ASSERT_EQ(jsonData["0"]["pitch"], transform.pitch());
    ASSERT_EQ(jsonData["0"]["roll"], transform.roll());
    ASSERT_EQ(jsonData["0"]["yaw"], transform.yaw());

    // Remove the temporary file
    remove(jsonFilePath);
}