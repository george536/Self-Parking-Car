#ifndef FILEUTILS_H
#define FILEUTILS_H

#include <iostream>
#include <nlohmann/json.hpp>
#include <fstream>
#include <cstring>
#include <string>

class FileUtils {
public:
    virtual nlohmann::json readJson(const char* jsonFilePath);
    void saveJsonData(const char* jsonFilePath, nlohmann::json& jsonData);
};

#endif