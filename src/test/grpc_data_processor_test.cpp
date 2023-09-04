#include <gtest/gtest.h>

#include "../grpc_processing_utils/include/grpc_data_processor.h"

TEST(GrpcDataProcessorTest, GetCurrentDirectoryTest) {
    GrpcDataProcessor processor;
    std::string currentDirectory = processor.getCurrentDirectory();

    ASSERT_FALSE(currentDirectory.empty()) << "Current directory should not be empty.";
    ASSERT_TRUE(currentDirectory.find("src\\grpc_processing_utils") != std::string::npos) << "instead found: " << currentDirectory.c_str();
}



