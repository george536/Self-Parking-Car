#pragma once 
#include <gtest/gtest.h>
#include <gmock/gmock.h>

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



