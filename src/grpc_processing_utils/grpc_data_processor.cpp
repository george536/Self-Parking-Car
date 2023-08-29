#include "include/grpc_data_processor.h"

GrpcDataProcessor::GrpcDataProcessor() {
    imageDimensions.width = INVALID_DIMENSION;
    imageDimensions.height = INVALID_DIMENSION;
}

bool GrpcDataProcessor::convertAndSaveImage(const google::protobuf::RepeatedField<float>& imageBytes) {

    // Check if image was loaded successfully
    if (imageBytes.empty()) {
        std::cerr << "Failed to load image from RGB data." << std::endl;
        return false;
    }

    loadWidthAndHeight();

    cv::Mat image = convertRGBtoCV2(imageBytes);
    // check if needed
    cv::Mat bgr_image;
    cv::cvtColor(image, bgr_image, cv::COLOR_RGB2BGR);
    // ###############
    
    bool saved = saveImage(image);
    if (!saved) {
        std::cerr << "Failed to save image." << std::endl;
        return false;
    }
    std::cout << "Image saved successfully." << std::endl;

    return true;
}


void GrpcDataProcessor::saveTransformData(const std::vector<float>& transform) {

}

char GrpcDataProcessor::getNextImageId() {
    return '0';
}

cv::Mat GrpcDataProcessor::convertRGBtoCV2(const google::protobuf::RepeatedField<float>& imageBytes) {
    int height = imageDimensions.height;
    int width = imageDimensions.width;

    cv::Mat image(height, width, CV_8UC3);
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            int index = (y * width + x) * 3;
            image.at<cv::Vec3b>(y, x) = cv::Vec3b(
                static_cast<unsigned char>(imageBytes[index] * 255),
                static_cast<unsigned char>(imageBytes[index + 1] * 255),
                static_cast<unsigned char>(imageBytes[index + 2] * 255)
            );
        }
    }
    return image;
}

bool GrpcDataProcessor::saveImage(cv::Mat image) {
    char nextID = getNextImageId();
    char currentDirectory[FILENAME_MAX];
    char filePath[260];
    snprintf(filePath, sizeof(filePath), "%s/../..\\training_data\\%c.jpg", currentDirectory, nextID);
    return cv::imwrite(filePath, image);
}

void GrpcDataProcessor::loadWidthAndHeight() {
    if(imageDimensions.width == INVALID_DIMENSION || imageDimensions.height == INVALID_DIMENSION) {
        char currentDirectory[FILENAME_MAX];
        char jsonFilePath[260];
        snprintf(jsonFilePath, sizeof(jsonFilePath), "%s/../..\\birds_eye_view\\camera_configs.json", currentDirectory);
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

