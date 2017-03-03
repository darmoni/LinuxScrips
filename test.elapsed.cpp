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

class elapsedTimeCalculator
{
    struct timeval start, now;
    suseconds_t limit, seconds;
    bool passed;
    public:
    elapsedTimeCalculator(suseconds_t _uSecondslimit):limit(_uSecondslimit % 1000000),
                                seconds((_uSecondslimit-limit)/1000000),passed(false)
    {
       gettimeofday(&start, NULL); 
    }
    bool over()
    {
        if(passed) return true;
        gettimeofday(&now, NULL);
        if((now.tv_sec-start.tv_sec) > (1+seconds))
            {
                passed = true;
                return true;
            }
        if((now.tv_sec-start.tv_sec) == seconds)
        {
            if (limit + start.tv_usec <= now.tv_usec)
            {
                passed = true;
                return true;
            }
        }
        else if((now.tv_sec-start.tv_sec) > seconds)
        {
            if (start.tv_usec <= (limit+now.tv_usec))
            {
                passed = true;
                return true;
            }                
        }
        return false;
    }    
};

int main()
{
    bool lt_sec_passed = false;
    bool gt_sec_passed = false;
    suseconds_t lt_sec =  500000;
    suseconds_t gt_sec = 3500000;
    string ts="";
    elapsedTimeCalculator ltsec(lt_sec);
    elapsedTimeCalculator gtsec(gt_sec);
    int i;
    for(i=0;i<40;++i)
    {
        get_timestamp(ts);
        if(!lt_sec_passed && ltsec.over())
        {
            lt_sec_passed = true;
            cout << ts << " longer than "<< lt_sec << "\n" << flush;
            
        }
        if(!gt_sec_passed && gtsec.over())
        {
            gt_sec_passed = true;
            cout << ts << " longer than "<< gt_sec << "\n" << flush;
            //break;
        }
        if(!(lt_sec_passed && gt_sec_passed)) cout << ts <<  " zzzz\n" << flush;
        usleep(300000);
    }
    cout << "Value of i=" << i << "\n";
}
