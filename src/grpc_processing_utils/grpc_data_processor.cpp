#include "include/grpc_data_processor.h"

bool GrpcDataProcessor::convertAndSaveImage(const std::vector<char> imageBytes) {
    // Convert std::vector<char> to cv::Mat
    cv::Mat imageMat(imageBytes.size(), 1, CV_8U);
    memcpy(imageMat.data, imageBytes.data(), imageBytes.size() * sizeof(char));

    // If the image format is known (e.g., JPEG or PNG), you can decode it using cv::imdecode
    cv::Mat decodedImage = cv::imdecode(imageMat, cv::IMREAD_COLOR);

    // Check if the image was successfully decoded
    if (decodedImage.empty()) {
        std::cout << "Error decoding image" << std::endl;
        return false;
    }

    // Save the decoded image to a file
    std::string outputFilename = "output.jpg";
    cv::imwrite(outputFilename, decodedImage);

    return true;
}

void GrpcDataProcessor::saveTransformData(const std::vector<float>& transform) {

}

int GrpcDataProcessor::getNextImageId() {
    return 0;
}

std::vector<char> GrpcDataProcessor::convertToBytes(image_request& image) {
    // Create a pointer to the object and a pointer to a byte
    const char* bytePointer = reinterpret_cast<const char*>(&image);

    // Calculate the size of the object in bytes
    size_t objectSize = sizeof(image);

    // Create a vector to hold the bytes
    std::vector<char> byteList(bytePointer, bytePointer + objectSize);

    return byteList;
}
