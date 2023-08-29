#ifndef IMAGECONVERTER_H
#define IMAGECONVERTER_H

#include <opencv2/opencv.hpp>
#include "../../include/ipc_configs.pb.h"
#include <iostream>
#include <vector>
#include <nlohmann/json.hpp>
#include <cstdio>
#include <fstream>

struct ImageDimensions {
    int width;
    int height;
};

class GrpcDataProcessor {
public:
    GrpcDataProcessor();
    bool convertAndSaveImage(const google::protobuf::RepeatedField<float>& imageBytes);
    void saveTransformData(const std::vector<float>& transform);
private:
    const int INVALID_DIMENSION = -1;
    ImageDimensions imageDimensions;
    char lastID;

    char getNextImageId();
    cv::Mat convertRGBtoCV2(const google::protobuf::RepeatedField<float>& imageBytes);
    bool saveImage(cv::Mat image);
    void loadWidthAndHeight();
    void readJson(const char* jsonFilePath);
};

#endif
