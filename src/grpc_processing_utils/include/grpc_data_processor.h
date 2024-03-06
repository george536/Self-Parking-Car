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

#include "opencv2/opencv.hpp"
#include "file_utils.h"
#include "../../grpc_server/include/ipc_configs.pb.h"
#include "../../utils/structs/GrpcData.h"

struct ImageDimensions {
    int width;
    int height;
};

class GrpcDataProcessor {
public:
    const int INVALID_DIMENSION = -1;
    const char* CAMERA_CONFIGS_FILE = "%s\\birds_eye_view\\camera_configs.json";
    const char* TRANSFORMS_JSON_FILE = "%s\\training_data\\transforms.json";
    ImageDimensions imageDimensions;
    int nextID = 0;
    std::string projectPath;

    GrpcDataProcessor(FileUtils* fUtils = nullptr);
    bool convertAndSaveImage(const google::protobuf::RepeatedField<float>& imageBytes);
    void saveTransformData(const transform_request& transform);
    void extractNextImageId();
    cv::Mat convertRGBtoCV2(const google::protobuf::RepeatedField<float>& imageBytes);
    bool saveImage(cv::Mat image);
    void loadWidthAndHeight();

private:
    FileUtils* fUtils_;
};

#endif
