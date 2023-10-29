#include "include/grpc_data_processor.h"

namespace fs = std::filesystem;

GrpcDataProcessor::GrpcDataProcessor(FileUtils* fUtils) : fUtils_(fUtils) {
    if (!fUtils_) {
        fUtils_ = new FileUtils;
    }

    imageDimensions.width = INVALID_DIMENSION;
    imageDimensions.height = INVALID_DIMENSION;
    projectPath = fs::current_path().string();
    loadWidthAndHeight();
    extractNextImageId();
}

bool GrpcDataProcessor::convertAndSaveImage(const google::protobuf::RepeatedField<float>& imageBytes) {
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
    char filePath[260];
    snprintf(filePath, sizeof(filePath), TRANSFORMS_JSON_FILE, projectPath.c_str());

    nlohmann::json jsonData = fUtils_->readJson(filePath);

    jsonData[std::to_string(nextID)] = {
        {"x", transform.x()},
        {"y", transform.y()},
        {"z", transform.z()},
        {"pitch", transform.pitch()},
        {"yaw", transform.yaw()},
        {"roll", transform.roll()},
    };

    fUtils_->saveJsonData(filePath, jsonData);

    nextID++;
}

void GrpcDataProcessor::extractNextImageId() {
    char filePath[260];
    snprintf(filePath, sizeof(filePath), TRANSFORMS_JSON_FILE, projectPath.c_str());

    std::ifstream file(filePath);
    if (!file) {
        return;
    }

    nlohmann::json jsonData = fUtils_->readJson(filePath);
    if (jsonData.empty()) {
        return;
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
    if (image.empty()) {
        return false;
    }
    char filePath[260];
    snprintf(filePath, sizeof(filePath), "%s\\training_data\\%s.jpg", projectPath.c_str(), std::to_string(nextID).c_str());
    return cv::imwrite(filePath, image);
}

void GrpcDataProcessor::loadWidthAndHeight() {
    if(imageDimensions.width == INVALID_DIMENSION || imageDimensions.height == INVALID_DIMENSION) {
        char jsonFilePath[260];
        snprintf(jsonFilePath, sizeof(jsonFilePath), CAMERA_CONFIGS_FILE, projectPath.c_str());
        nlohmann::json jsonData = fUtils_->readJson(jsonFilePath);
        nlohmann::json pygame_window_dimensions = jsonData["pygame_window_dimensions"];
        imageDimensions.width = pygame_window_dimensions["w"];
        imageDimensions.height = pygame_window_dimensions["h"];
    }
}