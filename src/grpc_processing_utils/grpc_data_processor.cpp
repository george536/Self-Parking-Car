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
    fetchAllParkingSpotsCoordinates();
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

void GrpcDataProcessor::saveTransformAndInViewSpotsData(const transform_request& transform, const std::tuple<int, std::string> inViewSpotsResult) {
    int numOfSpotsFound = std::get<0>(inViewSpotsResult);
    std::string inViewSpots = std::get<1>(inViewSpotsResult);

    char transformsJsonFilePath[260];
    snprintf(transformsJsonFilePath, sizeof(transformsJsonFilePath), TRANSFORMS_JSON_FILE, projectPath.c_str());

    nlohmann::json jsonData = fUtils_->readJson(transformsJsonFilePath);

    jsonData[std::to_string(nextID)] = {
        {"x", transform.x()},
        {"y", transform.y()},
        {"z", transform.z()},
        {"pitch", transform.pitch()},
        {"yaw", transform.yaw()},
        {"roll", transform.roll()},
        {"in_view_spots", inViewSpots}
    };

    std::cout << "Saving vehicle location x: "<< transform.x() 
    << " , y: "<< transform.y() 
    << ", and the number of parking spots found in view is: " << numOfSpotsFound << " spots"
    << std::endl;

    fUtils_->saveJsonData(transformsJsonFilePath, jsonData);

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

bool GrpcDataProcessor::checkBoundingBoxesIntesection(const BoundingBox& box1, const BoundingBox& box2) {
    // Check if any corner of box1 is inside box2
    if ((box1.x1 >= std::min(box2.x1, box2.x3) && box1.x1 <= std::max(box2.x1, box2.x3) &&
         box1.y1 >= std::min(box2.y1, box2.y3) && box1.y1 <= std::max(box2.y1, box2.y3)) ||
        (box1.x2 >= std::min(box2.x1, box2.x3) && box1.x2 <= std::max(box2.x1, box2.x3) &&
         box1.y2 >= std::min(box2.y1, box2.y3) && box1.y2 <= std::max(box2.y1, box2.y3)) ||
        (box1.x3 >= std::min(box2.x1, box2.x3) && box1.x3 <= std::max(box2.x1, box2.x3) &&
         box1.y3 >= std::min(box2.y1, box2.y3) && box1.y3 <= std::max(box2.y1, box2.y3)) ||
        (box1.x4 >= std::min(box2.x1, box2.x3) && box1.x4 <= std::max(box2.x1, box2.x3) &&
         box1.y4 >= std::min(box2.y1, box2.y3) && box1.y4 <= std::max(box2.y1, box2.y3)))
        return true;

    // Check if any corner of box2 is inside box1
    if ((box2.x1 >= std::min(box1.x1, box1.x3) && box2.x1 <= std::max(box1.x1, box1.x3) &&
         box2.y1 >= std::min(box1.y1, box1.y3) && box2.y1 <= std::max(box1.y1, box1.y3)) ||
        (box2.x2 >= std::min(box1.x1, box1.x3) && box2.x2 <= std::max(box1.x1, box1.x3) &&
         box2.y2 >= std::min(box1.y1, box1.y3) && box2.y2 <= std::max(box1.y1, box1.y3)) ||
        (box2.x3 >= std::min(box1.x1, box1.x3) && box2.x3 <= std::max(box1.x1, box1.x3) &&
         box2.y3 >= std::min(box1.y1, box1.y3) && box2.y3 <= std::max(box1.y1, box1.y3)) ||
        (box2.x4 >= std::min(box1.x1, box1.x3) && box2.x4 <= std::max(box1.x1, box1.x3) &&
         box2.y4 >= std::min(box1.y1, box1.y3) && box2.y4 <= std::max(box1.y1, box1.y3)))
        return true;

    // Check if box1 is inside box2
    if ((box1.x1 >= std::min(box2.x1, box2.x3) && box1.x1 <= std::max(box2.x1, box2.x3) &&
         box1.y1 >= std::min(box2.y1, box2.y3) && box1.y1 <= std::max(box2.y1, box2.y3)) &&
        (box1.x2 >= std::min(box2.x1, box2.x3) && box1.x2 <= std::max(box2.x1, box2.x3) &&
         box1.y2 >= std::min(box2.y1, box2.y3) && box1.y2 <= std::max(box2.y1, box2.y3)) &&
        (box1.x3 >= std::min(box2.x1, box2.x3) && box1.x3 <= std::max(box2.x1, box2.x3) &&
         box1.y3 >= std::min(box2.y1, box2.y3) && box1.y3 <= std::max(box2.y1, box2.y3)) &&
        (box1.x4 >= std::min(box2.x1, box2.x3) && box1.x4 <= std::max(box2.x1, box2.x3) &&
         box1.y4 >= std::min(box2.y1, box2.y3) && box1.y4 <= std::max(box2.y1, box2.y3)))
        return true;

    // Check if box2 is inside box1
    if ((box2.x1 >= std::min(box1.x1, box1.x3) && box2.x1 <= std::max(box1.x1, box1.x3) &&
         box2.y1 >= std::min(box1.y1, box1.y3) && box2.y1 <= std::max(box1.y1, box1.y3)) &&
        (box2.x2 >= std::min(box1.x1, box1.x3) && box2.x2 <= std::max(box1.x1, box1.x3) &&
         box2.y2 >= std::min(box1.y1, box1.y3) && box2.y2 <= std::max(box1.y1, box1.y3)) &&
        (box2.x3 >= std::min(box1.x1, box1.x3) && box2.x3 <= std::max(box1.x1, box1.x3) &&
         box2.y3 >= std::min(box1.y1, box1.y3) && box2.y3 <= std::max(box1.y1, box1.y3)) &&
        (box2.x4 >= std::min(box1.x1, box1.x3) && box2.x4 <= std::max(box1.x1, box1.x3) &&
         box2.y4 >= std::min(box1.y1, box1.y3) && box2.y4 <= std::max(box1.y1, box1.y3)))
        return true;

    // Check for edge overlap
    if ((box1.x1 == box2.x1 && box1.y1 == box2.y1) || (box1.x2 == box2.x1 && box1.y2 == box2.y1) ||
        (box1.x3 == box2.x1 && box1.y3 == box2.y1) || (box1.x4 == box2.x1 && box1.y4 == box2.y1) ||
        (box1.x1 == box2.x2 && box1.y1 == box2.y2) || (box1.x2 == box2.x2 && box1.y2 == box2.y2) ||
        (box1.x3 == box2.x2 && box1.y3 == box2.y2) || (box1.x4 == box2.x2 && box1.y4 == box2.y2) ||
        (box1.x1 == box2.x3 && box1.y1 == box2.y3) || (box1.x2 == box2.x3 && box1.y2 == box2.y3) ||
        (box1.x3 == box2.x3 && box1.y3 == box2.y3) || (box1.x4 == box2.x3 && box1.y4 == box2.y3) ||
        (box1.x1 == box2.x4 && box1.y1 == box2.y4) || (box1.x2 == box2.x4 && box1.y2 == box2.y4) ||
        (box1.x3 == box2.x4 && box1.y3 == box2.y4) || (box1.x4 == box2.x4 && box1.y4 == box2.y4))
        return true;

    return false;
}

void GrpcDataProcessor::fetchAllParkingSpotsCoordinates() {
    char parkingSpotsJsonFilePath[260];
    snprintf(parkingSpotsJsonFilePath, sizeof(parkingSpotsJsonFilePath), PARKING_LOT_COORDINATES_FILE, projectPath.c_str());

    nlohmann::json jsonData = fUtils_->readJson(parkingSpotsJsonFilePath);
    for (auto& pair : jsonData.items()) {
        if (pair.key() == "parking lot") {
            continue;
        }
        BoundingBox parkingSpotBoundingBox;
        parkingSpotBoundingBox.x1 = pair.value()[0][0];
        parkingSpotBoundingBox.y1 = pair.value()[0][1];
        parkingSpotBoundingBox.x2 = pair.value()[1][0];
        parkingSpotBoundingBox.y2 = pair.value()[1][1];
        parkingSpotBoundingBox.x3 = pair.value()[2][0];
        parkingSpotBoundingBox.y3 = pair.value()[2][1];
        parkingSpotBoundingBox.x4 = pair.value()[3][0];
        parkingSpotBoundingBox.y4 = pair.value()[3][1];

        labelledParkingSpotsBoundingBoxesMap[pair.key()] = parkingSpotBoundingBox;
    }
}

std::tuple<int, std::string> GrpcDataProcessor::getAllIntersectingBoundingBoxes(const BEV_bounding_box_cord_request& BEV_bounding_box_cord) {
    std::string intersectingBoundingBoxesIds = "";
    BoundingBox BEVBoundingBox;
    BEVBoundingBox.x1 = BEV_bounding_box_cord.left_bottom_x();
    BEVBoundingBox.y1 = BEV_bounding_box_cord.left_bottom_y();
    BEVBoundingBox.x2 = BEV_bounding_box_cord.left_top_x();
    BEVBoundingBox.y2 = BEV_bounding_box_cord.left_top_y();
    BEVBoundingBox.x3 = BEV_bounding_box_cord.right_top_x();
    BEVBoundingBox.y3 = BEV_bounding_box_cord.right_top_y();
    BEVBoundingBox.x4 = BEV_bounding_box_cord.right_bottom_x();
    BEVBoundingBox.y4 = BEV_bounding_box_cord.right_bottom_y();

    int numOfSpotsFound = 0;
    for (const auto& parkingSpotBoundingBox : labelledParkingSpotsBoundingBoxesMap) {
        if (checkBoundingBoxesIntesection(parkingSpotBoundingBox.second, BEVBoundingBox)) {
            numOfSpotsFound++;
            intersectingBoundingBoxesIds += parkingSpotBoundingBox.first + ",";
        }
    }

    return std::make_tuple(numOfSpotsFound, intersectingBoundingBoxesIds);
}
