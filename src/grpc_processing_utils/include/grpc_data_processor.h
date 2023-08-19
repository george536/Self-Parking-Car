#ifndef IMAGECONVERTER_H
#define IMAGECONVERTER_H

#include <opencv2/opencv.hpp>
#include <vector>

class GrpcDataProcessor {
public:
    bool convertAndSaveImage(const std::vector<char> imageBytes);
    void saveTransformData(const std::vector<float>& transform);
    int getNextImageId();
    std::vector<char> convertToBytes(image_request& image);
};

#endif
