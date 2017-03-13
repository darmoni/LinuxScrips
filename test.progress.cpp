#include <iostream>
#include <string>
#include <sys/types.h>
#include <sys/time.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
using namespace std;






static void get_timestamp(std::string & ts)
{
    char buffer[100];
    struct timeval now;
    gettimeofday(&now, NULL);
    sprintf(buffer,"%ld.%06ld",now.tv_sec,now.tv_usec);
    ts.assign(buffer);
}

class inProgress
{
    static bool started;
    bool running;
    public:
    static bool isRunning() {return started;}
    inProgress()
    {
        cout << "inProgress::inProgress()" << inProgress::isRunning() << "\n";
        if(!started)
        {
            running = true;
            started = true;
        }
    }
    ~inProgress() {if (running) started = false;}
};

bool inProgress::started = false;

int test()
{
    if(inProgress::isRunning()) return 1;
    {
        cout << "test() starts " << __LINE__ << "\n";
        inProgress first;
    }
    cout << "test() done " << __LINE__ << "\n";
}

int main()
{
    for(int i =0 ; i < 1; ++i)
    {
        cout << "before testing " << __LINE__ << "\n";
//        inProgress first;
        test();
        cout << "after testing " << __LINE__ << "\n";
        inProgress second;
        cout << "after testing " << __LINE__ << "\n";
    }
    for(int i =0 ; i < 1; ++i)
    {
        cout << "before testing " << inProgress::isRunning() << "\n";
        test();
        {
            inProgress many[3];
        }
        cout << "after testing " << inProgress::isRunning()<< "\n";
        test();
        if(!inProgress::isRunning()) inProgress second;
    }
}
