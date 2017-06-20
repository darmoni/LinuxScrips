#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <unistd.h>
#include <fcntl.h>
#include <sstream>
using namespace std;

#include <sys/stat.h>
#include <inttypes.h>

int ls(const string &path)
{
    struct stat statbuf;
    if (stat(path.c_str(), &statbuf) == -1) {
      cout << "Error, invalid unswer\n";/* check the value of errno */
      return -1;
    }
    return statbuf.st_size;
    //else printf("%9jd\n", statbuf.st_size);
}
int main(int argc, char *argv[]) {
    string fn; //the test file
    if(0 < argc) fn.assign(argv[1]);
    else fn = argv[0];
    string cmd = "/bin/fuser ";
    cmd.append(fn);
    unsigned char r = execv(cmd.c_str(), [cmd.c_str(), fn.c_str(), NULL]);// system(cmd.c_str());
    cout << "system call " << cmd << " returned \n" << (int) r << "\ncompiled result: " << ((r <0)? -1:r) << "\n";
    //printf("file size of %s = %9jd\n", fn,(intmax_t)(ls(fn)));
    return 0;
}
