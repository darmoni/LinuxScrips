

#include <iostream>
#include <sstream>
#include <vector>
#include <map>

using namespace std;


#define update_log_levels(a) log_levels[#a] = (a);


class LogLevels{

protected:
    map<const char*, unsigned> log_levels;
    string definition;
    vector<string> lines;
    bool presentFirst;

public:
    enum LogLevel_t {
        LOG_ALWAYS		= 1 >> 1,
        LOG_ERROR		= 1 << 0,
        LOG_DEBUG		= 1 << 1,
        LOG_TRACE		= 1 << 2,
        LOG_SHORT		= 1 << 3,
        LOG_FULL		= 1 << 4,
        LOG_LEVELS		= 0x0000FFFF
    };
    LogLevels(bool _presentFirst = true, string const def = ""):definition(def), presentFirst(_presentFirst) {
        log_levels.clear();
        update_log_levels(LOG_ALWAYS)
        update_log_levels(LOG_ERROR)
        update_log_levels(LOG_DEBUG)
        update_log_levels(LOG_TRACE)
        update_log_levels(LOG_SHORT)
        update_log_levels(LOG_FULL)
        update_log_levels(LOG_LEVELS)
        log_levels["Critical"] = 2;
        log_levels["Error"] = 3;
        log_levels["Notice"] = 5;
        log_levels["Warning"] = 4;
        log_levels["Debug"] = 7;
        log_levels["Informational"] = 6;

        string delimiter = "\n";
        size_t pos = 0;
        string line;
        while((pos = definition.find(delimiter)) != std::string::npos)
        {
            line = definition.substr(0, pos);
            lines.push_back(line);
            definition.erase(0, pos + delimiter.length());
        }
        definition = def;
    }
    string to_string()
    {
        ostringstream os;
        for (auto it = log_levels.begin() ; it != log_levels.end(); ++it)
        {
            os << it->first << " = " << it->second << '\n';
        }
        return os.str();
    }
    const map<const char*, unsigned> get_log_levels(){
        auto _log_levels = log_levels;
        return _log_levels;
    }

    virtual void present(ostream & os = cout) {
        size_t pos = 0;
        for (auto line = lines.begin(); line != lines.end(); ++line)
        {
            //os << *line << "\n";
            for (auto it = log_levels.begin() ; it != log_levels.end(); ++it)
            {
                //os << it->second << "==>" << it->first << "\n";
                if((pos = line->find(it->first)) != std::string::npos)
                {
                    if(presentFirst)
                        os << it->first << " ==> " << *line << "\n";
                    else
                        os << it->second << " ==> " << *line << "\n";
                    break;
                }
            }
        }
    }
    virtual ~LogLevels()
    {}

};
#include <syslog.h>
#include <unistd.h>
#include <sys/types.h>


class SyslogLogLevels: public LogLevels{
public:
    SyslogLogLevels(bool _presentFirst = false, string const def = ""):LogLevels(_presentFirst, def){
        log_levels.clear();
        update_log_levels(LOG_EMERG)
        update_log_levels(LOG_ALERT)
        update_log_levels(LOG_CRIT)
        update_log_levels(LOG_ERR)
        update_log_levels(LOG_WARNING)
        update_log_levels(LOG_NOTICE)
        update_log_levels(LOG_INFO)
        update_log_levels(LOG_DEBUG)
    }
};


int main()
{ 
    string syslog_levels = R">>>(Values for level
       This determines the importance of the message.  The levels are, in
       order of decreasing importance:

       LOG_EMERG      system is unusable 
       LOG_ALERT      action must be taken immediately 
       LOG_CRIT       critical conditions 
       LOG_ERR        error conditions 
       LOG_WARNING    warning conditions 
       LOG_NOTICE     normal, but significant, condition 
       LOG_INFO       informational message 
       LOG_DEBUG      debug-level message
    )>>>";

    string 	Severities = R">>>(static int Severities[8] = {
    2,	// Critical
    3,	// Error
    5,	// Notice
    4,	// Warning
    7,	// Debug
    3,
    6, // Informational
    3	};
    )>>>";
    auto  syslog_levels_backup = syslog_levels;

    LogLevels vg = LogLevels(true, Severities);
    LogLevels syslog = SyslogLogLevels(false,syslog_levels);

    cout << "\nVG: \n" << vg.to_string();
    vg.present(cout);
    cout << "\nSYSLOG: \n";//<< syslog.to_string();;
    syslog.present(cout);
    /*
    vector<string> lines;
    string delimiter = "\n";
    size_t pos = 0;
    string line;
    while((pos = syslog_levels.find(delimiter)) != std::string::npos)
    {
        line = syslog_levels.substr(0, pos);
        lines.push_back(line);
        syslog_levels.erase(0, pos + delimiter.length());
    }
    syslog_levels = syslog_levels_backup;
    */
    /*
    auto log_levels = syslog.get_log_levels();
    cout << "\nSYSLOG \n";
    present(lines, log_levels, cout);


    log_levels = vg.get_log_levels();
    cout << "\nVG \n";
    present(lines, log_levels, cout);
    */

    /*
    for (auto line = lines.begin(); line != lines.end(); ++line)
    {
        for (auto it = log_levels.begin() ; it != log_levels.end(); ++it)
        {
            if((pos = line->find(it->first)) != std::string::npos)
                cout << it->second << " = " << *line << "\n";
        }
        //cout << *line << '\n';
    }
*/
    //std::cout << syslog_levels + '\n';
    //std::cout << syslog_levels + '\n';
    //std::string values = syslog_levels.replace(syslog_levels.find("LOG_EMERG", std::to_string(LOG_EMERG)).c_str());
    //std::cout << values + '\n';

    return (0);
/*
    int prev_mask = setlogmask (LOG_UPTO (LOG_DEBUG));
    //setlogmask (LOG_UPTO (LOG_NOTICE));
    //setlogmask (LOG_UPTO (LOG_ERR));

    openlog ("exampleprog", LOG_CONS | LOG_PID | LOG_NDELAY, LOG_LOCAL1);

    syslog (LOG_DEBUG, "LOG_FULL = 0x%x",LOG_FULL);
    syslog (LOG_DEBUG, "logmask is set to  0x%x",LOG_UPTO (LOG_DEBUG));
    syslog (LOG_NOTICE, "Program started by User %d", getuid());
    syslog (LOG_INFO, "A tree falls in a forest");
    syslog (LOG_ERR, "All trees in a the forest fell");

    closelog ();
*/
}
  