#include "../include/file_utils.h"

nlohmann::json FileUtils::readJson(const char* jsonFilePath) {
    nlohmann::json jsonData;
    std::ifstream jsonFile(jsonFilePath);
    if (jsonFile.is_open()) {
        jsonFile >> jsonData;
        if (jsonFile.fail()) {
            std::cerr << "Failed to read JSON data from the file." << std::endl;
        }
        jsonFile.close();
    } else {
        std::cerr << "Failed to open JSON file or file does not exist." << std::endl;
    }
    return jsonData;
}

void FileUtils::saveJsonData(const char* jsonFilePath, nlohmann::json& jsonData) {
    std::ofstream outputFile(jsonFilePath);
    if (outputFile.is_open()) {
        outputFile << jsonData.dump(4); // Indent with 4 spaces for better readability
        outputFile.close();
    } else {
        std::cerr << "Error opening file for writing: " << jsonFilePath << std::endl;
    }
}