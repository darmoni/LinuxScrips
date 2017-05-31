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
        bool run();
#endif // RUN_IT
};
#if RUN_IT
bool command_runner::run() {
    pid_t child_pid;

    if(prepare()) {
        child_pid = fork();
        if (child_pid == -1)
        {
            return false;
        }
        if(child_pid == 0) {
        /* This is done by the child process. */

            execv(path(), argv());

        /* If execv returns, it must have failed. */

            printf("Unknown command\n");
            return 0;
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
    return false;
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
#if ! RUN_IT
    printf("DEBUG::: path = '%s', argc = %lu\n", _path, _argv.size());
    for(vector<char * >::iterator i =_argv.begin(); i != _argv.end(); ++i)
    /*if(NULL != *i)*/ printf("'%s' ",*i);
    printf("\n");
#endif
    return true;
}
#if 0
command_runner {
    vector<string> holder_argv;
    map<string,string> holder_path;
    vector<char * > _argv;

    const char *_path;
    char * path_var;
    public:
        void cmd(string c) {
            holder_path["cmd"] = c;
        }
        void arg(string s) {
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
#if RUN_IT
        bool run(){
            pid_t child_pid;

            if(prepare()) {
                child_pid = fork();
                if (child_pid == -1)
                {
                    return false;
                }
                if(child_pid == 0) {
                /* This is done by the child process. */

                    execv(path(), argv());

                /* If execv returns, it must have failed. */

                    printf("Unknown command\n");
                    return 0;
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
            return false;
        }
    private:
#endif
        bool prepare() {
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
#if ! RUN_IT
            printf("DEBUG::: path = '%s', argc = %lu\n", _path, _argv.size());
            for(vector<char * >::iterator i =_argv.begin(); i != _argv.end(); ++i)
            /*if(NULL != *i)*/ printf("'%s' ",*i);
            printf("\n");
#endif
            return true;
        }
};
#endif //0
const char * s1 = "test";
const char * s2 = "test";
char s3[] = "test";
char s4[] = "test";
char * const s5 = s4;
//char * const s6 = (const char * )("test");
int main()
{
//usr/local/registrator/lib/mserver/app/mappemail_acdrecording.php 30320 109050 25518 "7160" 15999 "9801" "7161" \
"Near Darmoni 61" ""Message Center" <message-center@xcastlabs.com>" \
"ndarmoni@xcastlabs.com" "/usr/local/registrator/callrecordings//siptalk64.xcastlabs.com/71/acdcallrec-15999-109049.mp3" wav
    command_runner my_exec;
//    my_exec.cmd("/usr/bin/php");
//    my_exec.arg("-f");
//    my_exec.arg("get_params.php");
    my_exec.cmd("/home/nir/bin/test.py");
    my_exec.arg("-p");
    my_exec.arg("qman_staging_log_server");

/*
printf("Hello World!\n");
// s1[0] = 'a'; FORBIDDEN
printf("s1=%s, s2=%s\n",s1,s2);
char const * const s7(++s2);
printf("s3=%s, s4=%s\n",s3,s4);
printf("s5=%s, s6=%s, s7=%s\n",s5,s6,s7);
s1++;
s3[0] = 'a';
//s4++; // FORBIDDEN
s5[0] = 'a';
//s6[0] = 'a'; // core dump
//s6++; // FORBIDDEN
//s7++; // FORBIDDEN
printf("s1=%s, s2=%s\n",s1,s2);
printf("s3=%s, s4=%s\n",s3,s4);
printf("s5=%s, s6=%s, s7=%s\n",s5,s6,s7);
* */
    bool i =false;
#if RUN_IT
    printf("run %d, result:\n%d\n",__LINE__,i = my_exec.run());
//    printf("run %d, result:\n%d\n",__LINE__,i = my_exec.run());
#else
    printf("run %d, result %d\n",__LINE__,i = my_exec.prepare());
#endif
    return true != i;
}
