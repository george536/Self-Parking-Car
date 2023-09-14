#ifndef IMAGECONVERTER_H
#define IMAGECONVERTER_H

#include "opencv2/opencv.hpp"
#include "../../include/ipc_configs.pb.h"
#include <iostream>
#include <vector>
#include <nlohmann/json.hpp>
#include <fstream>
#include <cstring>
#include <direct.h>
#include <string>
#include <algorithm>

struct ImageDimensions {
    int width;
    int height;
};

class GrpcDataProcessor {
public:
    const int INVALID_DIMENSION = -1;
    const char* CAMERA_CONFIGS_FILE = "%s/../..\\birds_eye_view\\camera_configs.json";
    const char* TRANSFORMS_JSON_FILE = "%s/../..\\training_data\\transforms.json";
    ImageDimensions imageDimensions;
    int nextID = 0;
    std::string currentDirectory;

    GrpcDataProcessor();
    bool convertAndSaveImage(const google::protobuf::RepeatedField<float>& imageBytes);
    void saveTransformData(const transform_request& transform);
    void extractNextImageId();
    cv::Mat convertRGBtoCV2(const google::protobuf::RepeatedField<float>& imageBytes);
    bool saveImage(cv::Mat image);
    void loadWidthAndHeight();
    virtual nlohmann::json readJson(const char* jsonFilePath);
    std::string getCurrentDirectory();
    void saveJsonData(const char* jsonFilePath, nlohmann::json& jsonData);
};

#endif
