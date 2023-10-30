#pragma once 
#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include <filesystem>

#include "file_utils.h"

namespace fs = std::filesystem;

FileUtils futils;

TEST(FileUtilsTest, ReadJsonTest) {
    const char* testJsonFile = "test_data.json";
    std::ofstream testJsonStream(testJsonFile);
    testJsonStream << R"({"1": "5"})";
    testJsonStream.close();

    nlohmann::json jsonData = futils.readJson(testJsonFile);
    remove(testJsonFile);
    ASSERT_FALSE(jsonData.empty());
    ASSERT_EQ(jsonData["1"], "5");
}

TEST(FileUtilsTest, ReadEmptyJsonTest) {
    const char* testJsonFile = "test_data.json";
    nlohmann::json jsonData = futils.readJson(testJsonFile);
    ASSERT_TRUE(jsonData == nullptr);
}

TEST(FileUtilsTest, SaveJsonDataTest) {
    const char* testJsonFile = "test_data.json";
    nlohmann::json jsonData = {{"key1", "value1"}, {"key2", 42}};

    futils.saveJsonData(testJsonFile, jsonData);

    std::ifstream testJsonStream(testJsonFile);
    ASSERT_TRUE(testJsonStream.is_open());

    if (testJsonStream.is_open()) {
        nlohmann::json readData;
        testJsonStream >> readData;

        ASSERT_EQ(jsonData, readData);

        testJsonStream.close();
    } else {
        FAIL() << "Failed to open the JSON file for reading.";
    }

    remove(testJsonFile);
}