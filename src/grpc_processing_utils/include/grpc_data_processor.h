#ifndef IMAGECONVERTER_H
#define IMAGECONVERTER_H

#include <iostream>
#include <vector>
#include <fstream>
#include <cstring>
#include <direct.h>
#include <string>
#include <algorithm>
#include <filesystem>
#include <map>
#include <tuple>

#include "opencv2/opencv.hpp"
#include "file_utils.h"
#include "../../grpc_server/include/ipc_configs.pb.h"
#include "../../utils/structs/GrpcData.h"
#include "../../utils/structs/BoundingBox.h"

struct ImageDimensions {
    int width;
    int height;
};

class GrpcDataProcessor {
public:
    const int INVALID_DIMENSION = -1;
    const char* CAMERA_CONFIGS_FILE = "%s\\birds_eye_view\\camera_configs.json";
    const char* TRANSFORMS_JSON_FILE = "%s\\training_data\\transforms.json";
    const char* PARKING_LOT_COORDINATES_FILE = "%s\\parking_spot_labeller\\spots_data.json";
    ImageDimensions imageDimensions;
    int nextID = 0;
    std::string projectPath;
    std::map<std::string, BoundingBox> labelledParkingSpotsBoundingBoxesMap;

    GrpcDataProcessor(FileUtils* fUtils = nullptr);
    bool convertAndSaveImage(const google::protobuf::RepeatedField<float>& imageBytes);
    void saveTransformAndInViewSpotsData(const transform_request& transform, const std::tuple<int, std::string> inViewSpotsResult);
    void extractNextImageId();
    cv::Mat convertRGBtoCV2(const google::protobuf::RepeatedField<float>& imageBytes);
    bool saveImage(cv::Mat image);
    void loadWidthAndHeight();
    bool checkBoundingBoxesIntesection(const BoundingBox& box1, const BoundingBox& box2);
    void fetchAllParkingSpotsCoordinates();
    std::tuple<int, std::string> getAllIntersectingBoundingBoxes(const BEV_bounding_box_cord_request& BEV_bounding_box_cord);

private:
    FileUtils* fUtils_;
};

#endif
