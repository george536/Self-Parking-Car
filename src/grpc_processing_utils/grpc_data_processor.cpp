#include "include/grpc_data_processor.h"
//#include "opencv2/core.hpp"

GrpcDataProcessor::GrpcDataProcessor() {
    imageDimensions.width = INVALID_DIMENSION;
    imageDimensions.height = INVALID_DIMENSION;
    currentDirectory = getCurrentDirectory();
    loadWidthAndHeight();
    extractNextImageId();
}

bool GrpcDataProcessor::convertAndSaveImage(const google::protobuf::RepeatedField<float>& imageBytes) {

    // Check if image was loaded successfully
    if (imageBytes.empty()) {
        std::cerr << "Failed to load image from RGB data." << std::endl;
        return false;
    }

    cv::Mat image = convertRGBtoCV2(imageBytes);
    
    bool saved = saveImage(image);
    if (!saved) {
        std::cerr << "Failed to save image." << std::endl;
        return false;
    }
    std::cout << "Image saved successfully." << std::endl;

    return true;
}


void GrpcDataProcessor::saveTransformData(const transform_request& transform) {
    std::string currentDir = currentDirectory;
    char filePath[260];
    snprintf(filePath, sizeof(filePath), "%s/../..\\training_data\\transforms.json", currentDir.c_str());

    nlohmann::json jsonData;
    // Append new transform data to the existing JSON data

    // Read existing JSON data from file
    std::ifstream inputFile(filePath);
    if (inputFile.is_open()) {
        inputFile >> jsonData;
        inputFile.close();
    } else {
        // Handle error if the file doesn't exist or can't be opened
}

    jsonData[std::to_string(nextID)] = {
        {"x", transform.x()},
        {"y", transform.y()},
        {"z", transform.z()},
        {"pitch", transform.pitch()},
        {"yaw", transform.yaw()},
        {"roll", transform.roll()},
    };

    std::ofstream outputFile(filePath);
    if (outputFile.is_open()) {
        outputFile << jsonData.dump(4); // Indent with 4 spaces for better readability
        outputFile.close();
    } else {
        std::cerr << "Error opening file for writing: " << filePath << std::endl;
    }

    nextID++;

}

void GrpcDataProcessor::extractNextImageId() {
    std::string currentDir = currentDirectory;
    char filePath[260];
    snprintf(filePath, sizeof(filePath), "%s/../..\\training_data\\transforms.json", currentDir.c_str());

    // Check if the file "transforms.json" exists
    std::ifstream file(filePath);
    if (!file) {
        return; // File doesn't exist, return defaultId
    }

    // Read the JSON content from the file
    nlohmann::json jsonData;
    std::ifstream jsonFile(filePath);
    if (jsonFile.is_open()) {
        jsonFile >> jsonData;
        if (jsonFile.fail()) {
            std::cerr << "Failed to read JSON data from the file." << std::endl;
        }
        jsonFile.close();
    } else {
        std::cerr << "Failed to open JSON file." << std::endl;
    }

    for (auto it = jsonData.begin(); it != jsonData.end(); ++it) {
        if (std::stoi(it.key()) > nextID) {
            nextID = std::stoi(it.key());
        }
    }

    nextID++;
}

cv::Mat GrpcDataProcessor::convertRGBtoCV2(const google::protobuf::RepeatedField<float>& imageBytes) {
    int height = imageDimensions.height;
    int width = imageDimensions.width;

    cv::Mat image(height, width, CV_8UC3);
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            int index = (y * width + x) * 3;
            image.at<cv::Vec3b>(y, x) = cv::Vec3b(
            static_cast<unsigned char>(imageBytes[index + 2]),
            static_cast<unsigned char>(imageBytes[index + 1]),
            static_cast<unsigned char>(imageBytes[index])   
            );
        }
    }
    return image;
}

bool GrpcDataProcessor::saveImage(cv::Mat image) {
    std::string currentDir = currentDirectory;
    char filePath[260];
    snprintf(filePath, sizeof(filePath), "%s/../..\\training_data\\%s.jpg", currentDir.c_str(), std::to_string(nextID).c_str());
    return cv::imwrite(filePath, image);
}

void GrpcDataProcessor::loadWidthAndHeight() {
    if(imageDimensions.width == INVALID_DIMENSION || imageDimensions.height == INVALID_DIMENSION) {
        std::string currentDir = currentDirectory;
        char jsonFilePath[260];
        snprintf(jsonFilePath, sizeof(jsonFilePath), "%s/../..\\birds_eye_view\\camera_configs.json", currentDir.c_str());
        readJson(jsonFilePath);
    }
}

void GrpcDataProcessor::readJson(const char* jsonFilePath) {
        nlohmann::json jsonData;
        std::ifstream jsonFile(jsonFilePath);
        if (jsonFile.is_open()) {
            jsonFile >> jsonData;
            if (jsonFile.fail()) {
                std::cerr << "Failed to read JSON data from the file." << std::endl;
            }
            jsonFile.close();
        } else {
            std::cerr << "Failed to open JSON file." << std::endl;
        }
        
        nlohmann::json pygame_window_dimensions = jsonData["pygame_window_dimensions"];
        imageDimensions.width = pygame_window_dimensions["w"];
        imageDimensions.height = pygame_window_dimensions["h"];
}

std::string GrpcDataProcessor::getCurrentDirectory() {
    std::string fullPath(__FILE__);  // Get full path of the current source file
    size_t lastSeparator = fullPath.rfind("\\");  // Find the last separator in the path
    if (lastSeparator != std::string::npos) {
        return fullPath.substr(0, lastSeparator);  // Extract the directory
    }
    std::cerr << "Error getting current directory." << std::endl;
    return "";  // Return an empty string in case of failure
}

