#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <unistd.h>
#include <sys/wait.h>
using namespace std;
#define RUN_IT 1

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
#if RUN_IT
        int run();
#endif // RUN_IT
};
#if RUN_IT
    int command_runner::run(){
        pid_t child_pid;

        if(prepare()) {
            child_pid = fork();
            if (child_pid == -1)
            {
                printf("fork failed? '%d'\n", child_pid);
                return child_pid;
            }
            if(child_pid == 0) {
            /* This is done by the child process. */

                execv(path(), argv());

            /* If execv returns, it must have failed. */

                printf("Unknown command '%s'\n", path());
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
                 printf("Got results '%d'\n", child_status);
                 return child_status;
            }
        }
        printf("how did we get here? '%d'\n", child_pid);
        return -1;
    }
#endif // RUN_IT
bool command_runner::prepare() {
    if(holder_path.end() == holder_path.find("cmd")) return false;
    if(_argv.size() && 0 == holder_path.find("cmd")->second.compare(_argv[0])) return true;
    _path = path_var = &(holder_path["cmd"])[0];
    if(holder_argv.size() > 0) {
        _argv.resize(holder_argv.size()+1);
        _argv[0] =path_var;
        for (int i=0; i < holder_argv.size() ; ++i){
            _argv[i+1] = &(holder_argv[i])[0];
        }
        _argv.push_back(NULL);
    }
//#if ! RUN_IT
    printf("DEBUG::: path = '%s', argc = %lu\n", _path, _argv.size());
    for(vector<char * >::iterator i =_argv.begin(); i != _argv.end(); ++i)
    /*if(NULL != *i)*/ printf("'%s' ",*i);
//#endif
    printf("prepare is done\n");
    return true;
}

const char * s1 = "test";
const char * s2 = "test";
char s3[] = "test";
char s4[] = "test";
char * const s5 = s4;
//char * const s6 = (const char * )("test");
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
int main(int argc, char *argv[])
{
//usr/local/registrator/lib/mserver/app/mappemail_acdrecording.php 30320 109050 25518 "7160" 15999 "9801" "7161" \
"Near Darmoni 61" ""Message Center" <message-center@xcastlabs.com>" \
"ndarmoni@xcastlabs.com" "/usr/local/registrator/callrecordings//siptalk64.xcastlabs.com/71/acdcallrec-15999-109049.mp3" wav
    command_runner my_exec;
    int ret = 0;
//    my_exec.cmd("/usr/bin/php");
//    my_exec.arg("-f");
//    my_exec.arg("get_params.php");
    my_exec.cmd("/bin/fuser");

    //string fn = argv[0];
    string fn = __FILE__;
    if(argc >1)fn.assign(argv[1]);
    printf("running %s %s \n",my_exec.path(),fn.c_str());
    if(-1 == file_size(fn)) ret = -1;
    else
        my_exec.arg(fn);
    //my_exec.arg("qman_staging_log_server");


#if RUN_IT
    if(!ret) ret = my_exec.run();
    printf("run %d, result '%d'\n",__LINE__,ret);
//    printf("run %d, result:\n%d\n",__LINE__,i = my_exec.run());
#else
    printf("run %d, result %d\n",__LINE__,ret = my_exec.prepare());
#endif
    return ret;
}
