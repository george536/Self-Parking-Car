#ifndef IMAGECONVERTER_H
#define IMAGECONVERTER_H

#include <opencv2/opencv.hpp>
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
    GrpcDataProcessor();
    bool convertAndSaveImage(const google::protobuf::RepeatedField<float>& imageBytes);
    void saveTransformData(const transform_request& transform);
private:
    const int INVALID_DIMENSION = -1;
    ImageDimensions imageDimensions;
    int nextID = 0;
    std::string currentDirectory;

    void extractNextImageId();
    cv::Mat convertRGBtoCV2(const google::protobuf::RepeatedField<float>& imageBytes);
    bool saveImage(cv::Mat image);
    void loadWidthAndHeight();
    void readJson(const char* jsonFilePath);
    std::string getCurrentDirectory();
};

#endif
