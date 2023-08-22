#ifndef IMAGECONVERTER_H
#define IMAGECONVERTER_H

#include <opencv2/opencv.hpp>
#include "../../include/ipc_configs.pb.h"
#include <vector>

class GrpcDataProcessor {
public:
    bool convertAndSaveImage(const char* imageBytes);
    void saveTransformData(const std::vector<float>& transform);
    int getNextImageId();
    const char* convertToBytes(const std::string image);
};

#endif
