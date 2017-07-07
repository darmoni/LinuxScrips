#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <unistd.h>
#include <fcntl.h>
#include <sstream>
#include <vector>
#include <map>
#include <sys/wait.h>
using namespace std;

#include <sys/stat.h>
#include <inttypes.h>

class command_runner {
    std::vector<std::string> holder_argv;
    std::map<std::string,std::string> holder_path;
    std::vector<char * > _argv;

    const char *_path;
    char * path_var;
public:
    void cmd(std::string c) {
        holder_path["cmd"] = c;
    }
    void arg(std::string s) {
        holder_argv.push_back(s);
    }
    const char * path() {
        if(prepare()) return _path;
        else return ("");
    }
    char **const argv() {
        if(prepare())
            return &_argv.front();
        else
            return NULL;
    }
    bool prepare();
    int run();
};
bool command_runner::prepare()
{
    if(holder_path.end() == holder_path.find("cmd")) return false;
    if(_argv.size() && 0 == holder_path.find("cmd")->second.compare(_argv[0])) return true;
    _path = path_var = &(holder_path["cmd"])[0];
    if(holder_argv.size() > 0) {
        _argv.resize(holder_argv.size()+1);
        _argv[0] =path_var;
        for (unsigned int i=0; i < holder_argv.size() ; ++i){
            _argv[i+1] = &(holder_argv[i])[0];
        }
        _argv.push_back(NULL);
    }
    if(_argv.size() && 0 == holder_path.find("cmd")->second.compare(_argv[0])) return true;
    return false;
}

int command_runner::run()
{
    pid_t child_pid;

    if(prepare()) {
        child_pid = fork();
        if (child_pid == -1)
        {
            return -1;
        }
        if(child_pid == 0) {
        /* This is done by the child process. */

            execv(path(), argv());

        /* If execv returns, it must have failed. */

            printf("command_runner::run() fileName='%s' !!! Unknown command?", path());
            return -1;
        }
        else {
            int child_status;
            pid_t tpid;
         /* This is run by the parent.  Wait for the child
            to terminate. */
             do {
                    tpid = wait(&child_status);
             } while(tpid != child_pid);
             return child_status;
        }
    }
    return -1;
}

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

#include <sys/stat.h>
#include <inttypes.h>
int file_size(const std::string& path)
{
    struct stat statbuf;
    if (stat(path.c_str(), &statbuf) == -1)
    {
      return -1;
    }
    return statbuf.st_size;
}

int main(int argc, char *argv[]) {

    int r = 0;
    command_runner cmd;
    string fn; //the test file
    if(1 < argc) fn.assign(argv[1]);
    else fn = __FILE__;//argv[0];
    r = file_size(fn);
    if(0 < r) {
        cmd.cmd("/bin/fuser");
        cmd.arg(fn);
        r = cmd.run();//execv(cmd.c_str(), [cmd.c_str(), fn.c_str(), NULL]);// system(cmd.c_str());
    }
    cout << "system call " << cmd.path() << " returned \n" << (int) r << "\ncompiled result: " << ((r < 0)?-1:256==r?0:1) << "\n";
    //printf("file size of %s = %9jd\n", fn,(intmax_t)(ls(fn)));
    return 0;
}
