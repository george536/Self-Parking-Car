#ifndef FILEUTILS_H
#define FILEUTILS_H

#include <iostream>
#include <nlohmann/json.hpp>
#include <fstream>
#include <cstring>
#include <string>

class fileUtils {
public:
    nlohmann::json readJson(const char* jsonFilePath) {
            nlohmann::json jsonData;
            std::ifstream jsonFile(jsonFilePath);
            if (jsonFile.is_open()) {
                jsonFile >> jsonData;
                if (jsonFile.fail()) {
                    std::cerr << "Failed to read JSON data from the file." << std::endl;
                }
                jsonFile.close();
            } else {
                std::cerr << "Failed to open JSON file." << std::endl;
            }
            return jsonData;
    }

    void saveJsonData(const char* jsonFilePath, nlohmann::json& jsonData) {
        std::ofstream outputFile(jsonFilePath);
        if (outputFile.is_open()) {
            outputFile << jsonData.dump(4); // Indent with 4 spaces for better readability
            outputFile.close();
        } else {
            std::cerr << "Error opening file for writing: " << jsonFilePath << std::endl;
        }
    }

    std::string getCurrentDirectory(std::string fullPath) {
        size_t lastSeparator = fullPath.rfind("\\");  // Find the last separator in the path
        if (lastSeparator != std::string::npos) {
            return fullPath.substr(0, lastSeparator);  // Extract the directory
        }
        std::cerr << "Error getting current directory." << std::endl;
        return "";  // Return an empty string in case of failure
    }
};

#endif // FILEUTILS_H