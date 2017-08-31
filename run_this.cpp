// $Id$ $Date$

#include <iostream>
#include <stdexcept>
#include <stdio.h>
#include <string>

std::string fuser(const char* path) {
    char buffer[128];
    std::string result = "fuser ";
    result.append( path);
    FILE* pipe = popen(result.c_str(), "r");
    result.assign("");
    if (!pipe) throw std::runtime_error("popen() failed!");
    try {
        while (!feof(pipe)) {
            if (fgets(buffer, 128, pipe) != NULL)
                result += buffer;
        }
    } catch (...) {
        pclose(pipe);
        throw;
    }
    pclose(pipe);
    return result;
}

#include <iostream>
int main(int, const char * argv[])
{
    try
    {
        std::string result = fuser(argv[0]);
        std::cout << result << "\n";
    } catch (...) {}
    return 0;
}
